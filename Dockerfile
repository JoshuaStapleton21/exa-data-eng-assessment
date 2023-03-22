# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the local storage system and main pipeline file into the container
COPY execute_pipeline.py /app

# Copy the subdirectories with python tooling modules into the container
COPY tools /app/tools
COPY data /app/data
COPY data_output /app/data_output
COPY requirements.txt /app/requirements.txt

# Install any dependencies required by the pipeline
RUN pip install -r requirements.txt

# Define the command to run when the container starts
CMD ["python", "execute_pipeline.py"]