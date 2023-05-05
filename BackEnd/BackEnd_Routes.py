from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask import g  # g对象在请求上下文中存储数据库连接
import pymysql
import os
import sys
import time
from werkzeug.datastructures import FileStorage

sys.path.append("C:/Users/likejie/AppData/Local/Programs/Python/Python39/Lib/site-packages")
from flask_cors import CORS

# Global Variables
# ----------------应用配置--------------------#
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)  # 解决跨域问题

app.config['UPLOAD_FILE_FOLDER'] = './uploads/files'  # 设置上传文件的文件夹路径
app.config['UPLOAD_IMAGE_FOLDER'] = './uploads/images'  # 设置上传图片的文件夹路径
app.config['ALLOWED_EXTENSIONS'] = {'xlsx', 'xls', 'csv', 'doc', 'docx', 'jpg', 'jpeg', 'png','pdf'}  # 设置允许的文件类型

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
    cursor.close()

    if result:
        personal_info = {
            'owner_id': owner_id,
            'username': result['username'],
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
            'avatar_url': result['avatar_url']
        }
    else:
        personal_info = {
            'owner_id': '',
            'username': '',
            'phone': '',
            'address': '',
            'email': '',
            'communityName': '',
            'buildingNumber': '',
            'unitNumber': '',
            'doorNumber': '',
            'parkingNumber': '',
            'securityCardNumber': '',
            'emergencyContact': '',
            'emergencyContactPhone': '',
            'avatar_url': '../../assets/images/userpic.jpg'
        }
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
                username=%s,
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
                avatar_url=%s
            WHERE id = %s
        """
    # print("Executing SQL:", sql)  # Print generated SQL

    cursor.execute(sql, (
        data['username'],
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
        data['avatar_url'],
        data['owner_id'],  # Add this line
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
                avatar_url=%s
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
@app.route('/test', methods=['POST'])
def my_test():
    data = request.get_json()
    print("received this time:", data)


# 获取用户列表
@app.route('/getUserList', methods=['POST'])
def get_user_list():
    data = request.get_json()
    page = data.get("page", 1)
    size = data.get("size", 10)

    cursor = g.db.cursor()
    query = """
        SELECT * FROM user
        LIMIT %s OFFSET %s
    """
    cursor.execute(query, (size, (page - 1) * size))
    result = cursor.fetchall()
    cursor.close()

    users = []
    if result:
        for row in result:
            users.append({
                'id': row['id'],
                'username': row['username'],
                'email': row['email'],
                'gender': row['gender'],
                'status': row['status'],
                'department': row['department'],
                'role': row['role'],
            })

    return jsonify({'list': users, 'total': len(users)})


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


#
# # 插入数据到 personal_info 表的函数
# def insert_personal_info(db, data):
#     cursor = db.cursor()
#     sql = """
#     INSERT
#     INTO
#     personal_info(
#         username, phone, address, email, community_name, building_number,
#         unit_number, door_number, parking_number, security_card_number,
#         emergency_contact, emergency_contact_phone, avatar_url
#     )
#     VALUES( % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s)
#     """
#     cursor.executemany(sql, data)
#     db.commit()
#     cursor.close()


# 检查文件是否为允许的文件类型

@app.route('/', methods=['GET', 'POST'])
def hello():
    return "Nice to see you again!"


if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FILE_FOLDER']):
        os.makedirs(app.config['UPLOAD_FILE_FOLDER'])  # 如果上传文件夹不存在，则创建
    if not os.path.exists(app.config['UPLOAD_IMAGE_FOLDER']):
        os.makedirs(app.config['UPLOAD_IMAGE_FOLDER'])

    # test_data = [
    #     ("张三", "13800138000", "上海市虹口区XX路XX号", "zhangsan@example.com", "阳光花园", "5栋", "2单元", "502室", "B-102", "AF-123456",
    #      "李四", "18212345678"),
    #     (
    #         "王五", "13900139000", "上海市浦东新区XX路XX号", "wangwu@example.com", "绿地新城", "3栋", "1单元", "301室", "B-203",
    #         "AF-234567",
    #         "赵六",
    #         "18323456789"),
    # ]
    # # 插入数据
    # insert_personal_info(mydb,test_data)

    app.run(debug=True)
