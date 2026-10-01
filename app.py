from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from services.gemini_service import GeminiService
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

app = Flask(__name__)
CORS(app)

gemini_service = GeminiService()

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    user_query = data.get("message", "")
    
    if not user_query:
        return jsonify({"error": "Message is required"}), 400

    try:
        result = gemini_service.process_support_pipeline(user_query)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/download-pdf", methods=["POST"])
def download_pdf():
    data = request.json
    chat_history = data.get("history", [])

    pdf_path = "smart_support_report.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle(
        'TitleStyle', parent=styles['Heading1'], fontSize=18, textColor='#1e293b', spaceAfter=12
    )

    story.append(Paragraph("Smart HR & IT Support - Session Report", title_style))
    story.append(Spacer(1, 10))

    for chat in chat_history:
        sender = "<b>User:</b> " if chat['isUser'] else "<b>AI Assistant:</b> "
        text = Paragraph(sender + chat['text'], styles['Normal'])
        story.append(text)
        story.append(Spacer(1, 6))

    doc.build(story)
    return send_file(pdf_path, as_attachment=True, download_name="support_report.pdf")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
