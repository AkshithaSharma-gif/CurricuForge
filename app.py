from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from curriculum_generator import generate_curriculum
from pdf_generator import create_pdf

app = Flask(__name__)
CORS(app)

@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/info")
def info():
    return render_template("info.html")


# Landing Page
@app.route("/")
def landing():
    return render_template("landing.html")


# Main Application Page (existing UI)
@app.route("/app")
def home():
    return render_template("index.html")


@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json

    curriculum = generate_curriculum(
        data.get("skill"),
        data.get("education_level"),
        data.get("semesters"),
        data.get("weekly_hours"),
        data.get("industry_focus")
    )

    return jsonify(curriculum)


@app.route('/api/download-pdf', methods=['POST'])
def download_pdf():
    pdf_buffer = create_pdf(request.json)

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name="Curriculum.pdf",
        mimetype="application/pdf"
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
