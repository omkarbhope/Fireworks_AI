# Identity Verification PoC using Firework AI

## Overview
This proof of concept (PoC) demonstrates the use of Firework AI’s platform and APIs to automate the extraction of necessary information for identity verification from provided documents. This application leverages `llama-v3p2-11b-vision-instruct` model from Fireworks_AI. 

The application consists of a front-end and several back-end services that handle different aspects of the workflow:

### Frontend
- **HTML/CSS/JavaScript:** Basic components for user interaction and display.
- **Image Assets:** Visual elements for user guidance.

### Backend Services
- **Main Application (`main.py`):** Orchestrates the server and routes.
- **Fireworks Client (`services/fireworks_client.py`):** Manages API calls to Firework AI for processing documents.
- **File Handler (`services/file_handler.py`):** Controls file uploads and storage.
- **Date Check (`services/date_check.py`):** Verifies the validity of dates extracted from documents.

### Workflow structure:

- Welcome Page
- Click on continue to go to user page
- Enter user details and upload file to verify identify
- Click on verify Identity
- Results Success (Show User Data) / Failure (Show Error: Error type)

### Design Choice:

- User inputs name, DOB, address, file.
- Verify Identity button calls the Fireworks API
- The `llama-v3p2-11b-vision-instruct` extracts (Document_type, Document_number, Name, Sex, DOB, Expiry_Date, Address) from the image.
- Image extraction can be faulty at times, to tackle this error the function is called 5 times. Maximum occurence of each value is taken and an aggregated result is generated.
- 5 API calls are made parallely using async and await functions.
- The Dates are brought to common format (MM/DD/YYYY)
- The DOB on ID is compared with user input
- If the dates are mismatched - Invalid date error is thrown
- If the ID is expired  - Expired ID error is thrown.


## Requirements
To run this project, you will need the following:
- Python 3.8 or higher
- fastapi
- uvicorn
- python-multipart
- pydantic
- httpx
- backoff


Install the necessary libraries using:

`pip install requirements.txt`

## Frontend run:

`npm install -g http-server`
`http-server -p 3000 --cors`

## Backend run:

`uvicorn main:app --reload`

