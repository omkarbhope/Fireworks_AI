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

# Design Rationale

## Choice of Technology Stack

### Frontend (HTML/CSS/JavaScript)
- **Why chosen**: For their simplicity and broad support across all web browsers, making the application easily accessible and enhancing user-friendliness.

### Backend (Python/FastAPI)
- **Why chosen**: Python is favored for its simplicity and robust library ecosystem. FastAPI is selected for its high performance and ease of building APIs with asynchronous capabilities, crucial for efficiently managing I/O-bound tasks such as network calls.

### Libraries (httpx and backoff)
- **Why chosen**: httpx supports asynchronous requests vital for making concurrent API calls to Fireworks AI, thus enhancing throughput and responsiveness. The backoff library is crucial for implementing retry logic, improving the application's robustness against transient network issues or API failures.

## API Call Strategy

- **Model Used**: llama-v3p2-11b-vision-instruct model from Fireworks AI.
- **Reason**: It allows for robust extraction of document features, thanks to its pre-trained capabilities on a wide variety of document types.
- **Implementation**: Making multiple API calls (five times) and using the most common results to mitigate the effects of potential inaccuracies in AI-based extraction, ensuring higher reliability of the parsed data.

## Error Handling and Data Verification

### Date Formatting and Validation
- **Approach**: Converting dates to a common format (MM/DD/YYYY) and verifying them against user inputs are critical for maintaining data integrity and ensuring the accuracy of information.

### Error-specific Feedback
- **Approach**: Providing detailed errors like 'Invalid date' or 'Expired ID' helps users understand exactly what went wrong, enhancing user experience and trust in the application.

# Trade-offs

## Performance vs. Accuracy
- **Details**: Repeated API calls increase the chances of correct data extraction but at the cost of increased response time and resource utilization. This tradeoff is considered acceptable given the importance of accuracy in identity verification.
- **Countermeasure**: Asynchronous execution helps mitigate some performance costs, but complexity increases with the management of asynchronous tasks.

## Simplicity vs. Feature Richness
- **Details**: The frontend is kept simple to reduce load times and dependency issues, which may limit advanced user interactions or more dynamic content. This choice prioritizes accessibility and ease of use over more complex functionalities.

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

