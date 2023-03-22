# EMIS Patient Data Pipeline (exa-data-eng-assessment)
#### - Technical project/interview for EMIS data engineer position


## Introduction

This project is a data pipeline that transforms patient FHIR data to a more workable, tabular format. The pipeline is designed to receive incoming FHIR messages from an external system or supplier, process and transform the data, and output it in either CSV format, or write to a SQL database.

## Technology Stack

This data pipeline is built using the following technologies:

- Python 3.9 - the programming language used to develop the pipeline
- Filesystem (CSV) - the data storage layer used to output the transformed data in tabular format
- SQLAlchemy - the ORM used to interact with the database
- Docker - used for containerization
- Additional frameworks/modules - Pandas, fhir.resources, requests, python-dotenv

## Setup Instructions

To get started with this data pipeline, clone this repository to your local machine. Then, follow either of these steps:

##### EITHER

In the root directory, run the following commands to create a virtual environment and install the required dependencies:
```
python3 -m venv venv
source venv/bin/activate
OR source .venv/bin/activate
python3 -m pip install -r requirements.txt
```
Then, run the pipeline in interactive mode through the execute_pipeline.ipynb notebook.

##### OR

Install Docker on your machine.
Open the terminal and navigate to the project directory.
Run the following commands to build the Docker container:

```
docker build -t <your container name here> .
```
Then, run the following command to start the container (ensure you use the same container name as above):
```
docker run -e host=<hostname> -e user=<username> -p 3000:3000 <your container name here>
```
Ensure to pass in the database connection strings as environment variables in the docker command.

## Directory Structure
```
- exa-data-eng-assessment
  |- data
    |- example_patient_1.json
    |- example_patient_2.json
    ...
  |- data_output
    |- 1NF_data
        |- 1NF_data.csv
    |- 2NF_data
        |- 2NF_main_table.csv
        |- 2NF_subtable_1.csv
        |- 2NF_subtable_2.csv
        ...
    0NF_raw_table.csv
  |- EDA
    |- FHIR_data_eda.ipynb
  |- resources
    |- bad_example.json
  |- tools
      |- create_database.py
      |- data_tests.py
      |- misc.py
      |- read_data.py
      |- update_database.py
- Dokerfile
- execute_pipeline.ipynb
- execute_pipeline.py
- Dockerfile
- README.md
|- requirements.txt
```


`exa-data-eng-assessment` - This directory contains the main pipeline code.

`data` - Directory hosting the raw input FHIR .json data files which are to be processed by the pipeline.

`data_output` - Directory hosting the processed tabular .csv data files which have been processed by the pipeline and written out in various normalizations.

`EDA` - This directory contains the Jupyter notebook used to explore the FHIR data and perform some basic EDA.

`resources` - This directory contains the bad_example.json file which is used to test the pipeline's error handling.

`tools` - This directory contains various tooling modules used by the pipeline.

`Dockerfile` - This file is used to build the Docker image for the pipeline.

`execute_pipeline.ipynb` - This Jupyter notebook is used to run the pipeline in interactive mode.

`execute_pipeline.py` - This is the main Python script that initiates the pipeline.

`README.md` - This file contains the project documentation.

`requirements.txt` - This file contains the Python dependencies required by the pipeline.

The repository also contains support for secure environment variables using the python-dotenv module. The .env file is not included in the repository for security reasons. Please add the necessary variables to a .env file in the root directory of the project, or by passing them in as environment variables in the docker run command as above.