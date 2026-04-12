#项目初始化文件
from flask import Flask 
from app.settings.config import config_dict
from common.utils import constants
import os,sys
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from common.utils.converters import register_converters
from flask_migrate import Migrate

#项目路径D:\flaskproject
BASE_PATH =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0,os.path.join(BASE_PATH,'common'))

#暴露db对象
db=SQLAlchemy()
appRedis=None #type:StrictRedis
#内部创建app工厂方法
def create_flask_app(config_type):
    app = Flask(__name__)    
    register_converters(app)
    app.config.from_object(config_dict.get(config_type))
    app.config.from_envvar(constants.EXTRA_ENV_CONFIG,silent=True)
    return app

#外部调用生成app工厂方法
def create_app(config_type):
    app = create_flask_app(config_type)
    #注册扩展组件
    register_extensions(app)
    #注册蓝图组件
    register_blueprints(app)
    return app

#注册扩展组件函数  
def register_extensions(app:Flask):
    db.init_app(app)
    global appRedis
    appRedis=StrictRedis(host=app.config.get("REDIS_HOST"),
                         port=app.config.get("REDIS_PORT"),
                         db=app.config.get("REDIS_DB"),
                         password=app.config.get("REDIS_PASSWORD"),
                         decode_responses=True)
    Migrate(app,db)
    from common.models import user

    #添加请求钩子
    from common.utils.midd import get_userinfo
    app.before_request(get_userinfo)
       
#注册蓝图组件函数
def register_blueprints(app:Flask):
    from app.resource.user import user_bp
    app.register_blueprint(user_bp)