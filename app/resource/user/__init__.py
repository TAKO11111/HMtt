#用户模块初始化
from flask import Blueprint
from flask_restful import Api
from common.utils.constants import APP_URL_PREFIX
from app.resource.user.passport import SHSCodeResource,LoginregisterResource
from common.utils.output import output_json
from app.resource.user.profile import CurrentUserResource,UserPhotoResource
#1.创建蓝图对象
user_bp=Blueprint('user_bp',__name__,url_prefix=APP_URL_PREFIX)

#2.创建api对象
user_api=Api(user_bp)
#3.添加资源类到api对象中
user_api.add_resource(SHSCodeResource,"/codes/<mobile:mobile>")
user_api.add_resource(LoginregisterResource,"/login")
user_api.add_resource(CurrentUserResource,"/user")
user_api.add_resource(UserPhotoResource,"/user/photo")
#4.注册蓝图对象到app工厂方法中(在app.init文件实现)
#5。给模块自定义返回json数据格式(在app.init文件实现)
""
{
    "message":"ok",
    "data":{},
}
""
user_api.representation(mediatype="application/json")(output_json)
