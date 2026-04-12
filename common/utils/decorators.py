# 强制装饰器
import functools
from  flask import g
def logina_required(view_func):
    @functools.wraps(view_func)
    def wrapper(*args,**kwargs):
        user_id=g.user_id
        is_refresh=g.is_refresh
        if user_id is None:
            return {"message":"请登录"},401
        elif user_id and is_refresh ==True:          
            return {"message":"请获取新的登录token重新登录"},403
        else:
            return view_func(*args,**kwargs)
    return wrapper