# Sherlock Agent OSINT Credibility Verifier

A small OSINT credibility investigation app with a React-style frontend and Flask backend.

## Overview

- `backend/`: Flask API server that searches DDGS results and generates an investigation report via Groq.
- `frontend/`: Static frontend UI for querying claims and displaying the report as a boxed response.

## Features

- Investigates a query using DDGS search results.
- Generates a structured investigation report with:
  - Given Query
  - Confidence Score
  - Key Findings
  - Final Conclusion
  - References
- Uses a pink-themed boxed report layout.

## Backend Setup

1. Create and activate a virtual environment:

```bash
cd /Users/deepshikanaga/OSINT/backend
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Add your Groq API key to `backend/.env`:

```text
GROQ_API_KEY=your_groq_api_key_here
```

4. Start the backend server:

```bash
python3 app.py
```

The backend will run on `http://127.0.0.1:5001`.

## Frontend Setup

### Option 1: Open directly

Open `frontend/index.html` in a browser.

### Option 2: Serve locally

```bash
cd /Users/deepshikanaga/OSINT/frontend
python3 -m http.server 3000
```

Then open `http://127.0.0.1:3000`.

The frontend calls the backend at `http://127.0.0.1:5001/api/verify-credibility`.

## Usage

1. Start the backend.
2. Open the frontend in your browser.
3. Enter a claim or topic.
4. Click `Verify Credibility`.

The report will display in a styled boxed layout with the requested sections.

## Notes

- If the Groq model hits a rate limit, the API may return a `429` error and the frontend will show an investigation failure.
- The backend uses DDGS search results as the trusted evidence source.

## GitHub Push

To push the repository to GitHub:

```bash
git remote set-url origin https://github.com/HARINEE-WEB/osint-agenr.git
git branch -M main
git push -u origin main
```

