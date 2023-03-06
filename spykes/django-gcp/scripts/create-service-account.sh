#!/bin/bash

set -e
FLAGS=$(getopt -a --options p:h --long "help,project-id:,service-account:" -- "$@")

eval set -- "$FLAGS"

while true; do
    case "$1" in
        -h | --help )             help="true"; shift 1;;
        -p | --project-id )       projectId=$2; shift 2;;
        --service-account )       serviceAccount=$2; shift 2;;
        --) shift; break;;
    esac
done

helpFunction() {
   echo "Creates a Service Account."
   echo ""
   echo "Flags:"
   echo -e "\t-p, --project-id     [Required] Project ID."
   echo -e "\t--service-account    [Required] Service account name (not an email)."
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
    # Service account check
    if [ -z "$serviceAccount" ];
    then
        echo -e "${red}Error: Missing paramenters, --serviceAccount is mandatory." >&2
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

createServiceAccount() {
    serviceAccounts=$(gcloud projects get-iam-policy "$projectId" --format='flattened' | grep members | grep serviceAccount: | cut -d ':' -f 3-)
    serviceAccountsArray=($serviceAccounts)
    
    echo "Creating Service Account..."
    serviceAccountEmail="${serviceAccount}@${projectId}.iam.gserviceaccount.com"
    echo -e "${white}Checking if service account ${serviceAccount} already exists..."
    if [[ ! " ${serviceAccountsArray[*]} " =~ " $serviceAccountEmail " ]]; # Searches right literal in left array. More info: https://stackoverflow.com/a/15394738
    then
        echo -e "${white}Creating new service account: $serviceAccountEmail..."
        if ! gcloud iam service-accounts create "$serviceAccount" --display-name="$serviceAccount" &> /dev/null;
        then
            echo -e "${red}Error: Cannot create service account with display name $serviceAccount." >&2
            echo -ne "${white}"
            exit 2
        else
            echo -e "${green}Service account $serviceAccount created successfully."
            echo -ne "${white}"
        fi
    else
        echo -e "${white}The service account $serviceAccount exists already. Proceeding to use it."
    fi
    echo -e "${white}Creating keys JSON file for service account $serviceAccount..."
    if ! gcloud iam service-accounts keys create "./key.json" --iam-account="$serviceAccountEmail" &> /dev/null;
    then
        echo -e "${white}Error: Service account key could not be created." >&2
        echo -ne "${white}"
        exit 2
    else
        echo -e "${green}Service account key creation ended successfully."
        echo -ne "${white}"
    fi
}

#==============================================================
# SCRIPT EXECUTION:

if [[ "$help" == "true" ]]; then helpFunction; exit; fi

checkMandatoryArguments

ckeckCliInstalled

checkGcloudProjectId

createServiceAccount