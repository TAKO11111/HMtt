#提取登录钩子的函数
from flask import request,current_app,g
from common.utils.jwt_util import verify

def get_userinfo():
    token=request.headers.get("Authorization")
    secret=current_app.config.get("JWT_SECRET")
    g.user_id=None
    g.is_refresh=False
    if token :
        try:
            payload=verify(token,secret)
        except Exception as e:
            payload=None
        if payload:
            g.user_id=payload.get("user_id")
            g.is_refresh=payload.get("is_refresh",False)
