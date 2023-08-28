# Use the official AWS Lambda base image for Python
FROM public.ecr.aws/lambda/python:3.9

# Copy the Lambda function code into the container image
COPY . ${LAMBDA_TASK_ROOT}

# Install the Python dependencies listed in requirements.txt
RUN pip install -r ${LAMBDA_TASK_ROOT}/requirements.txt

# Set the CMD to your Lambda handler function
CMD ["app.lambda_handler"]
