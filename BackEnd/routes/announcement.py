# ------------------安防公告部分-------------------------------------#
from flask import Blueprint, request, jsonify, g

# 创建一个名为 'announcement' 的蓝图
announcement_blueprint = Blueprint('announcement',__name__)


# 接受安防公告
@announcement_blueprint.route('/receive_announcements', methods=['GET'])
def get_announcements():
    cursor = g.db.cursor()
    cursor.execute("SELECT * FROM security_announcements")
    announcements = cursor.fetchall()
    cursor.close()
    return jsonify(announcements)


# 发布安防公告
@announcement_blueprint.route('/create_announcement', methods=['POST'])
def create_announcement():
    announcement = request.json
    id = announcement['id']
    title = announcement['title']
    date = announcement['date']
    author = announcement['author']
    author_id=announcement['author_id']
    status = announcement['status']
    content = announcement['content']

    cursor = g.db.cursor()
    cursor.execute(
        "INSERT INTO security_announcements (id, title, date, author, author_id,status, content) VALUES (%s, %s, %s,%s, %s, %s, %s)",
        (id, title, date, author,author_id, status, content))
    g.db.commit()

    return jsonify({"message": "Announcement created successfully"}), 200
