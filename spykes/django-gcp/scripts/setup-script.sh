#!/bin/bash
set -e

read -p "Setup Cloud SQL and press ENTER"

read -p "Project ID: " projectId
read -p "Region [us-central1]: " region
region=${region:-us-central1}
read -p "Location [US-CENTRAL1]: " location
location=${location:-US-CENTRAL1}

serviceAccount="djano-app-web"
serviceAccountEmail="${serviceAccount}@${projectId}.iam.gserviceaccount.com"
./create-service-account.sh --p "$projectId" --service-account "$serviceAccount"
./create-cloud-run.sh -p "$projectId" -n "django-app-web" -r "$region" --port 8000 --service-account-email "$serviceAccountEmail"

read -p "Web URL: " webUrl
storageBucket="djano-app-bucket-${projectId}"
echo "Using bucket name: ${storageBucket}"
./create-cloud-storage.sh -p $projectId -n "$storageBucket" --cors-url $webUrl --location $location

echo "Using Artifact Repository Name: django-app-repo"
# Locations: https://cloud.google.com/artifact-registry/docs/repositories/repo-locations
gcloud artifacts repositories create "django-app-repo" --repository-format=docker --location=$region

echo "Using Secret Manager name: django-app-secrets"
read -p "Setup .env.prod and press ENTER"
./create-secret-manager.sh -p $projectId -n "django-app-secrets" --env-file ../ProyectoWeb/.env.prod

echo "Giving permissions to service account"
gcloud secrets add-iam-policy-binding "django-app-secrets" --member serviceAccount:${serviceAccountEmail} --role roles/secretmanager.secretAccessor
gcloud projects add-iam-policy-binding $projectId --member serviceAccount:${serviceAccountEmail} --role roles/cloudsql.client

echo "Missing steps:"
echo "    1- Go to Cloud Run service, add SQL connection and add environment variables."
echo "    2- Go to Cloud Build service, create a trigger, add substitutions variables and Give SQL Client, Cloud Run, Cloud Build and Service Accounts permisions to cloudbuild service account."