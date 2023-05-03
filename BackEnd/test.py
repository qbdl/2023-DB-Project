from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import pymysql
import os
import sys

sys.path.append("C:/Users/likejie/AppData/Local/Programs/Python/Python39/Lib/site-packages")
from flask_cors import CORS

# Global Variables
# ----------------应用配置--------------------#
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)  # 解决跨域问题

app.config['UPLOAD_FOLDER'] = './uploads'  # 设置上传文件夹路径
app.config['ALLOWED_EXTENSIONS'] = {'xlsx', 'xls', 'csv', 'doc', 'docx'}  # 设置允许的文件类型

# ----------------数据库配置--------------------#
db_config = {
    'host': 'localhost',
    'user': 'username',
    'password': 'password',
    'database': 'db_name'
}


# 检查文件是否为允许的文件类型
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    myfile = request.files['file']

    if myfile.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if myfile and allowed_file(myfile.filename):
        filename = secure_filename(myfile.filename)
        myfile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({"message": "File uploaded successfully"}), 200
    else:
        return jsonify({"error": "Unsupported file type"}), 400


@app.route('/', methods=['GET', 'POST'])
def hello():
    return "hello world"


@app.route('/home/', methods=['GET', 'POST'])
def hello2():
    return "Nice to see you again!"


if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])  # 如果上传文件夹不存在，则创建
    app.run(debug=True)
