#!/bin/bash

set -e
FLAGS=$(getopt -a --options n:p:h --long "help,project-id:,name:,location:,cors-url:" -- "$@")

eval set -- "$FLAGS"

while true; do
    case "$1" in
        -h | --help )             help="true"; shift 1;;
        -p | --project-id )       projectId=$2; shift 2;;
        -n | --name )             name=$2; shift 2;;
        --location )              location=$2; shift 2;;
        --cors-url )              corsUrl=$2; shift 2;;
        --) shift; break;;
    esac
done

helpFunction() {
   echo "Creates a Cloud Storage Bucket."
   echo ""
   echo "Flags:"
   echo -e "\t-p, --project-id        [Required] Project ID."
   echo -e "\t-n, --name              [Required] Name for the Cloud Storage bucket."
   echo -e "\t--location                         Location (https://cloud.google.com/storage/docs/locations)"
   echo -e "\t--cors-url                         Url available for CORS."
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

createCloudStorageBucket() {
    extraArgs=""
    if [[ "$location" != "" ]] ; then
        extraArgs="${extraArgs} --location ${location}"
    fi
    echo "Creating Cloud Storage Bucket..."
    if ! gcloud storage buckets create "gs://${name}" --project "$projectId" $extraArgs ; then
        echo -e "${red}Error: Cannot create Cloud Storage Bucket" >&2
        echo -ne "${white}" >&2
        exit 1
    fi
    echo "$serviceUrl"
}

applyCors() {
    export corsUrl
    envsubst '$corsUrl' < "./cors.json.template" > "./cors.json"
    gsutil cors set "./cors.json" "gs://${name}"
}

#==============================================================
# SCRIPT EXECUTION:

if [[ "$help" == "true" ]]; then helpFunction; exit; fi

checkMandatoryArguments

ckeckCliInstalled

checkGcloudProjectId

createCloudStorageBucket

if [[ "$corsUrl" != "" ]]; then applyCors; exit; fi