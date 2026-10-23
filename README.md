# API Monitoring & Service Request Management System

A Python FastAPI application developed as a Python Development Internship Project.

The system combines API endpoint monitoring with service request management. It can monitor external APIs, measure response time, detect failures, retry failed requests, store monitoring results in SQLite, and automatically create service requests for detected API failures.

---

## Project Overview

The **API Monitoring & Service Request Management System** is designed to monitor the availability and performance of external APIs and manage service requests related to system failures.

The application provides two major modules:

1. **API Monitoring**
2. **Service Request Management**

### API Monitoring

The monitoring module can:

- Monitor external API endpoints
- Check HTTP response status
- Measure response time
- Detect successful and failed requests
- Retry failed requests
- Record the number of attempts
- Store error messages
- Store monitoring results in SQLite
- Generate monitoring reports

### Service Request Management

The service request module can:

- Create service requests
- Read service requests
- Read an individual service request
- Update service requests
- Delete service requests
- Search service requests
- Filter by status
- Filter by priority
- Automatically create a service request when API monitoring detects a failure

---

## Technologies Used

- **Python 3.13**
- **FastAPI**
- **SQLAlchemy**
- **SQLite**
- **Pydantic**
- **Requests**
- **Pytest**
- **Uvicorn**

---

## Project Structure

