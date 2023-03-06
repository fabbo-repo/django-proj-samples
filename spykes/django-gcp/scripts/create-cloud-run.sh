#!/bin/bash

set -e
FLAGS=$(getopt -a --options n:r:p:h --long "help,project-id:,region:,name:,service-account-email:,port:" -- "$@")

eval set -- "$FLAGS"

while true; do
    case "$1" in
        -h | --help )             help="true"; shift 1;;
        -p | --project-id )       projectId=$2; shift 2;;
        -r | --region )           region=$2; shift 2;;
        -n | --name )             name=$2; shift 2;;
        --service-account-email ) serviceAccountEmail=$2; shift 2;;
        --port )                  port=$2; shift 2;;
        --) shift; break;;
    esac
done

helpFunction() {
   echo "Creates a new Cloud Run service with a predefined HelloWorld image deployed and retrieves the public URL."
   echo ""
   echo "Flags:"
   echo -e "\t-p, --project-id     [Required] Project ID."
   echo -e "\t-n, --name           [Required] Name for the Cloud Run service endpoint."
   echo -e "\t-r, --region         [Required] Region where the Cloud Run service will be created."
   echo -e "\t--service-account-email         Service account email."
   echo -e "\t--port                          Service port."
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
    if [ -z "$region" ];
    then
        echo -e "${red}Error: Missing paramenters, -r or --region is mandatory." >&2
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

createCloudRunService() {
    extraArgs=""
    if [[ "$serviceAccountEmail" != "" ]] ; then
        extraArgs="${extraArgs} --service-account ${serviceAccountEmail}"
    fi
    if [[ "$port" != "" ]] ; then
        extraArgs="${extraArgs} --port ${port}"
    fi
    echo "Creating Cloud Run Instance..."
    if ! gcloud run deploy "$name" --image=us-docker.pkg.dev/cloudrun/container/hello --region "$region" --project "$projectId" --allow-unauthenticated $extraArgs; then
        echo -e "${red}Error: Cannot create Cloud Run Instance" >&2
        echo -ne "${white}" >&2
        exit 1
    fi
    serviceUrl=$(gcloud run services describe "$name" --format 'value(status.url)' --project "$projectId" --region "$region")
    echo "$serviceUrl"
}

#==============================================================
# SCRIPT EXECUTION:

if [[ "$help" == "true" ]]; then helpFunction; exit; fi

checkMandatoryArguments

ckeckCliInstalled

checkGcloudProjectId

createCloudRunService