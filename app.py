from flask import Flask, request, send_from_directory, jsonify
from PIL import Image, ImageDraw, ImageFont
from fpdf import FPDF
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
PDF_FOLDER = 'pdfs'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PDF_FOLDER, exist_ok=True)

@app.route('/convert', methods=['POST'])
def convert_to_pdf():
    if 'image' not in request.files:
        return jsonify({'status': 'fail', 'message': 'No image file provided.'}), 400

    image_file = request.files['image']
    name = request.form.get('name', '')
    subject = request.form.get('subject', '')

    # 텍스트 위치 설정
    name_position = (580, 550)  # 이름 텍스트 위치 (x, y)
    subject_position = (580, 630)  # 과목 텍스트 위치 (x, y)

    # 이미지 열기
    image = Image.open(image_file.stream)
    draw = ImageDraw.Draw(image)

    # 폰트 설정 (경로를 실제 폰트 파일로 수정 필요)
    font = ImageFont.truetype("arial.ttf", 40)

    # 텍스트 추가
    draw.text(name_position, name, font=font, fill="black")
    draw.text(subject_position, subject, font=font, fill="black")

    # 이미지를 서버에 저장
    img_path = os.path.join(UPLOAD_FOLDER, 'annotated_image.jpg')
    image.save(img_path)

    # PDF 생성
    pdf = FPDF()
    pdf.add_page()
    pdf.image(img_path, x=10, y=10, w=180)

    # PDF를 서버에 저장
    pdf_path = os.path.join(PDF_FOLDER, 'certificate.pdf')
    pdf.output(pdf_path)

    return jsonify({'status': 'success', 'downloadUrl': f'/pdfs/certificate.pdf'})

@app.route('/pdfs/<filename>', methods=['GET'])
def download_pdf(filename):
    return send_from_directory(PDF_FOLDER, filename)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
