# Set the environment variables for your AWS credentials and other sensitive information
# export AWS_ACCESS_KEY_ID=<your_access_key_id>
# export AWS_SECRET_ACCESS_KEY=<your_secret_access_key>
# export AWS_SESSION_TOKEN=<your_session_token>
# export LAMBDA_ROLE_ARN=<your_lambda_role_arn>
# export S3_BUCKET=<your_s3_bucket>
# export S3_KEY=<your_s3_key>
# export FUNCTION_NAME=<your_function_name>
# export REGION=<your_region_on_AWS>

# Install your function's dependencies using pip
mkdir deploy
cp ./ingestao_s3/* deploy
cd ./deploy
pip install -r requirements.txt -t .

# Create a deployment package for your Lambda function
# check if the zip file exists
if [ -f "../function.zip" ]; then
    echo "Zip file $ZIPFILE already exists. Deleting..."
    rm "../function.zip"
else
    echo "Zip file $ZIPFILE does not exist."
fi
zip -r ../function.zip .
cd ..

# # Upload the deployment package to AWS S3
# Check if the bucket already exists
if aws s3api head-bucket --bucket "$S3_BUCKET" 2>/dev/null; then
  echo "Bucket $S3_BUCKET already exists"
else
  # Create the bucket
  aws s3api create-bucket --bucket "$S3_BUCKET" --region "$REGION"
  echo "Bucket $S3_BUCKET created"
fi
aws s3 cp function.zip s3://${S3_BUCKET}/${S3_KEY}

# Create or update your Lambda function
if aws lambda get-function --function-name "$FUNCTION_NAME" --region "$REGION" --no-cli-pager 2>/dev/null; then
  echo "Function $FUNCTION_NAME already exists"
  echo "Updating the function..."
  aws lambda update-function-code \
    --function-name "$FUNCTION_NAME" \
    --s3-bucket "$S3_BUCKET" \
    --s3-key "$S3_KEY" \
    --region "$REGION" \
    --publish \
    --no-cli-pager
else
  aws lambda create-function \
    --function-name ${FUNCTION_NAME} \
    --runtime python3.8 \
    --role ${LAMBDA_ROLE_ARN} \
    --handler lambda_function.lambda_handler \
    --environment "Variables={S3_BUCKET=${S3_BUCKET},S3_KEY=${S3_KEY}}" \
    --code "S3Bucket=${S3_BUCKET},S3Key=${S3_KEY}" \
    --timeout 900 \
    --memory-size 512 \
    --region "$REGION" \
    --no-cli-pager
fi