```text
api-monitoring-service/
│
├── app/
│   ├── __init__.py
│   ├── api_monitor.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── service_requests.py
│   └── utils.py
│
├── data/
│   ├── monitoring.db
│   └── test_monitoring.db
│
├── reports/
│
├── samples/
│
├── screenshots/
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_monitoring.py
│   └── test_service_requests.py
│
├── .gitignore
├── README.md
└── requirements.txt

Application Architecture

                    Client
                       |
                       v
                FastAPI Application
                       |
             +---------+---------+
             |                   |
             v                   v
       API Monitoring      Service Requests
             |                   |
             v                   v
       External API         CRUD Operations
             |
             v
      Monitoring Result
             |
             v
           SQLite

API Monitoring Module
The monitoring module allows an external API endpoint to be checked through the /monitor endpoint.
Monitor Endpoint
POST /monitor
Monitors the supplied API endpoint.
Request
{
  "endpoint": "https://jsonplaceholder.typicode.com/posts"
}

Successful Response
{
  "id": 1,
  "endpoint": "https://jsonplaceholder.typicode.com/posts",
  "status_code": 200,
  "status": "SUCCESS",
  "response_time_ms": 815.77,
  "attempt": 1,
  "error_message": null
}

Response Fields
Field	Description
id	Unique monitoring result ID
endpoint	API endpoint that was monitored
status_code	HTTP response status code
status	Monitoring result status
response_time_ms	API response time in milliseconds
attempt	Number of attempts made
error_message	Error message when monitoring fails


Failed API Monitoring
The application can detect API failures and retry the request.

For example:
{
  "endpoint": "https://jsonplaceholder.typicode.com/invalid-endpoint"
}

The endpoint returns HTTP 404, so the monitoring system marks it as failed.
Example Response
{
  "id": 7,
  "endpoint": "https://jsonplaceholder.typicode.com/invalid-endpoint",
  "status_code": 404,
  "status": "FAILED",
  "response_time_ms": 1799.06,
  "attempt": 3,
  "error_message": "404 Client Error: Not Found for url: https://jsonplaceholder.typicode.com/invalid-endpoint"
}

The attempt value of 3 indicates that the monitoring system retried the request before marking it as failed.
Automatic Service Request Creation
When API monitoring detects a failure, the application can create a corresponding service request.

For example, a failed API monitoring result can generate a service request similar to:
{
  "title": "External API failure",
  "description": "API monitoring detected a failure. Endpoint: https://jsonplaceholder.typicode.com/invalid-endpoint. HTTP status: 404. Error: 404 Client Error: Not Found for url: https://jsonplaceholder.typicode.com/invalid-endpoint",
  "status": "OPEN",
  "priority": "HIGH",
  "requester": "API Monitor",
  "assigned_to": "Operations Team"
}

This connects the monitoring system with the service-request management system.
Service Request Management
The service request module provides complete CRUD functionality.

CRUD means:
- Create
- Read
- Update
- Delete
Service Request Endpoints
Method	Endpoint	Description
POST	/service-requests	Create a service request
GET	/service-requests	Get service requests
GET	/service-requests/{request_id}	Get a service request by ID
PUT	/service-requests/{request_id}	Update a service request
DELETE	/service-requests/{request_id}	Delete a service request


Create Service Request
POST /service-requests
Creates a new service request.
Request Body
{
  "title": "Payment API failure",
  "description": "Payment service returned HTTP 500",
  "priority": "HIGH",
  "requester": "Deepak",
  "assigned_to": "Employee01"
}

Example Response
{
  "id": 2,
  "title": "Payment API failure",
  "description": "Payment service returned HTTP 500",
  "status": "OPEN",
  "priority": "HIGH",
  "requester": "Deepak",
  "assigned_to": "Employee01",
  "created_at": "2026-10-23T14:32:56.497227",
  "updated_at": "2026-10-23T14:32:56.497241"
}

The status is automatically initialized as:
OPEN

Get All Service Requests
GET /service-requests
Returns all service requests.
Example Response
[
  {
    "id": 1,
    "title": "External API failure",
    "description": "API monitoring detected a failure.",
    "status": "OPEN",
    "priority": "HIGH",
    "requester": "API Monitor",
    "assigned_to": "Operations Team",
    "created_at": "2026-10-23T16:52:37.084274",
    "updated_at": "2026-10-23T16:52:37.084297"
  }
]

Get Service Request by ID
GET /service-requests/{request_id}
Returns a specific service request.

Example:
/service-requests/2

Response
{
  "id": 2,
  "title": "Payment API failure",
  "description": "Payment service returned HTTP 500",
  "status": "OPEN",
  "priority": "HIGH",
  "requester": "Deepak",
  "assigned_to": "Employee01",
  "created_at": "2026-10-23T14:32:56.497227",
  "updated_at": "2026-10-23T14:32:56.497241"
}

Search Service Requests
The service request list endpoint supports searching.

Example:
GET /service-requests?search=Payment

The search can be used to find service requests matching a keyword.
Filter by Priority
Service requests can be filtered by priority.

Example:
GET /service-requests?priority=HIGH

Supported priorities:
- LOW
- MEDIUM
- HIGH
Filter by Status
Service requests can also be filtered by status.

Example:
GET /service-requests?status=OPEN

Supported statuses:
- OPEN
- IN_PROGRESS
- RESOLVED
- CLOSED
Update Service Request
PUT /service-requests/{request_id}
Updates an existing service request.

The request can be used to change fields such as:
- Title
- Description
- Status
- Priority
- Requester
- Assigned employee
Delete Service Request
DELETE /service-requests/{request_id}
Deletes a service request using its ID.

Example:
DELETE /service-requests/2

Database
The project uses SQLite with SQLAlchemy ORM.

The main database is:
data/monitoring.db

The application uses SQLAlchemy to communicate with the SQLite database.
Database Tables
1. service_requests
The service_requests table stores service request information.
Column	Description
id	Unique request ID
title	Request title
description	Detailed description
status	Current request status
priority	Request priority
requester	Person/system creating the request
assigned_to	Person/team assigned to the request
created_at	Request creation time
updated_at	Last update time


2. monitoring_results
The monitoring_results table stores API monitoring information.
Column	Description
id	Unique monitoring result ID
endpoint	Monitored API endpoint
status_code	HTTP response status
status	SUCCESS or FAILED
response_time_ms	Response time
attempt	Attempt number
error_message	Error information
checked_at	Time when monitoring was performed


FastAPI Documentation
FastAPI automatically provides interactive API documentation.

After starting the application, open:
http://127.0.0.1:8000/docs

The Swagger UI allows you to:
- View available endpoints
- Enter request data
- Execute API requests
- View responses
- Test validation
- Test query parameters
Running the Project
1. Open the project directory
cd C:\Users\DEEPAK\Desktop\skycurve\api-monitoring-service

2. Activate the virtual environment
.\venv\Scripts\Activate.ps1

If PowerShell blocks script execution, run:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

Then activate:
.\venv\Scripts\Activate.ps1

You should see:
(venv) PS C:\Users\DEEPAK\Desktop\skycurve\api-monitoring-service>

3. Install dependencies
If dependencies are not installed:
pip install -r requirements.txt

4. Start the application
Run:
python -m app.main

5. Open Swagger
Open:
http://127.0.0.1:8000/docs

Testing
The project uses pytest for automated testing.

Run all tests with:
pytest -v

Test Coverage
The project currently contains 12 automated tests.
Monitoring Tests
The monitoring test suite verifies:
1. Successful API monitoring
2. Failed API monitoring
3. Retrieving monitoring results
4. Monitoring report generation
5. Invalid monitoring request handling
Service Request Tests
The service-request test suite verifies:
6. Creating a service request
7. Getting service requests
8. Getting a service request by ID
9. Handling a non-existent service request
10. Searching service requests
11. Filtering by priority
12. Filtering by status
Test Result
The complete test suite currently passes successfully:
12 passed

This confirms that all implemented monitoring and service-request tests are passing.
Example Test Command
pytest -v

Expected result:
collected 12 items

tests/test_monitoring.py::test_monitor_success PASSED
tests/test_monitoring.py::test_monitor_failure PASSED
tests/test_monitoring.py::test_get_monitoring_results PASSED
tests/test_monitoring.py::test_monitoring_report PASSED
tests/test_monitoring.py::test_invalid_monitor_request PASSED

tests/test_service_requests.py::test_create_service_request PASSED
tests/test_service_requests.py::test_get_service_requests PASSED
tests/test_service_requests.py::test_get_service_request_by_id PASSED
tests/test_service_requests.py::test_get_nonexistent_service_request PASSED
tests/test_service_requests.py::test_service_request_search PASSED
tests/test_service_requests.py::test_service_request_filter_by_priority PASSED
tests/test_service_requests.py::test_service_request_filter_by_status PASSED

12 passed

Error Handling
The application handles different types of errors, including:
- Invalid API endpoints
- HTTP errors
- Failed API requests
- API retry attempts
- Invalid request data
- Missing service requests
- Validation errors
- Database operations
API Monitoring Flow
Client
  |
  v
POST /monitor
  |
  v
Validate Endpoint
  |
  v
Send HTTP Request
  |
  +-------------------+
  |                   |
  v                   v
SUCCESS             FAILURE
  |                   |
  |                   v
  |                 Retry
  |                   |
  |              +----+----+
  |              |         |
  |           Success    Failed
  |                        |
  v                        v
Save Result             Save Result
                           |
                           v
                   Create Service
                      Request
                           |
                           v
                   Return Response

Service Request Flow
Create Request
      |
      v
Validate Data
      |
      v
Save to Database
      |
      v
Return Service Request

For an automatically generated monitoring failure:
API Failure
    |
    v
Monitoring Result
    |
    v
Create Service Request
    |
    v
Priority = HIGH
    |
    v
Status = OPEN
    |
    v
Operations Team

Sample Monitored APIs
The project was tested using:
Successful Endpoint
https://jsonplaceholder.typicode.com/posts

Expected HTTP status:
200

Failed Endpoint
https://jsonplaceholder.typicode.com/invalid-endpoint

Expected HTTP status:
404

The failed endpoint is useful for testing retry and error-handling functionality.
Configuration
The SQLite database is configured in:
app/database.py

The database URL is:
DATABASE_URL = "sqlite:///./data/monitoring.db"


The SQLAlchemy engine uses:
connect_args={"check_same_thread": False}


This allows SQLite to be used with the FastAPI application.
Testing Database
The project also contains a separate test database:
data/test_monitoring.db

This helps keep automated tests separate from the main application database.
Important Project Files
app/main.py
Contains the main FastAPI application and API endpoints.
app/api_monitor.py
Contains API monitoring functionality such as:
- Sending requests
- Measuring response time
- Retry handling
- Saving monitoring results
app/service_requests.py
Contains service request management functionality.
app/models.py
Contains SQLAlchemy database models.
app/schemas.py
Contains Pydantic schemas used for API request and response validation.
app/database.py
Contains:
- SQLite configuration
- SQLAlchemy engine
- Session configuration
- Database dependency
app/utils.py
Contains reusable utility functionality used by the application.
Development Workflow
The project was developed incrementally:
Project Setup
     |
     v
Virtual Environment
     |
     v
FastAPI Setup
     |
     v
SQLite + SQLAlchemy
     |
     v
Service Request CRUD
     |
     v
API Monitoring
     |
     v
Retry Handling
     |
     v
Automatic Service Requests
     |
     v
Automated Tests
     |
     v
12 Tests Passing

Current Project Status
The API Monitoring & Service Request Management System has been implemented successfully.
Completed Features
- [x] FastAPI application
- [x] SQLite database
- [x] SQLAlchemy models
- [x] API endpoint monitoring
- [x] HTTP status detection
- [x] Response-time measurement
- [x] Retry mechanism
- [x] Monitoring result storage
- [x] Monitoring report
- [x] Service request creation
- [x] Service request retrieval
- [x] Service request update
- [x] Service request deletion
- [x] Service request search
- [x] Status filtering
- [x] Priority filtering
- [x] Automatic service request generation for API failures
- [x] Pytest test suite
- [x] 12 automated tests passing
Final Test Status
12 / 12 Tests Passed

The project is ready for final documentation, Git commit, and submission.

Author
Deepak

Python Development Internship
Python Development Internship Project

Project: API Monitoring & Service Request Management System

### One thing I would change before committing

Your latest code has already moved to timezone-aware timestamps (`DateTime(timezone=True)` and `utc_now`), based on your screenshot. So the README is fine, but make sure the **actual `models.py` and README are consistent**.

Also, because your latest test result is:

```text
12 passed, 1 warning

