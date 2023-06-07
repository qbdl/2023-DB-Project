# -----------------登陆登出部分-----------------#
from flask import Blueprint, request, g
import json

# 创建一个名为 'login' 的蓝图
login_blueprint = Blueprint('login', __name__)


# 登录
@login_blueprint.route('/login', methods=['POST'])
def login():
    # request.json.get针对获取POST数据
    print(request.json)
    username = request.json.get('username')  # 获取username参数
    password = request.json.get('password')  # 获取password参数
    print(username, password)
    query = """
        SELECT password
        FROM personal_info
        WHERE username=%s
    """
    cursor = g.db.cursor()
    cursor.execute(query, (username,))  # 首先执行查询
    get_password = cursor.fetchone()  # 然后获取查询结果
    cursor.close()
    print("get_password:", get_password)
    if get_password is not None:
        get_password = get_password['password']
    if get_password == '' or get_password != password:
        info = {"code": 500, "data": {"access_token": ""}, "msg": "用户名或密码错误"}
    else:
        info = {"code": 200, "data": {"access_token": "bqddxxwqmfncffacvbpkuxvwvqrhln"}, "msg": "成功"}
    return json.dumps(info)


# 登录的按钮
@login_blueprint.route('/auth/buttons', methods=['GET'])
def buttons():
    info = {"code": 200, "msg": "成功", "data": {"useProTable": ["add", "batchAdd", "export", "batchDelete", "status"],
                                               "authButton": ["add", "edit", "delete", "import", "export"]}}
    return json.dumps(info)


# 登出
@login_blueprint.route('/logout', methods=['POST'])
def logout():
    info = {"code": 200, "msg": "成功"}
    return json.dumps(info)
