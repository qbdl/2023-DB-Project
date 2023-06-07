from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask import g  # g对象在请求上下文中存储数据库连接
import pymysql
import os
import sys
import time
import json
from werkzeug.datastructures import FileStorage
from datetime import datetime, date

sys.path.append("C:/Users/likejie/AppData/Local/Programs/Python/Python39/Lib/site-packages")
from flask_cors import CORS

# Global Variables
# ----------------应用配置--------------------#
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)  # 解决跨域问题

app.config['UPLOAD_FILE_FOLDER'] = './uploads/files'  # 设置上传文件的文件夹路径
app.config['UPLOAD_IMAGE_FOLDER'] = './uploads/images'  # 设置上传图片的文件夹路径
app.config['ALLOWED_EXTENSIONS'] = {'xlsx', 'xls', 'csv', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'pdf'}  # 设置允许的文件类型

# ----------------数据库配置--------------------#
#  MySQL 数据库的实际信息
db_config = {
    'host': 'localhost',
    'user': 'qbdl',
    'password': 'likejie123',
    'database': '2023_security_database'
}


# 连接到数据库的辅助函数
def get_db_connection():
    db = pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database'],
        cursorclass=pymysql.cursors.DictCursor
    )
    return db


# 数据库
mydb = get_db_connection()


@app.before_request
def before_request():
    g.db = get_db_connection()


