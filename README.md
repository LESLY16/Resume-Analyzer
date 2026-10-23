# Resume Analyzer

A full-stack application that analyzes uploaded resumes and provides an ATS-style evaluation against a selected target role. The project includes a FastAPI backend for processing and scoring candidate resumes, and a React + Vite frontend for user interaction.

## Overview

Resume Analyzer helps recruiters or applicants assess how well a resume matches a job target by:

- uploading a PDF or DOCX resume
- selecting a role (for example, software engineer, data analyst, product manager, etc.)
- extracting resume sections and keywords
- calculating ATS, role-match, and readability scores
- highlighting missing keywords and recommendations for improvement

## Features

- Resume upload support for PDF and DOCX files
- Role-based keyword analysis
- ATS score estimation
- Role match scoring
- Readability analysis
- Missing keyword recommendations
- Visitor count tracking
- Frontend autocomplete for role selection
- CORS-enabled API for local frontend use

## Tech Stack

- Frontend: React + Vite
- Backend: FastAPI
- Resume parsing: Python-based document processing
- Styling: CSS

## Repository Structure

```text
Resume-Analyzer/
├── resume-analyzer-ui/        # React frontend
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│   └── README.md
├── resume_analyzer_api/       # FastAPI backend
│   ├── app/
│   ├── requirements.txt
│   ├── Procfile
│   ├── runtime.txt
│   └── README.md
├── .vscode/
├── .gitignore
└── README.md
```

## Prerequisites

Before running the project, make sure you have:

- Python 3.10+
- Node.js 18+
- npm
- pip

## Backend Setup

1. Open a terminal and navigate to the API folder:

```bash
cd resume_analyzer_api
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# or
.venv\Scripts\activate      # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Start the API server:

```bash
uvicorn app.main:app --reload
```

The API will run at:

- http://localhost:8000

Available endpoints include:

- GET /
- GET /roles
- GET /visitor-count/increment
- POST /analyze

## Frontend Setup

1. Open a second terminal and navigate to the frontend folder:

```bash
cd resume-analyzer-ui
```

2. Install dependencies:

```bash
npm install
```

3. Start the app:

```bash
npm run dev
```

The frontend will typically run at:

- http://localhost:5173

## How It Works

1. Upload a resume file in PDF or DOCX format.
2. Select a target role.
3. The backend extracts text and sections from the document.
4. It compares document content against role-specific keywords.
5. The app returns:
   - ATS score
   - Role match score
   - Readability score
   - Missing keywords
   - Suggestions and recommendations

## Example Usage

- Open the frontend in the browser.
- Enter a target role (for example: "software engineer").
- Upload your resume.
- Click "Analyze Resume".
- Review the score breakdown and recommendations.

## Notes

- The frontend is configured to call the API at `http://localhost:8000`.
- The app expects a valid API key header for the analyze request in the local UI flow.
- This project is intended for local development and evaluation, not production deployment without additional security and configuration hardening.

## License

This project does not currently include a license file. Add one if you intend to publish or share the project publicly.

## Contributing

Contributions are welcome. Feel free to fork the repository, create a feature branch, and submit a pull request.

## Contact

For questions or collaboration, visit the repository on GitHub:

- https://github.com/LESLY16/Resume-Analyzer
