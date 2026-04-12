#用户模块的相关接口
from flask_restful import Resource
import random
from app import appRedis
from common.utils.constants import SMS_CODE_RXPIRE
from flask_restful.reqparse import RequestParser
from flask_restful.inputs import *
from common.utils import parser as type_parser
from common.models.user import User
from app import db
from sqlalchemy.orm import load_only
from datetime import datetime,timezone,timedelta
from common.utils.jwt_util import generate_jwt
from flask import current_app,g
class SHSCodeResource(Resource):
    #发送短信验证码视图类
    def get(self,mobile):
        #生成短信验证码
       random_code="%06d"%random.randint(0,999999)
       key="app:code:{}".format(mobile)
       appRedis.setex(name=key,time=SMS_CODE_RXPIRE,value=random_code)
       print("发送短信验证码成功 手机号码{} 验证码{}".format(mobile,random_code))
       return {"mobile":mobile,"code":random_code}
    
class LoginregisterResource(Resource):
    #登录注册视图
    def _generate_jwt_token(self,user_id):
        #生成2小时登录token
        login_payload={
            "user_id":user_id,
            "is_refresh":False
        }
        exp2h=datetime.now(timezone.utc)+timedelta(hours=current_app.config.get("JWT_LOGIN_EXPIRE"))
        secret=current_app.config.get("JWT_SECRET")
        login_token=generate_jwt(payload=login_payload,expiry=exp2h,secret=secret)
        #生成14天刷新token
        refresh_payload={
            "user_id":user_id,
            "is_refresh":True
            }
        exp14d=datetime.now(timezone.utc)+timedelta(days=current_app.config.get("JWT_REFRESH_EXPIRE"))
        refresh_token=generate_jwt(payload=refresh_payload,expiry=exp14d,secret=secret)
        return login_token,refresh_token
    
    #1.获取参数 2.校验参数 3.查询数据库 4.返回结果处理
    #重点三：根据手机号拼接短信验证码去redis查询真是验证码
    #根据手机号查询用户是否存在，做出相应操作
    def post(self):
        #参数解析校验
        parser=RequestParser()
        parser.add_argument("mobile",required=True,location="json",type=type_parser.mobile)
        parser.add_argument("code",required=True,location="json")
        ret=parser.parse_args()
        mobile=ret["mobile"]
        code=ret["code"]
        #逻辑处理
        key="app:code:{}".format(mobile)
        real_code=appRedis.get(key)
        if real_code is None or real_code !=code:
            return {"message":"验证码错误"},400
        #查询数据库
        user=User.query.options(load_only(User.id)).filter(User.mobile==mobile).first()
        #如果用户不存在，注册用户
        if user is None:
            user=User(name=mobile,mobile=mobile,last_login=datetime.now())
            db.session.add(user)
        #如果用户存在，登录成功
        else:
             user.last_login=datetime.now()
        #操作数据库
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"message":e},507
        #生成token
        login_token,refresh_token=self._generate_jwt_token(user.id)
        return {"login_token":login_token,"refresh_token":refresh_token}
    #刷新token函数
    def put(self):
        user_id=g.user_id
        if user_id and g.is_refresh ==True:
            login_token,_= self._generate_jwt_token(user_id)
            return {"login_token":login_token}
        else:
            return {"message":"无效的刷新token"},403


