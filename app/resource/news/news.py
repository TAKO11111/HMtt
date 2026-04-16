from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from common.models.news import News,NewsContent,Collection,Attitude
from common.models.user import User,Relation
from sqlalchemy.orm import load_only
from app import db
from datetime import datetime
from flask import g
#频道文章列表接口

class NewsListResource(Resource):

    def get(self):
        #获取参数
        parser=RequestParser()
        parser.add_argument("channel_id",type=int,required=True,location="args")
        parser.add_argument("timestamp",type=int,required=True,location="args")
        parser.add_argument("per_page",type=int,default=20,location="args")
        ret=parser.parse_args()
        #对参数进行处理
        timestamp=ret["timestamp"]
        channel_id=ret["channel_id"]
        per_page=ret["per_page"]
        data=datetime.fromtimestamp(timestamp/1000) 
        #进行逻辑处理
        if channel_id==0:
            return {"results":[],"per_page":0}

        new_list=db.session.query(News.id,News.title,News.user_id,News.ctime,News.comment_count,News.cover,User.name)\
            .join(User,News.user_id==User.id)\
                .filter(News.channel_id==channel_id,News.ctime<data,News.status==News.STATUS.APPROVED)\
                 .order_by(News.ctime.desc()).limit(per_page).all()

        new_dict=[{
            "id":item.id,
            "title":item.title,
            "user_id":item.user_id,
            "ctime":item.ctime.isoformat(),
            "comment_count":item.comment_count,
            "cover":item.cover,
            "user_name":item.name
        } for item in new_list]

        pre_timestamp=int(new_list[-1].ctime.timestamp())*1000 if new_list else 0

        return {"results":new_dict,"pre_timestamp":pre_timestamp,"per_page":per_page}


#文章详情信息接口
class NewsDetailResource(Resource):
    def get(self,news_id):
        user_id=g.user_id
        is_refresh=g.is_refresh
        news=db.session.query(News.id,News.title,News.user_id,News.ctime,User.profile_photo,NewsContent.content)\
            .join(User,News.user_id==User.id)\
            .join(NewsContent,News.id==NewsContent.news_id)\
            .filter(News.id==news_id,News.status==News.STATUS.APPROVED).first()
        news_dict={
            "id":news.id,
            "title":news.title,
            "user_id":news.user_id,
            "ctime":news.ctime.isoformat(),
            "profile_photo":news.profile_photo,
            "content":news.content,
            "is_followed":False,
            "attitude":-1,
            "is_collected":False
        }
        news_user_id=news.user_id

        if user_id and is_refresh==False:
            relation=Relation.query.options(load_only(Relation.id)).filter(Relation.news_user_id==news_user_id,Relation.user_id==user_id,Relation.relation==Relation.RELATION.FOLLOW).first()
            news_dict["is_followed"]=True if relation else False
            collection=Collection.query.options(load_only(Collection.id)).filter(Collection.user_id==user_id,Collection.news_id==news_id,Collection.is_deleted==False).first()
            news_dict["is_collected"]=True if collection else False
            like=Attitude.query.options(load_only(Attitude.attitude)).filter(Attitude.user_id==user_id,Attitude.news_id==news_id).first()
            news_dict["attitude"]=like.attitude if like else -1
        return news_dict