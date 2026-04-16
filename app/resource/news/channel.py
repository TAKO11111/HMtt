#频道接口类试图
from flask_restful import Resource
from common.models.news import Channel,UserChannel
from sqlalchemy.orm import load_only
from flask import g
from common.utils.decorators import login_required
from flask import request
from sqlalchemy.orm import load_only
from app import db

class AllChannelResource(Resource):
    #获取所有频道接口 
    method_decorators={
        "put":[login_required]
    }
    def get(self):
        channels=Channel.query.options(load_only(Channel.id,Channel.name)).all()
        channel_dict_list=[channel.to_dict() for channel in channels]
        return {
            "channels":channel_dict_list
        }
    #更新频道接口
    def put(self):
        user_id=g.user_id
        #1.获取参数 
        #规定传进来的格式为{"id":1,"seq":1}
        channels=request.json.get("channels")
        # 2.校验参数 
        if not channels:
            return {"message":"参数错误"},400
        # 3.逻辑处理 
        #将用户之前的频道设置为删除状态，进行重置化修改
        UserChannel.query.filter(UserChannel.user_id==user_id , UserChannel.is_deleted==False).update({"is_deleted":True})
        for channel in channels:
            user_channels=UserChannel.query.options(load_only(UserChannel.id)).filter(UserChannel.user_id==user_id , UserChannel.channel_id==channel.get("id")).first()
            if user_channels:
                user_channels.is_deleted=False
                user_channels.sequence=channel.get("seq")
            else:
                user_channel=UserChannel(user_id=user_id,channel_id=channel.get("id"),sequence=channel.get("seq"))
                db.session.add(user_channel)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}

        # 4.返回结果处理
        return {"channels":channels,"message":"ok"}