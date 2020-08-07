#!/bin/bash

# Script usage:
# ./build_and_deploy_package.sh ENV_NAME PACKAGE_NAME|--all
# Example:
# ./build_and_deploy_package.sh dev cc-services-axcess-preAuth
# ./build_and_deploy_package.sh dev --all
# ./build_and_deploy_package.sh uat cc-services-axcess-preAuth
# ./build_and_deploy_package.sh uat --all
# ./build_and_deploy_package.sh production cc-services-axcess-preAuth
# ./build_and_deploy_package.sh production --all

PACKAGES=(
  "cc-services-axcess-preAuth"
  "cc-services-TRUSTPayments-preAuth"
  "cc-db-save-preAuthResponse"
)

ENV_NAME="$1"
PACKAGE_NAME="$2"
DATETIME="_"$(date '+%Y-%m-%d-%H-%M-%S');
PRODUCTION_BRANCH_NAME="master"
UAT_BRANCH_NAME="uat"
BRANCH_NAME="$(git symbolic-ref -q --short HEAD)"
DEPLOYMENT_FOLDER="$PWD/deployment"

function build_package() {
  local PACKAGE_NAME=$1 # This is passed to the function while execution
  local PACKAGE_FOLDER_NAME="$PACKAGE_NAME"
  # Check package folder
  printf "Creating %s folder...\n" "$PACKAGE_FOLDER_NAME"
  if [ ! -d "$DEPLOYMENT_FOLDER"/"$PACKAGE_FOLDER_NAME" ]; then
    mkdir -p "$DEPLOYMENT_FOLDER"/"$PACKAGE_FOLDER_NAME"
  else
    rm -rf "$DEPLOYMENT_FOLDER"/"$PACKAGE_FOLDER_NAME"
    mkdir -p "$DEPLOYMENT_FOLDER"/"$PACKAGE_FOLDER_NAME"
  fi

  printf "\nCopying package files...\n"
  cp -rp "$PACKAGE_NAME"/. "$DEPLOYMENT_FOLDER"/"$PACKAGE_FOLDER_NAME"/

  #  copying modules
  cp -rp modules "$DEPLOYMENT_FOLDER"/"$PACKAGE_FOLDER_NAME"/

  #  copying layers
#  cp -rp layers "$DEPLOYMENT_FOLDER"/"$PACKAGE_FOLDER_NAME"/

  # Delete __pycache__ from package folder
  printf "\nDeleting __pycache__ folders...\n"
  find "$DEPLOYMENT_FOLDER/$PACKAGE_FOLDER_NAME" -name "__pycache__" -exec rm -r "{}" \;

  printf "\nBuilding ZIP package %s.zip ...\n" "$PACKAGE_FOLDER_NAME"
  cd "$DEPLOYMENT_FOLDER"/"$PACKAGE_FOLDER_NAME" || exit 1
  # Create deployment info file
  printf "Deployment executed by: $USER \nDeployment executed on: $DATETIME \nEnvironment: $ENV_NAME \nPackage: $PACKAGE_NAME \nBranch: $BRANCH_NAME" > deployment.txt

  zip -r ../"$PACKAGE_FOLDER_NAME".zip ./* .[^.]*
  # Go up to $DEPLOYMENT_FOLDER
  cd ../..
  printf "\nDone.\n\n"
}

function deploy_package() {
  local PACKAGE_NAME=$1 # This is passed to the function while execution
  local PACKAGE_FOLDER_NAME="$PACKAGE_NAME"
  local PACKAGE_FILE_NAME="$PACKAGE_FOLDER_NAME.zip"

  FUNCTION_NAME="$PACKAGE_NAME-$ENV_NAME"

  printf "\nDeploying function to AWS..."
  aws lambda get-function --profile credit --region eu-west-2 --function-name "$FUNCTION_NAME" >/dev/null 2>&1
  if [ 0 -eq $? ]; then
    printf "\nLambda '%s' exists. Updating..." "$PACKAGE_NAME"
    aws lambda update-function-code --profile credit --region eu-west-2 --function-name "$FUNCTION_NAME" --zip-file fileb://"$DEPLOYMENT_FOLDER/$PACKAGE_FILE_NAME"
  else
    printf "\nLambda '%s' does not exist. Creating and deploying..." "$PACKAGE_NAME"
  fi

  printf "\nDone. %s deployed to AWS Lambda" "$PACKAGE_NAME"
}

# Check deployment folder
if [ ! -d "$DEPLOYMENT_FOLDER" ]; then
  printf "Creating deployment folder ...\n"
  mkdir -p "$DEPLOYMENT_FOLDER/$PACKAGE_NAME"
fi

# Check environment
if ! [[ "$ENV_NAME" =~ ^(dev|uat|prod)$ ]]; then
  echo "Environment name missing or incorrect."
  exit 1
fi

if [ "$ENV_NAME" == "prod" ] && [ "$BRANCH_NAME" != $PRODUCTION_BRANCH_NAME ]; then
  printf "Only '%s' branch can be deployed to PRODUCTION environment. Before you deploy to PRODUCTION please make sure all is good for deployment. Deployment has to be approved anyway." "$PRODUCTION_BRANCH_NAME"
  exit 1
fi

if [ "$ENV_NAME" == "uat" ] && [ "$BRANCH_NAME" != $UAT_BRANCH_NAME ]; then
  printf "Only '%s' branch can be deployed to UAT environment. Before you deploy to UAT please make sure all is good for deployment. Deployment has to be approved anyway." "$UAT_BRANCH_NAME"
  exit 1
fi

if [[ "$ENV_NAME" =~ ^(uat|prod)$ ]]; then
  echo "You're about to deploy code to $ENV_NAME environment"
  echo "Please confirm you have granted all the required approvements and know what you're doing"
  read -p "[y|Y for Yes, any other key for No]: " CONFIRMATION
  if ! [[ "$CONFIRMATION" =~ ^(y|Y)$ ]]; then
    exit 0
  fi
fi

# Check package name
if [[ "$PACKAGE_NAME" == "--all" ]]; then
  for i in "${!PACKAGES[@]}"; do
    build_package "${PACKAGES[i]}"
    deploy_package "${PACKAGES[i]}"
  done
else
  # Check package name
  if [[ ! "${PACKAGES[@]}" =~ "${PACKAGE_NAME}" || "${PACKAGE_NAME}" == "" ]]; then
    printf "\nPackage name incorrect.\nAvailable packages:\n"
    for i in "${!PACKAGES[@]}"; do
      printf "${PACKAGES[i]} %s\n"
    done
    exit 1
  fi

  build_package "$PACKAGE_NAME"
  deploy_package "$PACKAGE_NAME"
fi

exit 0
