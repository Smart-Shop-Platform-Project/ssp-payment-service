# Use the official AWS Lambda Python base image
FROM public.ecr.aws/lambda/python:3.12

# Set the working directory in the container
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY ./app ${LAMBDA_TASK_ROOT}/app
COPY lambda_handler.py ${LAMBDA_TASK_ROOT}/

# Set the command to the handler function
CMD [ "lambda_handler.handler" ]
