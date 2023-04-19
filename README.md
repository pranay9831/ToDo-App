# ToDo App
This is a simple ToDo App that uses AWS CloudFormation to set up an API Gateway, Lambda function, DynamoDB table, SNS topic, and Secrets Manager secret. The app allows users to create, read, update, and delete ToDo items.

# Architecture
**DynamoDB**: Stores ToDo items with a unique ID, task description, and completion status.
Lambda: A Python function that handles requests from API Gateway and performs CRUD operations on the DynamoDB table. It also sends notifications to the SNS topic when an item is added, updated, or deleted.

**API Gateway**: Provides RESTful API endpoints for the front-end application to interact with the Lambda function.

**SNS**: A Simple Notification Service topic that receives notifications from the Lambda function when ToDo items are modified.

**Secrets Manager**: Stores the SNS topic ARN as a secret, which is then retrieved by the Lambda function to send notifications.

# Deployment
1. Make sure you have an AWS account and the AWS CLI installed and configured.
2. Save the provided CloudFormation template (YAML file) to your local machine.
3. Use the AWS CLI to create a CloudFormation stack:
```
aws cloudformation create-stack --stack-name ToDoApp --template-body file://path/to/your/template.yaml --capabilities CAPABILITY_NAMED_IAM
```
4. Wait for the CloudFormation stack to complete its creation (check the AWS Management Console or use the AWS CLI to monitor the stack's status).
5. Once the stack is created, retrieve the API Gateway URL from the stack outputs:
```
aws cloudformation describe-stacks --stack-name ToDoApp --query 'Stacks[0].Outputs[?OutputKey==`ToDoAppApiUrl`].OutputValue' --output text
```
# Usage
You can interact with the API using any HTTP client or tool, such as curl, Postman, or a custom front-end application. The available endpoints are:

**GET /todos:** Get a list of all ToDo items.
POST /todos: Create a new ToDo item. Send a JSON object in the request body with the following format:
```
{
  "id": "unique-id",
  "task": "task-description",
  "completed": false
}
```
**PUT /todos:** Update an existing ToDo item. Send a JSON object in the request body with the following format:
```
{
  "id": "existing-id",
  "task": "updated-task-description",
  "completed": true
}
```
**DELETE /todos:** Delete an existing ToDo item. Send a JSON object in the request body with the following format:
```
{
  "id": "existing-id"
}
```
# Clean Up
To delete the resources created by this CloudFormation stack, use the AWS CLI to delete the stack:

```
aws cloudformation delete-stack --stack-name ToDoApp
```
Note that this will also delete the DynamoDB table and all its data. Make sure to back up any important data before deleting the stack.