I would not claim 12 passed, 0 warnings anywhere. The warning is from the installed Starlette/httpx compatibility layer, not a failing test.

## Screenshots

### Swagger API Documentation

![Swagger API Documentation]
(screenshots\Screenshot 2026-10-23 233339.png)

### Successful API Monitoring

![Successful API Monitoring]
(screenshots\Screenshot 2026-10-23 233612.png)
(screenshots\Screenshot 2026-10-23 233659.png)

### Failed API Monitoring

![Failed API Monitoring]
(screenshots\Screenshot 2026-10-23 233822.png)
(screenshots\Screenshot 2026-10-23 233841.png)

### Monitoring Results

![Monitoring Results]
(screenshots\Screenshot 2026-10-23 233947.png)
(screenshots\Screenshot 2026-10-23 234050.png)
(screenshots\Screenshot 2026-10-23 234117.png)

### Monitoring Report

![Monitoring Report]
(screenshots\Screenshot 2026-10-23 234249.png)
(screenshots\Screenshot 2026-10-23 234338.png)

### Service Request Creation

![Service Request Creation]
(screenshots\Screenshot 2026-10-23 234459.png)

### Service Request List

![Service Request List]
((screenshots\Screenshot 2026-10-23 234516.png))

### Service Request Search

![Service Request Search](screenshots/08-service-request-search.png)

### Service Request Priority Filter

![Service Request Priority Filter]
(screenshots\Screenshot 2026-10-23 234756.png)
(screenshots\Screenshot 2026-10-23 234814.png)

### Service Request Status Filter

![Service Request Status Filter]
(screenshots\Screenshot 2026-10-23 234857.png)
(screenshots\Screenshot 2026-10-23 234918.png)


