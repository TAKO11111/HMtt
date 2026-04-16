#文章模块
from datetime import datetime
from app import db
class Channel(db.Model):
    #频道表
    __tablename__="new_channel"

    id=db.Column(db.Integer,primary_key=True,doc='频道id')
    name=db.Column(db.String(20),doc='频道名称')
    is_default=db.Column(db.Boolean,default=False,doc='是否默认频道')

    def to_dict(self):
        return {
            'id':self.id,
            'name':self.name
        }
    

class UserChannel(db.Model):
    #用户收藏频道表
    __tablename__="user_channel"

    id=db.Column(db.Integer,primary_key=True,doc='主键id')
    user_id=db.Column(db.Integer,doc='用户id')
    channel_id=db.Column(db.Integer,doc='频道id')
    sequence=db.Column(db.Integer,doc='频道序号')
    is_deleted=db.Column(db.Boolean,default=False,doc='是否删除')

class News(db.Model):
    #文章表
    __tablename__="news_basic"

    class STATUS:
        DRAFT=0   #草稿
        UNREVIEWED=1  #待审核
        APPROVED=2  #已通过
        FAILED=3  #已拒绝
        DELETED=4  #已删除
        BANNED=5  #已封禁

    id=db.Column(db.Integer,primary_key=True,doc='文章id')
    user_id=db.Column(db.Integer,doc='用户id')
    channel_id=db.Column(db.Integer,doc='频道id')
    title=db.Column(db.String(200),doc='文章标题')
    cover=db.Column(db.JSON,doc='文章封面')
    ctime=db.Column(db.DateTime,default=datetime.now,doc='创建时间')
    status=db.Column(db.Integer,default=0,doc='文章状态')
    comment_count=db.Column(db.Integer,default=0,doc='文章评论数量')

class NewsContent(db.Model):
    #文章内容表
    __tablename__="news_content"

    news_id=db.Column(db.Integer,primary_key=True,doc='文章id')
    content=db.Column(db.Text,doc='文章内容')

class Attitude(db.Model):
    #文章态度表
    __tablename__="news_attitude"

    class ATTITUDE:
        DILIKE=0 #不喜欢
        LIKING=1 #喜欢
        DELETE=-1 #无态度

    id=db.Column(db.Integer,primary_key=True,doc='主键id')
    user_id=db.Column(db.Integer,doc='用户id')
    news_id=db.Column(db.Integer,doc='文章id')
    attitude=db.Column(db.Integer,doc='态度')

class Collection(db.Model):
    #文章收藏表
    __tablename__="news_collection"

    id=db.Column(db.Integer,primary_key=True,doc='主键id')
    user_id=db.Column(db.Integer,doc='用户id')
    news_id=db.Column(db.Integer,doc='文章id')
    is_deleted=db.Column(db.Boolean,default=False,doc='是否删除')

class Comment(db.Model):
    #文章评论表
    __tablename__="news_comment"

    id=db.Column(db.Integer,primary_key=True,doc='评论id')
    user_id=db.Column(db.Integer,doc='用户id')
    news_id=db.Column(db.Integer,doc='文章id')
    parent_id=db.Column(db.Integer,default=0,doc='被评论id')
    reply_count=db.Column(db.Integer,default=0,doc='回复数量')
    content=db.Column(db.String(200),doc='评论内容')
    ctime=db.Column(db.DateTime,default=datetime.now,doc='评论时间')
    like_count=db.Column(db.Integer,default=0,doc='点赞数量')

