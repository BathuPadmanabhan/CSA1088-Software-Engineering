from flask import Flask, request, render_template
import fitz  
from gtts import gTTS
import os

app = Flask(__name__)

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def text_to_speech(text, output_path, lang='en'):
    tts = gTTS(text=text, lang=lang)
    tts.save(output_path)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pdf_file = request.files['pdf']
        target_language = request.form['target_language']
        pdf_path = os.path.join('uploads', pdf_file.filename)
        pdf_file.save(pdf_path)
        output_path = os.path.join('outputs', 'output.mp3')
        text = extract_text_from_pdf(pdf_path)
        text_to_speech(text, output_path, lang=target_language)
        return 'Audio file generated successfully!'
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
