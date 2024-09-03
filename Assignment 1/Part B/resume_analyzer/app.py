import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import spacy
from docx import Document
from pdfminer.high_level import extract_text

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_text_from_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() == '.docx':
        doc = Document(file_path)
        return ' '.join([paragraph.text for paragraph in doc.paragraphs])
    elif file_extension.lower() == '.pdf':
        return extract_text(file_path)
    elif file_extension.lower() == '.txt':
        with open(file_path, 'r') as file:
            return file.read()
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")

def extract_skills(text):
    doc = nlp(text)
    skills = set()
    for ent in doc.ents:
        if ent.label_ == "SKILL":
            skills.add(ent.text.lower())
    return skills

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files or 'job_description' not in request.files:
        return jsonify({'error': 'Both resume and job description must be uploaded'}), 400

    resume_file = request.files['resume']
    job_description_file = request.files['job_description']

    if resume_file.filename == '' or job_description_file.filename == '':
        return jsonify({'error': 'Both files must have a filename'}), 400

    try:
        # Save and process resume
        resume_filename = secure_filename(resume_file.filename)
        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_filename)
        resume_file.save(resume_path)
        resume_text = extract_text_from_file(resume_path)
        resume_skills = extract_skills(resume_text)

        # Save and process job description
        jd_filename = secure_filename(job_description_file.filename)
        jd_path = os.path.join(app.config['UPLOAD_FOLDER'], jd_filename)
        job_description_file.save(jd_path)
        jd_text = extract_text_from_file(jd_path)
        jd_skills = extract_skills(jd_text)

        # Analyze
        matching_skills = resume_skills.intersection(jd_skills)
        missing_skills = jd_skills - resume_skills

        # Generate recommendations
        recommendations = []
        if missing_skills:
            recommendations.append(f"Consider adding the following skills to your resume: {', '.join(missing_skills)}")
        recommendations.append("Ensure your resume uses standard headings like 'Experience', 'Education', and 'Skills'")
        recommendations.append("Avoid using graphics or complex formatting that may confuse ATS systems")
        recommendations.append("Tailor your experience descriptions to match key phrases from the job description")

        return jsonify({
            'matching_skills': list(matching_skills),
            'missing_skills': list(missing_skills),
            'recommendations': recommendations
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        # Clean up uploaded files
        if os.path.exists(resume_path):
            os.remove(resume_path)
        if os.path.exists(jd_path):
            os.remove(jd_path)

if __name__ == '__main__':
    app.run(debug=True)