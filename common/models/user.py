#项目用户建表模型
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db

class User(db.Model):
    __tablename__= 'user_basic'

    id=db.Column(db.Integer,primary_key=True,doc='用户id')
    mobile=db.Column(db.String(11),doc='用户手机号')
    name=db.Column(db.String(20),doc='用户昵称')
    last_login=db.Column(db.DateTime,doc='最后一次登录时间')
    introduction=db.Column(db.String(200),doc='用户简介')
    article_count=db.Column(db.Integer,default=0,doc='用户文章数量')
    following_count=db.Column(db.Integer,default=0,doc='用户关注数量')
    fans_count=db.Column(db.Integer,default=0,doc='用户粉丝数量')
    profile_photo=db.Column(db.String(200),doc='用户头像')

    def to_dict(self):
        return {
            'id':self.id,
            'name':self.name,
            'photo':self.mobile,
            'intro':self.introduction if self.introduction else '这个人很懒，什么都没有留下',
            'art_count':self.article_count,
            'follow_count':self.following_count,
            'fans_count':self.fans_count,
        }

class Relation(db.Model):
    __tablename__='user_relation'

    class RELATTON:
        DELETE=0
        FOLLOW=1
        BLACKLIST=2
    
    id=db.Column(db.Integer,primary_key=True,doc='主键id')
    user_id=db.Column(db.Integer,doc='用户id')
    author_id=db.Column(db.Integer,doc='作者id')
    relation=db.Column(db.Integer,doc='关系')
    updata_time=db.Column(db.DateTime,default=datetime.now,doc='更新时间')