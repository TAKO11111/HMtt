from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from common.models.user import Relation, User
from sqlalchemy.orm import load_only
from app import db
from datetime import datetime
from flask import g
from common.utils.decorators import login_required


class UserFollowingResource(Resource):
    method_decorators={
        "post":[login_required],
        "get":[login_required]
    }
    #获取用户关注列表
    def get(self):
        parser = RequestParser()
        parser.add_argument('page', type=int, default=1, location='args')
        parser.add_argument('per_page', type=int, default=10, location='args')
        args = parser.parse_args()

        page = args['page']
        per_page = args['per_page']
        user_id = g.user_id  # 当前登录用户ID


        follow_query = User.query.options(
            load_only(User.id, User.name, User.fans_count, User.profile_photo)
        ).join(
            Relation, User.id == Relation.news_user_id
        ).filter(
            Relation.user_id == user_id,
            Relation.relation == Relation.RELATTON.FOLLOW
        ).order_by(
            Relation.updata_time.desc()
        )

        # 分页
        pagination = follow_query.paginate(page=page, per_page=per_page, error_out=False)
        follow_users = pagination.items


        fan_ids = db.session.query(Relation.user_id).filter(
            Relation.news_user_id == user_id,  # 我是被关注者
            Relation.relation == Relation.RELATTON.FOLLOW
        ).all()

        # 把粉丝ID转成集合，方便快速判断
        fan_id_set = {f[0] for f in fan_ids}

        # ======================
        # 步骤3：遍历 + 判断互相关注
        # ======================
        follow_list = []
        for user in follow_users:
            follow_list.append({
                "id": user.id,
                "name": user.name,
                "fans_count": user.fans_count,
                "profile_photo": user.profile_photo or "",
                "is_mutual_follow": user.id in fan_id_set
            })

        # 返回
            return {
            "page": page,
            "per_page": per_page,
            "total": pagination.total,
            "follows": follow_list
            }

    def post(self):
        # 1. 获取参数
        parser = RequestParser()
        parser.add_argument("target", required=True, type=int, location='json')
        ret = parser.parse_args()
        # 1.1 target 作者id
        author_id = ret["target"]
        # 1.2 user_id 当前登录的用户id
        user_id = g.user_id

        # 2. 参数校验（补充：不能关注自己）
        if user_id == author_id:
            return {"message": "不能关注自己"}, 400

        # 3. 逻辑处理
        # 3.1 根据user_id和author_id查询关注关系 —— 严格用 news_user_id
        relation_obj = Relation.query.options(load_only(Relation.id)) \
            .filter(Relation.user_id == user_id,
                    Relation.news_user_id == author_id).first()  # type: Relation

        # 3.2.关系对象存在：修改关系为:关注 修改关注时间
        if relation_obj is not None:
            # 1.修改关系为:关注
            relation_obj.relation = Relation.RELATTON.FOLLOW
            # 2.修改关注时间 —— 用你写的 updata_time
            relation_obj.updata_time = datetime.now()
            db.session.commit()

        # 3.3.关注对象不存在：新建关注对象添加到数据库
        else:
            relation_obj = Relation(
                user_id=user_id, 
                news_user_id=author_id, 
                relation=Relation.RELATTON.FOLLOW,
                updata_time=datetime.now()
            )
            db.session.add(relation_obj)
            db.session.commit()

            user = User.query.filter(User.id == user_id).first()
            if user:
                user.following_count += 1
                db.session.add(user)

            # 3.5 将当前作者的粉丝数量加一
            author = User.query.filter(User.id == author_id).first()
            if author:
                author.fans_count += 1
                db.session.add(author)

            # 统一提交事务
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return {"message":str(e)}
        
        # 4. 返回值处理
        return {"target":author_id,"message": "关注成功"}


class UserUnfollowingResource(Resource):
    method_decorators = {
        "post": [login_required]
    }

    def post(self,target):
        author_id = target
        user_id = g.user_id

        if user_id == author_id:
            return {"message": "不能取关自己"}, 400

        # 严格用 news_user_id
        relation_obj = Relation.query.options(load_only(Relation.id)) \
            .filter(
                Relation.user_id == user_id,
                Relation.news_user_id == author_id
            ).first()

        if not relation_obj:
            return {"message": "未关注该用户"}, 400

        try:
            if relation_obj.relation == Relation.RELATTON.FOLLOW:
                relation_obj.relation = Relation.RELATTON.DELETE
                relation_obj.updata_time = datetime.now()

                user = User.query.filter_by(id=user_id).first()
                if user:
                    user.following_count -= 1

                author = User.query.filter_by(id=author_id).first()
                if author:
                    author.fans_count -= 1

            db.session.commit()

        except Exception as e:
            db.session.rollback()
            return {"message": "取消关注失败：" + str(e)}, 500

        return {"target": author_id, "message": "取消关注成功"}, 200