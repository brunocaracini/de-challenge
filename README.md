# Data Engineering Coding Challenge Solution 👩‍💻

Welcome to my solution for the Data Engineering coding challenge! This repository, hosted by [brunocaracini](https://github.com/brunocaracini/de-challenge), contains a comprehensive solution that covers **API** and **SQL** sections along with a bonus track for Cloud, Testing, and Containers. Let's dive in! 🚀

## Table of Contents 📑

- [Challenge Description & Considerations](#challenge-description--considerations)
  - [API (Section 1)](#section-1-api)
  - [SQL (Section 2)](#section-2-sql)
  - [Bonus Track](#bonus-track-cloud-testing--containers)
- [Resolution](#resolution-🌐)  
  - [Technology Stack](#technology-stack-🚀)
  - [Assumptions for the Resolution](#assumptions-for-the-resolution-🔍)
- [API & Server](#server--api-🌐)
  - [Installation](#installation-🛠️)
  - [Usage](#usage-📝)
  - [Endpoints](#endpoints-📊)
  - [CSV Data Import](#csv-data-import)
  - [Batch Transactions](#batch-transactions)
- [Database](#database-💾)
  - [PostgreSQL](#postgresql-🐘)
  - [Object Relational Mapping - SQLAlchemy](#object-relational-mapping---sqlalchemy)
- [Bonus Track](#bonus-track-🌟)
  - [Cloud Deployment](#cloud-deployment-☁️)
    - [Cloud Provider - Azure](#cloud-provider---azure)
    - [Services used for the deployment](#services-used-for-the-deployment)
    - [Integration with GitHub Actions for CI/CD](#integration-with-github-actions-for-cicd)
  - [Automated Tests](#automated-tests-🧪)
  - [Containerization](#containerization-🐳)
    - [Build image and run it](#build-image-and-run-it)

## Challenge Description & Considerations

This challenge is divided into several sections, and you can choose which sections to solve based on your experience and available time. Below, you'll find the requirements for each section.

### Section 1: API

In this section, you will create a local REST API for a database migration with three different tables: departments, jobs, and employees. The API should:

1. Receive historical data from CSV files.
2. Upload these files to the new SQL database.
3. Be able to insert batch transactions (1 up to 1000 rows) with one request.

You can use any programming language, libraries, and frameworks you prefer. You can also choose a SQL database of your choice. Don't forget to publish your code on GitHub and create a README.md file to document your solution and development process.

### Section 2: SQL

In this section, you need to explore the data inserted in the previous section and create specific endpoints for the following requirements:

#### Requirements

1. Number of employees hired for each job and department in 2021, divided by quarter. The table must be ordered alphabetically by department and job.

   Output example:
   
   | department          | job            | Q1  | Q2  | Q3  | Q4  |
   |---------------------|----------------|----|----|----|----|
   | Staff               | Recruiter      | 3  | 0  | 7  | 11 |
   | Staff               | Manager        | 2  | 1  | 0  | 2  |
   | Supply Chain        | Manager        | 0  | 1  | 3  | 0  |

2. List of ids, names, and the number of employees hired by each department that hired more employees than the mean of employees hired in 2021 for all the departments. Order the list by the number of employees hired in descending order.

   Output example:
   
   | id  | department      | hired |
   |----|----------------|-------|
   | 7   | Staff          | 45    |
   | 9   | Supply Chain   | 12    |

### Bonus Track! Cloud, Testing & Containers

To make your solution more robust, consider adding the following:

- Host your architecture in any public cloud using suitable cloud services.
- Add automated tests to the API. You can use any library and different test types if necessary.
- Containerize your application by creating a Dockerfile for deployment.

**Csv files structures:**

- **hired_employees.csv**:
  - id INTEGER: Id of the employee
  - name STRING: Name and surname of the employee
  - datetime STRING: Hire datetime in ISO format
  - department_id INTEGER: Id of the department which the employee was hired for
  - job_id INTEGER: Id of the job which the employee was hired for

  Example:

  `4535,Marcelo Gonzalez,2021-07-27T16:02:08Z,1,2`  
  `4572,Lidia Mendez,2021-07-27T19:04:09Z,1,2`  


- **departments.csv**:
  - id INTEGER: Id of the department
  - department STRING: Name of the department

  Example:

  `1, Supply Chain`  
  `2, Maintenance`  
  `3, Staff`

- **jobs.csv**:
  - id INTEGER: Id of the job
  - job STRING: Name of the job

  Example:  

  `1, Recruiter`  
  `2, Manager`  
  `3, Analyst`   

  

## Resolution 🌐

### Introduction 🌟

This application is a REST API that handles historical data from CSV files and interacts with a SQL database. The API allows for importing CSV data, as well as batch transactions for data insertion.

#### Deployed version in Azure: https://dechallenge.azurewebsites.net/docs#/

### Technology Stack 🚀
- Programming Language: Python with Poetry
- Web Framework: FastAPI
- Database: PostgreSQL (Docker container for local development, Azure PostgreSQL for production)
- Cloud: Microsoft Azure
- CI-CD: GitHub Actions

### Assumptions for the Resolution 🔍

  As the challenge is in the context of a migration with no specific requirement of data cleaning, the following assumptions were made:

  1. IDs are mandatory for Jobs, Hired Employees and Department (No autoincremental). As is a migration API, correspondence with original sources should be preserved as external tools might be using mappings of these ids.

  2. Null values are allowed in foreign keys for department_id and job_id while inserting Hired Employees. This is in order to ensure no edge cases are outside the final DB, as the challenge does not sepcifies wether an employee can be hired without an specific position already defined (job) or department to which is going to be assigned.

## Server & API 🌐

### Installation 🛠️

To run the API using [Poetry](https://python-poetry.org/), follow these steps:

1. Clone this repository:

   ```bash
   git clone https://github.com/brunocaracini/de-challenge.git

2. Navigate to the project directory:

    ```bash
    cd de-challenge/de_challenge
3. Install Poetry:

    ```bash
    pip install poetry
4. Install the required dependencies:

    ```bash
    poetry install
5. Run the application:

    ```bash
    poetry run uvicorn main:app
### Usage 📝
- The API is running locally and can be accessed at http://localhost:8000.

- Deployed version can be accessed at: https://dechallenge.azurewebsites.net/docs#/

### Endpoints 📊
The following endpoints are available in the API:

### Jobs Router:

  #### Batch CSV Upload
  - Endpoint: /batch-csv-upload/
  - Method: POST
  - Description: Upload CSV data in batches.
  - Request Body: JSON object containing CSV data in batches.
  - Parameters: 
      - **first_row_headers**: bool indicating wether the first row is containing the headers or not. In case a value is passed for this parameter, the values from the csv_header key on the body will be dismissed. In case is null, attributes from the enity (defined by the table columns) will be automatically applied as headers to the data, unless there is a value for csv_headers on the body.

    Example Request:

    ```bash
    POST /batch-csv-upload/
    Content-Disposition: form-data; name="csv_headers"
    
    [id, job]

    Content-Disposition: form-data; name="file"; filename="batch_data.csv"
    Content-Type: text/csv

    (id,job)
    1,Recruiter
    2,Manager
    3,Analyst
    4,Developer
    5,Designer
    
  #### Insert Many Jobs (up to 1000 per request)
  - Endpoint: /
  - Method: POST
  - Description: Insert multiple job records.
  - Request Body: JSON object containing a list of job records.

    ```bash
    POST /
    Content-Type: application/json
    
    {
      "jobs": [
        {
          "id": 1,
          "job": "Recruiter"
        },
        {
          "id": 2,
          "job": "Manager"
        },
        ...
      ]
    }
### Department Router:

  #### Batch CSV Upload
  - Endpoint: /batch-csv-upload/
  - Method: POST
  - Description: Upload CSV data in batches.
  - Request Body: JSON object containing CSV data in batches.
  - Parameters: 
      - **first_row_headers**: bool indicating wether the first row is containing the headers or not. In case a value is passed for this parameter, the values from the csv_header key on the body will be dismissed. In case is null, attributes from the enity (defined by the table columns) will be automatically applied as headers to the data, unless there is a value for csv_headers on the body.

    Example Request:

    ```bash
    POST /batch-csv-upload/
    Content-Disposition: form-data; name="csv_headers"
    
    [id, department]

    Content-Disposition: form-data; name="file"; filename="batch_data.csv"
    Content-Type: text/csv

    (id,department)
    1,HR
    2,IT
    3,Finance
    4,Engineering
    5,Design
    
  #### Insert Many Departments (up to 1000 per request)
  - Endpoint: /
  - Method: POST
  - Description: Insert multiple department records.
  - Request Body: JSON object containing a list of department records.

    ```bash
    POST /
    Content-Type: application/json
    
    {
      "departments": [
        {
          "id": 1,
          "department": "HR"
        },
        {
          "id": 2,
          "department": "IT"
        },
        ...
      ]
    }

### Hired Employees Router:

  #### Batch CSV Upload
  - Endpoint: /batch-csv-upload/
  - Method: POST
  - Description: Upload CSV data in batches.
  - Request Body: JSON object containing CSV data in batches.
  - Parameters: 
      - **first_row_headers**: bool indicating wether the first row is containing the headers or not. In case a value is passed for this parameter, the values from the csv_header key on the body will be dismissed. In case is null, attributes from the enity (defined by the table columns) will be automatically applied as headers to the data, unless there is a value for csv_headers on the body.

    Example Request:

    ```bash
    POST /batch-csv-upload/
    Content-Disposition: form-data; name="csv_headers"
    
    [id, name, job_id, department_id]
    
    Content-Disposition: form-data; name="file"; filename="batch_data.csv"
    Content-Type: text/csv

    (id,name,job_id,department_id)
    1,Emily Johnson,8,15
    2,Daniel Rodriguez,9,17
    3,Sophia Smith,15,11
    4,Liam Anderson,14,28
    5,Olivia Davis,25,31
    
  #### Insert Many Hired Employees (up to 1000 per request)
  - Endpoint: /
  - Method: POST
  - Description: Insert multiple hired employees records.
  - Request Body: JSON object containing a list of hired employees records.

    Example Request:

    ```bash
    POST /
    Content-Type: application/json
    
    {
      "hired_employees": [
        {
          "id": 1,
          "name": "Emily Johnson",
          "job_id": 8,
          "department_id": 15
        },
        {
          "id": 2,
          "name": "Daniel Rodriguez",
          "job_id": 9,
          "department_id": 17
        },
        ...
      ]
    }
    
  #### Get Hired Employees by Job and Department by Quarter for Specific Year
  - Endpoint: /by-job-and-department-by-quarter/
  - Method: GET
  - Description: Get the amount of employees hired for each department on each      quarter during the given year.
  - Parameters: 
      - **year**: int determining the year for which the report will be made.  Default value is 2021.  

  Example Request:

    GET /by-job-and-department-by-quarter/?year=2023

  #### Get Hired Employees By Department Higher Than Year Mean
  - Endpoint: /by-department-higher-than-year-mean/
  - Method: GET
  - Description: Get the departments that have hired more than the mean of hired employees during the given year.
  - Parameters: 
      - **year**: int determining the year for which the report will be made.  Default value is 2021.  

  Example Request:

    GET /by-department-higher-than-year-mean/?year=2023
### CSV Data Import
CSVs for sample uploads are available on the repository under the path:
    
    de_challenge/samples/csv_samples/
                                    |__ departments.csv
                                    |__ hired_employees.csv
                                    |__ jobs.csv

Disclaimer: CSV files MUST be comma separated.


### Batch Transactions
Transactions are allowed up to 1000 per request. In case of batch upload though CSV, that limit does not apply, instead, internall process trhough batches of 1000 recods will be applied.

## Database 💾

### PostgreSQL 🐘
The selected Database for this solution has been PostgreSQL, which is a free and open-source relational database management system (RDBMS) emphasizing extensibility and SQL compliance.

### Object Relational Mapping - SQLAlchemy
To make the connection between the server and the API, SQLAlchemy has been implemented. SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL. 

### Connecting to the DB while running locally

  - #### Running from Docker: 
    A Postgres database instance has been placed on the Docker image, and credentials are already on the .env file under config folder. **This DB is only for DEV purposes.**
  
  - #### Running locally without Docker:
    In this case, credentials must be replaced on the .env file in order to connect properly.

### Tables creation:

To force tables creation, run the main.py script with the --create_tables partameter. 
  
  In case your deploying your docker image for the first time, include this paramter con the final CMD line of the Dockerfile 

### Connecting to the DB while running on cloud
Credentials for Database connection must be stored into the following Environment Variables:

  - DB_HOST
  - DB_PORT
  - POSTGRES_DB
  - POSTGRES_USER
  - POSTGRES_PASSWORD

## Bonus Track 🌟

### Cloud Deployment ☁️

#### Cloud Provider - Azure
For cloud deployment, Microsoft Azure has been chosen as the cloud provider. Azure offers a wide range of services and tools that make it suitable for hosting applications and services.

#### Services used for the deployment

- Azure Container Registry (ACR): Azure Container Registry has been used to store and manage the Docker container images. ACR allows to securely store and version container images.

- Azure App Service: Azure App Service is a fully managed platform for building, deploying, and scaling web apps. The Docker image from ACR has been deployed to Azure App Service.

- Azure PostgreSQL: PostgreSQL instance in Azure has been set up to serve as the database for the application.

- Managed Identities: Managed Identities have been enabled to allow secure interaction between the Azure resources. Managed identities help in securing access and authentication between services without the need for explicit credentials.

#### Integration with GitHub Actions for CI/CD
The solution has been integrated with GitHub Actions for continuous integration and continuous deployment (CI/CD). GitHub Actions is used to automate the build and deployment process of application.

**Summary of the CI/CD flow:**

- Code Changes: Whenever changes are made to the code and pushed to the GitHub repository, GitHub Actions are triggered.

- Build Docker Image: A Docker image of the application is built by GitHub Actions using the Dockerfile.

- Push to Azure Container Registry: The Docker image is then pushed to Azure Container Registry (ACR), where it is securely stored.

- Deploy to Azure App Service: After the image is in ACR, the application is deployed to Azure App Service by GitHub Actions, making it accessible over the internet.

- Database Interaction: The application interacts with the Azure PostgreSQL database using managed identities, ensuring secure communication.

- Continuous Updates: With this CI/CD setup, any future code changes made and pushed to the repository trigger automatic updates and deployments, ensuring the application stays up to date.

#### Automated Tests 🧪
Automated tests have been conducted using the pytest framework in conjunction with Poetry. The testing process is structured to validate the functionality and reliability of the application. Different types of tests have been implemented to cover various aspects of the application:

Unit Tests: Unit tests focus on testing individual components or functions in isolation. These tests ensure that each part of the codebase performs as expected.

Integration Tests: Integration tests verify the interaction between different parts or modules of the application. They ensure that these components work correctly when combined.

**More tests types and/or tests could have been implemented to increase the coverage and cover different behaviours even in edge cases.

### Containerization 🐳
The application has been containerized using Docker, facilitated by the presence of a Dockerfile and a compose file in the repository. Containerization provides several benefits, such as portability, isolation, efficient deployment and scalability.

#### Build image and run it:

1. Create the docker image 

        docker-compose build

    In case you want the container also to run after the building, please, include paramter --up.

        docker-compose build --up

2. Tag it with a name and version:
        
        docker tag your-app-image:your-version your-container-registry-url/your-image-name:your-version

3. Log in to your container registry using the docker login command
        
        az login your-container-registry-url

4. Push the docker image:  

        docker push your-container-registry-url/your-image-name:your-version

#
This README provides an overview of the solution to the Data Engineering coding challenge. You can explore the code within the repository for a deeper understanding of the implementation. If you have any questions or need further information, please feel free to reach out.

Thank you for reviewing my solution! 👏
