# Test Emulator

An example of a test emulator (TEmu) to help test payment integration.

In short, emulator of external API.
Note: This does not copy or emulate any actual existing API.

This is a pet project implemented using FastAPI, MongoDB, httpx, Poetry and Pytest.
    
## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
- [Usage](#usage)
    - [Running the Application](#running-the-application)
- [Potential Improvements](#potential-improvements)

## Features

- FastAPI to manage asynchronous endpoints.
  - Endpoint for creating payments ("/payment"):
    - Validation of incoming request (signature, body)
    - Storing data in the database
    - Provides different responses based on received amount value (several error cases just for presentation):
      - amount == "any value": default response with the specified structure and signature (HTTP 200)
      - amount == 101: response with only mandatory fields (HTTP 200)
      - amount == 102: error response (HTTP 400) 
      - amount == 103: unsigned response (HTTP 200)
  - Endpoint to update created order ("/update-order"):
    - Allows updating data in the TEmu database. For emulation of different behavior of external API to test your payment adapter.
  - Endpoint for check-status ("/check-status"):
    - Validation of incoming request (signature, body)
    - Fetching data from the database
    - Provides different responses based on order amount value (several error cases just for presentation):
      - amount == "any value": default response with the specified structure and signature (HTTP 200)
      - amount == 201: response with only mandatory fields (HTTP 200)
      - amount == 202: error response (HTTP 400) 
      - amount == 203: unsigned response (HTTP 200)
  - Endpoint to trigger callback ("/callback-request").
    - Allows triggering a callback query from TEmu to the previously received "callback_url"
    - Provides different queries based on order amount value (several error cases just for presentation):
      - amount == "any value": default callback with the specified structure and signature
      - amount == 301: callback with only mandatory fields
      - amount == 302: unsigned callback
- Using MongoDB asynchronously to work with orders.
- httpx is used to send callback asynchronously.
- Poetry is used to manage library versions and the project version.
- Pytest for module and integration tests.
- A separate test environment is used for integration tests.
- Simple and straightforward project structure.

## Project Structure

The project follows the following directory structure:

```
test-emulator/
├── temu/
│   ├── api/
│   │   ├── endpoints/
│   │   │   ├── callback.py
│   │   │   ├── check_status.py
│   │   │   ├── order_update.py
│   │   │   ├── payment.py
│   │   ├── models/
│   │   │   ├── callback.py
│   │   │   ├── check_status.py
│   │   │   ├── payment.py
│   │   │   ├── update_order.py
│   │   ├── signature/
│   │   │   ├── signature.py
│   ├── db/
│   │   ├── connection.py
│   │   ├── database.py
│   ├── settings/
│   │   ├── config.py
│   │   ├── log_config.yaml
├── tests/
│   ├── conftest.py
│   ├── integration/
│   │   ├── test_database.py
│   ├── unit/
│   │   ├── test_callback.py
│   │   ├── test_check_status.py
│   │   ├── test_order_update.py
│   │   ├── test_payment.py
├── .env
├── .env.example
├── .env_test
├── .gitignore
├── main.py
├── poetry.lock
├── poetry.toml
├── pytest.ini
├── README.md
```

- `api/endpoints`: Contains the logic for handling external API endpoints (e.g., payment creation, order update, etc.).
- `api/models`: Defines data models used for request validation and response formatting.
- `api/signature`: Contains logic for handling and verifying signatures in API requests and responses.
- `db`: Manages database connection and operations, including fetching, updating and storing data.
- `settings`: Configuration settings for the project, including logging and other environment-specific variables.
- `tests`: Contains unit and integration tests for the project.
- `.env`: Stores environment variables (e.g., database credentials, API keys).
- `.env.example`: Example structure of the `.env` file to demonstrate required environment variables.
- `.env_test`: Configuration file for environment variables used in testing.
- `.gitignore`: Lists files and directories to be ignored by version control (e.g., virtual environments, logs).
- `main.py`: The entry point for the application, where the API is initialized and run.
- `poetry.lock`: Lock file for project dependencies managed by Poetry.
- `poetry.toml`: Configuration file for Poetry, specifying project metadata and dependencies.
- `pytest.ini`: Configuration file for pytest settings (e.g., test discovery, markers).
- `README.md`: Documentation about the project, including setup and usage instructions.

## Getting Started

### Prerequisites

Before running the application, make sure you have the following prerequisites installed:

- Python 3.10+ (3.12 recommended).
- MongoDB.

### Installation

1. Install Poetry if you haven't already. You can do this by following the [Poetry installation guide](https://python-poetry.org/docs/#installation).

2. Clone the repository:

   ```bash
   git clone https://github.com/DAS-SPB/test-emulator.git
   ```
   
3. Navigate to the project directory:

   ```bash
   cd test-emulator
   ```

4. Install project dependencies using Poetry:

   ```bash
   poetry install
   ```
This will create a virtual environment and install all dependencies listed in pyproject.toml.

## Usage

### Running the Application

To run application locally, you can just run `main.py`:

   ```bash
   python3 main.py
   ```

## Potential improvements

CI/CD Integration: Set up continuous integration (CI) to automate testing and deployment processes. 
This would ensure that each change is automatically tested and validated before being merged, improving code quality and reducing manual effort. 
Tools like GitHub Actions, GitLab CI, or Jenkins could be used to implement automated testing, linting, and deployment pipelines.
