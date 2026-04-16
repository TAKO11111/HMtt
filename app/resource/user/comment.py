from flask_restful import Resource
from flask_restful.reqparse import RequestParser  
from common.models.news import News,Comment  
from common.models.user import User
from app import db
from flask import g
from common.utils.decorators import login_required
from datetime import datetime


class CommentResource(Resource):
    method_decorators = {
        "post":[login_required] ,
    }
    def get(self):
        # 1. 获取参数
        parser = RequestParser()
        parser.add_argument("offset", type=int, location='args', default=0)
        parser.add_argument("limit", type=int, location='args', default=10)
        parser.add_argument("source", type=int, location='args', required=True)
        ret = parser.parse_args()

        offset = ret["offset"]
        limit = ret["limit"]
        source = ret["source"]  # 文章 id

        # 2. 校验
        if limit < 1 or limit > 50:
            return {"message": "limit必须在1-50之间"}, 400
        if offset < 0:
            return {"message": "offset不能为负数"}, 400

        # 3. 核心查询（严格按你的模型）
        query = db.session.query(
            Comment.id,
            Comment.content,
            Comment.ctime,        
            Comment.like_count,   
            Comment.reply_count,  
            User.id.label("user_id"),
            User.name,
            User.profile_photo
        ).join(
            User, Comment.user_id == User.id  
        ).filter(
            Comment.news_id == source,
            Comment.parent_id == 0  
        ).order_by(
            Comment.ctime.desc()   
        ).offset(offset).limit(limit)

        comment_list = query.all()

        # 4. 字典格式化
        comments = []
        for item in comment_list:
            comments.append({
                "comment_id": item.id,
                "content": item.content,
                "ctime": item.ctime.strftime("%Y-%m-%d %H:%M:%S"),
                "like_count": item.like_count,
                "reply_count": item.reply_count,
                "user": {
                    "user_id": item.user_id,
                    "name": item.name,
                    "avatar": item.profile_photo or ""
                }
            })

        # 5. 分页信息
        last_id = comment_list[-1].id if comment_list else 0
        total_count = Comment.query.filter_by(news_id=source, parent_id=0).count()
        last_comment = Comment.query.filter_by(news_id=source, parent_id=0).order_by(Comment.ctime.desc()).first()
        end_id = last_comment.id if last_comment else 0

        # 6. 返回
        return {
            "comments": comments,
            "last_id": last_id,
            "end_id": end_id,
            "total": total_count,
            "offset": offset,
            "limit": limit,
            "source": source
        }
    def post(self):
        # 1. 获取参数
        parser = RequestParser()
        # 1.1 user_id 用户id (从g获取，无需传参)
        # 1.2 target 文章id
        parser.add_argument("target", type=int, required=True, location='json')
        # 1.3 content 评论内容
        parser.add_argument("content", type=str, required=True, location='json')
        ret = parser.parse_args()

        user_id = g.user_id
        news_id = ret["target"]
        comment_content = ret["content"]

        # 2. 逻辑处理
        # 2.1 新建评论对象 [主评论 parent_id = 0]
        comment = Comment(
            user_id=user_id,
            news_id=news_id,
            content=comment_content,
            parent_id=0
        )
        db.session.add(comment)

        # 2.2 根据文章id查询文章对象并更新评论数量
        # 写法: comment_count = comment_count + 1
        News.query.filter(News.id == news_id).update(
            {"comment_count": News.comment_count + 1}
        )

        # 3. 提交事务
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"message": "发布评论提交数据库异常: {}".format(e)}, 500

        # 4. 返回值 (包含评论id 或 成功提示)
        return {
            "message": "评论发布成功",
            "comment_id": comment.id,
            "traget":news_id
        }
    
class ChildCommentResource(Resource):
    method_decorators = {
        "post": [login_required],  # 发布子评论
    }


    def post(self):
        parser = RequestParser()
        parser.add_argument("target", type=int, required=True, location='json')      # 文章ID
        parser.add_argument("parent_id", type=int, required=True, location='json') # 父评论ID
        parser.add_argument("content", type=str, required=True, location='json')  # 评论内容
        ret = parser.parse_args()

        user_id = g.user_id
        news_id = ret["target"]
        parent_id = ret["parent_id"]
        content = ret["content"]

        # 新建子评论
        child_comment = Comment(
            user_id=user_id,
            news_id=news_id,
            parent_id=parent_id,  # 关键：绑定父评论
            content=content,
            ctime=datetime.now()
        )
        db.session.add(child_comment)

        # 父评论的回复数 +1（你的模型字段）
        Comment.query.filter_by(id=parent_id).update({"reply_count": Comment.reply_count + 1})

        # 文章总评论数 +1
        News.query.filter_by(id=news_id).update({"comment_count": News.comment_count + 1})

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"message": "回复失败"}, 500

        return {
            "message": "回复成功",
            "comment_id": child_comment.id,
            "parent_id": parent_id
        }


    def get(self):
        parser = RequestParser()
        parser.add_argument("parent_id", type=int, required=True, location='args')  # 父评论ID
        parser.add_argument("offset", type=int, default=0, location='args')
        parser.add_argument("limit", type=int, default=10, location='args')
        ret = parser.parse_args()

        parent_id = ret["parent_id"]
        offset = ret["offset"]
        limit = ret["limit"]

        # 查询子评论
        query = db.session.query(
            Comment.id,
            Comment.content,
            Comment.ctime,
            Comment.like_count,
            User.id.label("user_id"),
            User.name,
            User.profile_photo
        ).join(User, Comment.user_id == User.id
        ).filter(Comment.parent_id == parent_id
        ).order_by(Comment.ctime.asc()  # 子评论按时间正序
        ).offset(offset).limit(limit)

        child_list = query.all()
        child_comments = []
        for item in child_list:
            child_comments.append({
                "comment_id": item.id,
                "content": item.content,
                "ctime": item.ctime.strftime("%Y-%m-%d %H:%M:%S"),
                "like_count": item.like_count,
                "user": {
                    "user_id": item.user_id,
                    "name": item.name,
                    "avatar": item.profile_photo or ""
                }
            })

        total = Comment.query.filter_by(parent_id=parent_id).count()

        return {
            "parent_id": parent_id,
            "child_comments": child_comments,
            "total": total
        }