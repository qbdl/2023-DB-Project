# -----------------个人信息(业主信息）管理部分-----------------#
from flask import Blueprint, request, jsonify, g
from datetime import datetime, date
import json

# 创建一个名为 'user' 的蓝图
user_blueprint = Blueprint('user', __name__)


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
        personal_info = {}

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


@user_blueprint.route('/info', methods=['GET'])
def get_personal_info():
    # request.args.get针对获取GET数据

    # is_owner = request.args.get('is_owner', 0, type=int)
    # print(is_owner)
    owner_id = request.args.get('owner_id', None, type=int)  # 获取owner_id参数
    print(owner_id)

    if owner_id is None:
        print("no owner_id!")
        owner_id = 1  # TODO:get_current_logged_in_user_id()
    return get_personal_info_by_id(owner_id)


# ----------------业主信息管理——获取所有业主用户名-----------------#
@user_blueprint.route('/owners', methods=['GET'])
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
@user_blueprint.route('/info_update', methods=['PUT'])
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
        data['idCard'],
    ))
    g.db.commit()
    cursor.close()

    return jsonify({"message": "Personal info updated successfully"})


# -----------------车辆信息部分----------------------#


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


@user_blueprint.route('/list', methods=['POST'])
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


# @user_blueprint.route('/user/gender', methods=['GET'])
# def gender():
#     info = {"code": 200, "data": [{"genderLabel": "男", "genderValue": 1}, {"genderLabel": "女", "genderValue": 2}],
#             "msg": "成功"}
#     return json.dumps(info)


@user_blueprint.route('/status', methods=['GET'])
def status():
    info = {"code": 200, "data": [{"userLabel": "启用", "userStatus": 1}, {"userLabel": "禁用", "userStatus": 0}],
            "msg": "成功"}
    return json.dumps(info)
