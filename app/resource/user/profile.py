#操作用户信息接口
from flask_restful import Resource
from common.utils.decorators import logina_required
from common.models.user import User
from sqlalchemy.orm import load_only
from flask import g
from flask_restful.reqparse import RequestParser
from common.utils.parser import img_type
from common.utils.img_storage import upload_img  
from app import db


class CurrentUserResource(Resource):
#获取当前用户信息
    method_decorators={
        "get":[logina_required]
    }
    def get(self):
        user_id=g.user_id
        user=User.query.options(load_only(User.id,
                                          User.name,
                                          User.mobile,
                                          User.profile_photo,
                                          User.introduction,
                                          User.article_count,
                                          User.following_count,
                                          User.fans_count)).filter(User.id==user_id).first()
        if user:
            return user.to_dict()

class UserPhotoResource(Resource):
    #更新用户头像接口
    method_decorators={
        "patch":[logina_required]
    }
    def patch(self):
        #获取参数
        parser=RequestParser()
        parser.add_argument("photo",required=True,location="files",type=img_type)
        ret=parser.parse_args()
        photo_file=ret["photo"]
        user_id=g.user_id
        #上传图片到云储存，获取图片url
        photo_data=photo_file.read()
        try:
            full_url=upload_img(photo_data)
        except Exception as e:
            return {"message": "出现错误"}.format(e)
        #更新用户头像
        User.query.filter(User.id==user_id).update({"profile_photo":full_url})
        try:  
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"message": "出现错误"}.format(e)
        return {"photo_url":full_url}
