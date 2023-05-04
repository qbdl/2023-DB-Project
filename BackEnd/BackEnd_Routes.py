from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask import g  # g对象在请求上下文中存储数据库连接
import pymysql
import os
import sys

sys.path.append("C:/Users/likejie/AppData/Local/Programs/Python/Python39/Lib/site-packages")
from flask_cors import CORS

# Global Variables
# ----------------应用配置--------------------#
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)  # 解决跨域问题

app.config['UPLOAD_FILE_FOLDER'] = './uploads/files'  # 设置上传文件的文件夹路径
app.config['UPLOAD_IMAGE_FOLDER'] = './uploads/images'  # 设置上传图片的文件夹路径
app.config['ALLOWED_EXTENSIONS'] = {'xlsx', 'xls', 'csv', 'doc', 'docx', 'jpg', 'jpeg', 'png'}  # 设置允许的文件类型

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


mydb = get_db_connection()


@app.before_request
def before_request():
    g.db = get_db_connection()


@app.teardown_request
def teardown_request(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


# ----------------数据库表操作--------------------#

# -----个人信息(业主信息）管理部分------#

@app.route('/myapi/personal_info', methods=['GET'])
def get_personal_info(select_sql=None):
    cursor = g.db.cursor()
    cursor.execute("SELECT * FROM personal_info WHERE id = 1")
    result = cursor.fetchone()
    cursor.close()

    if result:
        personal_info = {
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
            'emergencyContactPhone': result['emergency_contact_phone']
        }
    else:
        personal_info = {
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
            'emergencyContactPhone': ''
        }
    return jsonify(personal_info)


# 由前端调用自动更新
@app.route('/myapi/personal_info', methods=['PUT'])
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
                emergency_contact_phone=%s
            WHERE id = 1
        """
    print("Executing SQL:", sql)  # Print generated SQL

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
        data['emergencyContactPhone']
    ))
    g.db.commit()
    cursor.close()

    return jsonify({"message": "Personal info updated successfully"})


@app.route('/upload_avatar', methods=['POST'])
def upload_avatar():
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
        cursor.execute("""
            UPDATE personal_info SET
                avatar_url=%s
            WHERE id = 1
        """, (os.path.join(app.config['UPLOAD_IMAGE_FOLDER'], filename)))
        g.db.commit()
        cursor.close()
        return jsonify({"message": "Avatar uploaded successfully"}), 200
    else:
        return jsonify({"error": "Unsupported file type"}), 400


# -------------------------#


# 插入数据到 personal_info 表的函数
def insert_personal_info(db, data):
    cursor = db.cursor()
    sql = """
        INSERT INTO personal_info (
            username, phone, address, email, community_name, building_number,
            unit_number, door_number, parking_number, security_card_number,
            emergency_contact, emergency_contact_phone
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(sql, data)
    db.commit()
    cursor.close()


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
        myfile.save(os.path.join(app.config['UPLOAD_FILE_FOLDER'], filename))
        return jsonify({"message": "File uploaded successfully"}), 200
    else:
        return jsonify({"error": "Unsupported file type"}), 400


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
