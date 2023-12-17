### AWS deployment process

Instructions also available when select "Push commands" for a selected AWS elastic container registry (ECR) repository. 
Similar reference instructions available here - https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html.

Note - sentence transformer model (all-MiniLM-L6-v2) and custom trained relevance model need to be downloaded and included locally in folder that Dockerfile builds from. Along with config.py, they are not included in this repo.

- On local machine, make code changes to lambda function that are then packaged / provisioned within Dockerfile (when run local build in later step)
- In AWS cloud console, create new repository in AWS ECR (e.g. aws-paper-agent-container-vX)
- On local machine, run first command from within "push commands" (in AWS cloud console in ECR) that starts `aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin [AWS host details]` - note this should not require any further local machine setup if AWS account credentials already setup correctly
- On local machine, run docker `build -t aws-paper-agent-container-vX .` This is the second command from within "push commands" (in AWS cloud console in ECR).
- On local machine, when docker image build is completed run third command from within "push commands" (in AWS cloud console in ECR) e.g. `docker tag aws-paper-agent-container-vX:latest [AWS host details]`
- On local machine, push this tagged image to AWS ECR which is the fourth command from within "push commands" (in AWS cloud console in ECR) e.g. `docker push [AWS host details]/aws-paper-agent-container-vX:latest`
- In AWS cloud console, go to the lambda aws-paper-agent-container (which has already been configured with an EventBridge event to run at 9am every day) and click on "Deploy new image". Run through instructions in UI to upload and connect the ECR image that just created. 
- In AWS cloud console, conduct a test run using the "Test" option in the lambda function console to confirm working as expected
- (Optional) In AWS cloud console, to manage costs, delete archive ECR repository used in previous version of the function