@app.teardown_request
def teardown_request(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


# -------------------------------数据库表操作------------------------------------#

# -----------------登陆注册部分-----------------#
@app.route('/login', methods=['POST'])
def login():
    info = {"code": 200, "data": {"access_token": "bqddxxwqmfncffacvbpkuxvwvqrhln"}, "msg": "成功"}
    return json.dumps(info)


@app.route('/auth/buttons', methods=['GET'])
def buttons():
    info = {"code": 200, "msg": "成功", "data": {"useProTable": ["add", "batchAdd", "export", "batchDelete", "status"],
                                               "authButton": ["add", "edit", "delete", "import", "export"]}}
    return json.dumps(info)


@app.route('/logout', methods=['POST'])
def logout():
    info = {"code": 200, "msg": "成功"}
    return json.dumps(info)


# -----------------个人信息(业主信息）管理部分-----------------#
def get_personal_info_by_id(owner_id):
    cursor = g.db.cursor()
    query = """
        SELECT *
        FROM personal_info
        WHERE id = %s
    """
    cursor.execute(query, (owner_id,))

    result = cursor.fetchone()
    print("fetch results:", result)
    cursor.close()

    if result:
        personal_info = {
            'id': owner_id,
            'idCard': result['idCard'],
            'username': result['username'],
            'gender': result['gender'],
            'phone': result['phone'],
            'address': result['address'],
            'email': result['email'],
            'communityName': result['community_name'],
            'buildingNumber': result['building_number'],
            'unitNumber': result['unit_number'],
            'doorNumber': result['door_number'],
            'parkingNumber': result['parking_number'],
            'securityCardNumber': result['security_card_number'],
            'emergencyContact': result['emergency_contact'],
            'emergencyContactPhone': result['emergency_contact_phone'],
            'avatar_path': result['avatar_path'],
            'faceInfo_path': result['faceInfo_path'],
            # 'createTime': result['createTime']
        }
    else:
        personal_info={}

    #     personal_info = {
    #         'id': '',
    #         'idCard': '',
    #         'username': '',
    #         'gender': '',
    #         'phone': '',
    #         'address': '',
    #         'email': '',
    #         'communityName': '',
    #         'buildingNumber': '',
    #         'unitNumber': '',
    #         'doorNumber': '',
    #         'parkingNumber': '',
    #         'securityCardNumber': '',
    #         'emergencyContact': '',
    #         'emergencyContactPhone': '',
    #         'avatar_path': '../../assets/images/userpic.jpg',
    #         'faceInfo_path': '../../assets/images/userpic.jpg',
    #         'createTime': ''
    #     }
    return jsonify(personal_info)


@app.route('/myapi/info', methods=['GET'])
def get_info():
    # is_owner = request.args.get('is_owner', 0, type=int)
    # print(is_owner)
    owner_id = request.args.get('owner_id', None, type=int)  # 获取owner_id参数
    print(owner_id)

    if owner_id is None:
        print("no owner_id!")
        owner_id = 1  # TODO:get_current_logged_in_user_id()
    return get_personal_info_by_id(owner_id)


# ----------------业主信息管理——获取所有业主用户名-----------------#
@app.route('/myapi/owners', methods=['GET'])
def get_all_owners():
    cursor = g.db.cursor()
    query = """
        SELECT id, username
        FROM personal_info
    """
    cursor.execute(query)

    result = cursor.fetchall()
    cursor.close()

    owners = []
    if result:
        for row in result:
            owners.append({
                'id': row['id'],
                'username': row['username']
            })
    return jsonify(owners)


# -----------------个人信息(业主信息）更新部分-----------------#
# 更新数据——由前端调用自动更新
@app.route('/myapi/info_update', methods=['PUT'])
def update_personal_info():
    data = request.get_json()

    print("Received data:", data)  # Print received data

    cursor = g.db.cursor()
    sql = """
                UPDATE personal_info SET
                    idCard=%s,
                    username=%s,
                    gender=%s,
                    phone=%s,
                    address=%s,
                    email=%s,
                    community_name=%s,
                    building_number=%s,
                    unit_number=%s,
                    door_number=%s,
                    parking_number=%s,
                    security_card_number=%s,
                    emergency_contact=%s,
                    emergency_contact_phone=%s,
                    avatar_path=%s,
                    faceInfo_path=%s
                WHERE idCard=%s
            """
    # print("Executing SQL:", sql)  # Print generated SQL

    cursor.execute(sql, (
        data['idCard'],
        data['username'],
        data['gender'],
        data['phone'],
        data['address'],
        data['email'],
        data['communityName'],
        data['buildingNumber'],
        data['unitNumber'],
        data['doorNumber'],
        data['parkingNumber'],
        data['securityCardNumber'],
        data['emergencyContact'],
        data['emergencyContactPhone'],
        data['avatar_path'],
        data['faceInfo_path'],
        # data['createTime'],
        data['idCard'],
    ))
    g.db.commit()
    cursor.close()

    return jsonify({"message": "Personal info updated successfully"})


# 上传头像
@app.route('/upload_avatar', methods=['POST'])
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
        myfile.save(os.path.join(app.config['UPLOAD_IMAGE_FOLDER'], filename))
        # 更新数据库中的头像 URL
        cursor = g.db.cursor()
        sql = """
            UPDATE personal_info SET
                avatar_path=%s
            WHERE id = %s
        """
        cursor.execute(sql, (os.path.join(app.config['UPLOAD_IMAGE_FOLDER'], filename), owner_id))
        g.db.commit()
        cursor.close()
        return jsonify({"message": "Avatar uploaded successfully"}), 200
    else:
        return jsonify({"error": "Unsupported file type"}), 400


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def upload_save_file(file: FileStorage, path: str):
    file_ext = file.filename.rsplit('.', 1)[1].lower()
    timestamp = int(time.time())
    new_filename = f"{timestamp}_{file.filename}"
    file.save(os.path.join(path, new_filename))
    return new_filename


# 上传文件
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        new_filename = upload_save_file(file, app.config['UPLOAD_FILE_FOLDER'])
        return jsonify({"success": f"File uploaded and saved as {new_filename}"}), 200
    else:
        return jsonify({"error": "Unsupported file type"}), 400


# ---------------------------------------------------------------#

# -----------------车辆信息部分(没用上）-----------------#
class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj: any) -> any:
        """
        重写json构造类，增加对解析时间的支持
        """
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


@app.route('/user/list', methods=['POST'])
def getUserList():
    cursor = g.db.cursor()
    query = """
            SELECT * FROM users_outline
        """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    print("results:", result)
    info = {"code": 200, "msg": "成功", "data": {"list": result,
                                               "pageNum": 1, "pageSize": 25, "total": len(result)}}
    return json.dumps(info, cls=DatetimeEncoder)


