from flask import g
from common.models.news import Channel, UserChannel
from flask_restful import Resource
from sqlalchemy.orm import load_only
from common.utils.decorators import login_required

class UserChannelResource(Resource):
    method_decorators = {
        "get": [login_required]
    }
    def get(self):
        user_id = g.user_id
        is_refresh = g.is_refresh

        # 1. 获取用户关注的频道 / 默认频道
        if user_id and is_refresh == False:
            channels = Channel.query.options(load_only(Channel.id, Channel.name)) \
                .join(UserChannel, Channel.id == UserChannel.channel_id) \
                .filter(
                UserChannel.user_id == user_id,
                UserChannel.is_deleted == False
            ).order_by(UserChannel.sequence).all()

            if not channels:
                channels = Channel.query.options(load_only(Channel.id, Channel.name)) \
                    .filter(Channel.is_default == True).all()
        else:
            channels = Channel.query.options(load_only(Channel.id, Channel.name)) \
                .filter(Channel.is_default == True).all()

        # 2. 转成字典列表
        channel_list = [channel.to_dict() for channel in channels]

        has_recommend = any(ch.get("id") == 0 for ch in channel_list)

        # 如果没有推荐频道，才插入到第一个位置
        if not has_recommend:
            channel_list.insert(0, {
                "id": 0,
                "name": "推荐"
            })

        return {
            "channels": channel_list
        }