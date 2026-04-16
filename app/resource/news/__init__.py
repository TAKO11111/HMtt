#文章蓝图创建
from flask import Blueprint
from flask_restful import Api
from common.utils.constants import NEWS_URL_PREFIX,APP_URL_PREFIX
from common.utils.output import output_json
from app.resource.news.channel import AllChannelResource
from app.resource.news.news import NewsListResource,NewsDetailResource

#1.创建蓝图对象
news_bp=Blueprint('news_bp',__name__,url_prefix=APP_URL_PREFIX+NEWS_URL_PREFIX)

#2.创建api对象
news_api=Api(news_bp)
#3.添加资源类到api对象中
news_api.add_resource(AllChannelResource,"/channels")
news_api.add_resource(NewsListResource,"")
news_api.add_resource(NewsDetailResource,"/<int:news_id>")

#4.注册蓝图对象到app工厂方法中(在app.init文件实现)
#5。给模块自定义返回json数据格式(在app.init文件实现)
""
{
    "message":"ok",
    "data":{},
}
""
news_api.representation(mediatype="application/json")(output_json)