@app.route('/user/gender', methods=['GET'])
def gender():
    info = {"code": 200, "data": [{"genderLabel": "男", "genderValue": 1}, {"genderLabel": "女", "genderValue": 2}],
            "msg": "成功"}
    return json.dumps(info)


@app.route('/user/status', methods=['GET'])
def status():
    info = {"code": 200, "data": [{"userLabel": "启用", "userStatus": 1}, {"userLabel": "禁用", "userStatus": 0}],
            "msg": "成功"}
    return json.dumps(info)


@app.route('/test', methods=['POST'])
def my_test():
    data = request.get_json()
    print("received this time:", data)


# 新增用户
@app.route('/user/add', methods=['POST'])
def add_user():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    gender = data.get("gender")
    status = data.get("status")
    department = data.get("department")
    role = data.get("role")

    cursor = g.db.cursor()
    query = """
        INSERT INTO user (username, email, gender, status, department, role)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (username, email, gender, status, department, role))
    g.db.commit()
    cursor.close()

    return jsonify({"message": "User added successfully"})


# 编辑用户
@app.route('/user/edit', methods=['POST'])
def edit_user():
    data = request.get_json()
    user_id = data.get("id")
    username = data.get("username")
    email = data.get("email")
    gender = data.get("gender")
    status = data.get("status")
    department = data.get("department")
    role = data.get("role")

    cursor = g.db.cursor()
    query = """
        UPDATE user SET
            username=%s,
            email=%s,
            gender=%s,
            status=%s,
            department=%s,
            role=%s
        WHERE id=%s
    """
    cursor.execute(query, (username, email, gender, status, department, role, user_id))
    g.db.commit()
    cursor.close()

    return jsonify({"message": "User updated successfully"})


# 删除用户
@app.route('/user/delete', methods=['POST'])
def delete_user():
    data = request.get_json()
    user_ids = data.get("id")

    cursor = g.db.cursor()
    query = """
        DELETE FROM user WHERE id IN %s
    """
    cursor.execute(query, (user_ids,))
    g.db.commit()
    cursor.close()

    return jsonify({"message": "User(s) deleted successfully"})


# 切换用户状态
@app.route('/user/change', methods=['POST'])
def change_user_status():
    data = request.get_json()
    user_id = data.get("id")
    new_status = data.get("status")

    cursor = g.db.cursor()
    query = """
        UPDATE user
        SET
        status=%s
        WHERE id=%s
        """
    cursor.execute(query, (new_status, user_id))
    g.db.commit()
    cursor.close()
    return jsonify({"message": "User status updated successfully"})


# ------------------小区安防公告-------------------------------------#
# 接受安防公告
@app.route('/myapi/announcements', methods=['GET'])
def get_announcements():
    cursor = g.db.cursor()
    cursor.execute("SELECT * FROM security_announcements")
    announcements = cursor.fetchall()
    cursor.close()
    return jsonify(announcements)


# 发布安防公告
@app.route('/myapi/create_announcement', methods=['POST'])
def create_announcement():
    announcement = request.json
    id = announcement['id']
    title = announcement['title']
    date = announcement['date']
    author = announcement['author']
    status = announcement['status']
    content = announcement['content']

    cursor = g.db.cursor()
    cursor.execute(
        "INSERT INTO security_announcements (id, title, date, author, status, content) VALUES (%s, %s, %s, %s, %s, %s)",
        (id, title, date, author, status, content))
    g.db.commit()

    return jsonify({"message": "Announcement created successfully"}), 201

@app.route('/', methods=['GET', 'POST'])
def hello():
    return "Nice to see you again!"


if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FILE_FOLDER']):
        os.makedirs(app.config['UPLOAD_FILE_FOLDER'])  # 如果上传文件夹不存在，则创建
    if not os.path.exists(app.config['UPLOAD_IMAGE_FOLDER']):
        os.makedirs(app.config['UPLOAD_IMAGE_FOLDER'])

    app.run(debug=True)
