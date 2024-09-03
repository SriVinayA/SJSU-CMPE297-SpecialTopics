# Resume and Job Description Analyzer

This is a local web application that allows users to upload their resume and a job description to analyze the match between them. It provides insights on matching skills, missing skills, and recommendations for improving the resume.

## Features

- File upload for resume (.docx or .pdf) and job description (.docx, .pdf, or .txt)
- Text extraction from uploaded documents
- Skill matching using NLP
- Recommendations for resume improvement
- Simple and intuitive web interface

## Installation

1. Clone this repository:
   ```
   git clone [repository-url]
   cd resume_analyzer
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Download the spaCy English model:
   ```
   python -m spacy download en_core_web_sm
   ```

## Usage

1. Start the Flask application:
   ```
   python app.py
   ```

2. Open a web browser and navigate to `http://localhost:5000`

3. Upload your resume and a job description, then click "Analyze"

4. View the results, including matching skills, missing skills, and recommendations

## Notes

- This application runs locally and does not require an internet connection after installation.
- Uploaded files are processed in-memory and are not stored permanently.
- The skill extraction is based on a simple NLP approach and may not catch all skills. In a production environment, a more sophisticated skill extraction method would be recommended.

## Future Improvements

- Implement more advanced NLP techniques for better skill extraction
- Add support for more file formats
- Improve the user interface with real-time analysis and interactive features
- Implement user accounts for saving and comparing multiple analyses