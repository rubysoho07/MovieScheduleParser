#!/bin/bash

# Download dependencies
echo 'Downloading dependencies ...'
mkdir -p python
pip install -r ../requirements.txt -t ./python/

# Copy Parser
echo 'Coping MovieScheduleParser ...'
cp -r ../MovieScheduleParser ./python/

# Download Chromedriver & Serverless Chrome
echo 'Downloading Chromedriver ...'
curl -O https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
mv -f chromedriver ./python/MovieScheduleParser/
rm chromedriver_linux64.zip

echo 'Downloading Serverless-chrome ...'
curl https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-55/stable-headless-chromium-amazonlinux-2017-03.zip -L -O
unzip stable-headless-chromium-amazonlinux-2017-03.zip
mv -f headless-chromium ./python/MovieScheduleParser/
rm stable-headless-chromium-amazonlinux-2017-03.zip

# Archiving Lambda Layer
echo 'Archiving lambda layer to a zip file ...'
zip -r lambda_layer.zip python/*

# Cleaning File
echo 'Cleaning all files ...'
rm -rf ./python

# Upload to S3 & Create Lambda Layer
echo 'Upload Lambda layer to S3 ...'
aws s3 cp ./lambda_layer.zip s3://$TARGET_BUCKET

echo 'Create Lambda Layer ...'
aws lambda publish-layer-version --layer-name 'MovieScheduleParser_Layer' \
    --content S3Bucket=$TARGET_BUCKET,S3Key=lambda_layer.zip --compatible-runtimes python3.7 | jq .LayerVersionArn

echo 'Creating Lambda Layer finished'
rm lambda_layer.zip