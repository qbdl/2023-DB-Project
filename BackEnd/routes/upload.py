# -----------------上传信息部分-----------------#
from flask import Blueprint, request, jsonify, g, current_app
import os
import time
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

# 创建一个名为 'upload' 的蓝图
upload_blueprint = Blueprint('upload', __name__)


# 上传头像
@upload_blueprint.route('/upload_avatar', methods=['POST'])
def upload_avatar():
    owner_id = request.args.get('owner_id', None, type=int)  # 获取owner_id参数
    print("upload_avatar_owner_id:", owner_id)

    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    myfile = request.files['file']

    if myfile.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if myfile and allowed_file(myfile.filename):
        filename = secure_filename(myfile.filename)
        myfile.save(os.path.join(current_app.config['UPLOAD_IMAGE_FOLDER'], filename))
        # 更新数据库中的头像 URL
        cursor = g.db.cursor()
        sql = """
            UPDATE personal_info SET
                avatar_path=%s
            WHERE id = %s
        """
        cursor.execute(sql, (os.path.join(current_app.config['UPLOAD_IMAGE_FOLDER'], filename), owner_id))
        g.db.commit()
        cursor.close()
        return jsonify({"message": "Avatar uploaded successfully"}), 200
    else:
        return jsonify({"error": "Unsupported file type"}), 400


# 上传文件
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def upload_save_file(file: FileStorage, path: str):
    file_ext = file.filename.rsplit('.', 1)[1].lower()
    timestamp = int(time.time())
    new_filename = f"{timestamp}_{file.filename}"
    file.save(os.path.join(path, new_filename))
    return new_filename


@upload_blueprint.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        new_filename = upload_save_file(file, current_app.config['UPLOAD_FILE_FOLDER'])
        return jsonify({"success": f"File uploaded and saved as {new_filename}"}), 200
    else:
        return jsonify({"error": "Unsupported file type"}), 400
