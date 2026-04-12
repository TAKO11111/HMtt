#项目配置文件
from flask_sqlalchemy import SQLAlchemy
class DefaultConfig(object):
    """ 项目默认配置"""
    SECRET_KEY = "python38"

    #防止flask——restful模块返回json数据时中文乱码问题
    RESTFUL_JSON ={"ensure_ascii":False}
    """mysql链接配置"""
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost:3306/flasktop"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    """redis链接配置"""
    REDIS_HOST ="localhost"
    REDIS_PORT = 6379
    REDIS_DB = 0
    REDIS_PASSWORD = None
    "JWT配置"
    JWT_SECRET = "927f6c8e5d37b4a9018f7e2d51c63b0a7e8d2f9c6104a3b5782e1d6c9f0a587b"
    JWT_LOGIN_EXPIRE = 2
    JWT_REFRESH_EXPIRE = 14
    #云储存配置
    QINIU_AK = "HypkNoXIEUk6v8X9YYgMgW6etJABthObi-STfpdO"
    QINIU_SK = "BCyjpYBcg8ZJWsBXy0H6UH53l9_FnoWIEF0WLGAT"
    QINIU_BN = "takotoutiao"
    QINIU_CDN = "http://tde0isbgq.hn-bkt.clouddn.com/"
class DevelopmentConfig(DefaultConfig):
    """ 开发环境配置"""
    DEBUG = True 




       
class ProductionConfig(DefaultConfig):
    """ 生产环境配置"""
    DEBUG = False   


#外界调用暴露字典接口
config_dict={
    "dev":DevelopmentConfig,
    "pro":ProductionConfig,
}