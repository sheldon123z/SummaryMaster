from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
import PyPDF2

app = Flask(__name__)

# 配置文件上传的保存路径
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 检查文件是否为允许的类型
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 处理文件上传的路由
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        # 在这里调用你的PDF处理函数
        summary = process_pdf(file_path)
        # 删除上传的文件
        os.remove(file_path)
        return jsonify({'summary': summary}), 200
    else:
        return jsonify({'error': 'File type not allowed'}), 400

# 处理PDF文件的函数
def process_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        text = ''
        for page_num in range(reader.numPages):
            text += reader.getPage(page_num).extractText()
        # 这里只是一个示例，你需要根据实际情况来处理和总结文本
        # 例如，你可以调用OpenAI API来生成摘要
        return text[:100]  # 返回前100个字符作为摘要

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)