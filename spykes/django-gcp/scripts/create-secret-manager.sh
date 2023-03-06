#!/bin/bash

set -e
FLAGS=$(getopt -a --options n:p:h --long "help,project-id:,name:,env-file:" -- "$@")

eval set -- "$FLAGS"

while true; do
    case "$1" in
        -h | --help )             help="true"; shift 1;;
        -p | --project-id )       projectId=$2; shift 2;;
        -n | --name )             name=$2; shift 2;;
        --env-file )               envFile=$2; shift 2;;
        --) shift; break;;
    esac
done

helpFunction() {
   echo "Creates a Secret Manager instance and upload secrets."
   echo ""
   echo "Flags:"
   echo -e "\t-p, --project-id     [Required] Project ID"
   echo -e "\t-n, --name           [Required] Name for the Cloud Storage bucket."
   echo -e "\t--env-file           [Required] File path for environment variables (secrets) to upload."
}

# Colours for the messages.
white='\e[1;37m'
red='\e[0;31m'

# Mandatory argument check
checkMandatoryArguments() {
    # Project id check
    if [ -z "$projectId" ];
    then
        echo -e "${red}Error: Missing paramenters, -p or --project-id is mandatory." >&2
        echo -e "${red}Use -h flag to display help." >&2
        echo -ne "${white}" >&2
        exit 2
    fi
    # Service Name check
    if [ -z "$name" ];
    then
        echo -e "${red}Error: Missing paramenters, -n or --name is mandatory." >&2
        echo -e "${red}Use -h flag to display help." >&2
        echo -ne "${white}" >&2
        exit 2
    fi
    if [ -z "$envFile" ];
    then
        echo -e "${red}Error: Missing paramenters, --env-file is mandatory." >&2
        echo -e "${red}Use -h flag to display help." >&2
        echo -ne "${white}" >&2
        exit 2
    fi
    if ! [ -f "$envFile" ];
    then
        echo -e "${red}Error: Env file does not exists." >&2
        echo -ne "${white}" >&2
        exit 2
    fi
}

# Required CLI check
ckeckCliInstalled() {
    # Check if GCloud CLI is installed
    if ! [ -x "$(command -v gcloud)" ]; then
        echo -e "${red}Error: GCloud CLI is not installed." >&2
        echo -ne "${white}" >&2
        exit 127
    fi
}

checkGcloudProjectId() {
    # Check if exists a Google Cloud project with that project ID. 
    if ! gcloud projects describe "$projectId" 2> /dev/null ; then
        echo -e "${red}Error: Project $projectId does not exist." >&2
        echo -ne "${white}" >&2
        exit 1
    fi
}

createSecretManagerInstance() {
    echo "Creating Secret Manager Instance..."
    if ! gcloud secrets create $name --project $projectId --replication-policy automatic ; then
        echo -e "${red}Error: Cannot create Secret Manager Instance" >&2
        echo -ne "${white}" >&2
        exit 1
    fi
}

uploadEnv() {
    echo "Uploading Secrets..."
    if ! gcloud secrets versions add $name --data-file "$envFile" --project $projectId ; then
        echo -e "${red}Error: Cannot create Secret Manager Instance" >&2
        echo -ne "${white}" >&2
        exit 1
    fi
}

givePermissions() {
    projectNum=$(gcloud projects describe "$projectId" --format 'value(projectNumber)')
    gcloud secrets add-iam-policy-binding $name \
        --member serviceAccount:${projectNum}@cloudbuild.gserviceaccount.com \
        --role roles/secretmanager.secretAccessor
    gcloud secrets describe $name
}

#==============================================================
# SCRIPT EXECUTION:

if [[ "$help" == "true" ]]; then helpFunction; exit; fi

checkMandatoryArguments

ckeckCliInstalled

checkGcloudProjectId

createSecretManagerInstance

uploadEnv

givePermissions