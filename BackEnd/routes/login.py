# -----------------登陆登出部分-----------------#
# TODO:这里没有做数据库的登录，直接返回成功了
from flask import Blueprint, g
import json

# 创建一个名为 'login' 的蓝图
login_blueprint = Blueprint('login', __name__)


# 登录
@login_blueprint.route('/login', methods=['POST'])
def login():
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
