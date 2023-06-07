from flask import Flask, request, jsonify
from flask import g  # g对象在请求上下文中存储数据库连接
import pymysql
import os
import sys
from routes import register_blueprints  # 使用蓝图blueprint改变的地方

# sys.path.append("C:/Users/likejie/AppData/Local/Programs/Python/Python39/Lib/site-packages")
from flask_cors import CORS

# Global Variables
# ----------------应用配置--------------------#
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)  # 解决跨域问题

app.config['UPLOAD_FILE_FOLDER'] = './uploads/files'  # 设置上传文件的文件夹路径
app.config['UPLOAD_IMAGE_FOLDER'] = './uploads/images'  # 设置上传图片的文件夹路径
app.config['ALLOWED_EXTENSIONS'] = {'xlsx', 'xls', 'csv', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'pdf'}  # 设置允许的文件类型

register_blueprints(app)  # 在Flask应用中注册自己写的蓝图

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


@app.route('/', methods=['GET', 'POST'])
def hello():
    return "Nice to see you again!"


if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FILE_FOLDER']):
        os.makedirs(app.config['UPLOAD_FILE_FOLDER'])  # 如果上传文件夹不存在，则创建
    if not os.path.exists(app.config['UPLOAD_IMAGE_FOLDER']):
        os.makedirs(app.config['UPLOAD_IMAGE_FOLDER'])

    app.run(debug=True)
