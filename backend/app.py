from flask import Flask, request, jsonify
import tempfile
import PyPDF2

app = Flask(__name__, static_folder="../frontend", static_url_path="")


def extract_text_from_pdf(path):
    with open(path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text() or ""
            text += page_text
        return text


def analyze_document(text):
    words = text.split()
    summary = " ".join(words[:100])
    return summary


@app.route('/process', methods=['POST'])
def process_document():
    if 'document' not in request.files:
        return jsonify({'error': 'No document uploaded'}), 400
    uploaded_file = request.files['document']
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        uploaded_file.save(tmp.name)
        text = extract_text_from_pdf(tmp.name)
    summary = analyze_document(text)
    return jsonify({'summary': summary})


@app.route('/')
def index():
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run(debug=True)
