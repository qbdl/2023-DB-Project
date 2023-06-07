from flask import Flask
from .login import login_blueprint
from .user import user_blueprint
from .upload import upload_blueprint
from .announcement import announcement_blueprint


# 将蓝图注册到Flask 应用中
def register_blueprints(app: Flask):
    app.register_blueprint(login_blueprint, url_prefix='')
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(upload_blueprint, url_prefix='/upload')
    app.register_blueprint(announcement_blueprint, url_prefix='/announce')
