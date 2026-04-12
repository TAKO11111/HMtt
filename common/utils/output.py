#对返回的json数据进行统一格式处理
from flask import current_app, request, make_response
from json import dumps
from sys import version_info
from sys import version_info
PY3 = version_info.major >= 3
def output_json(data,code,headers=None):
    if str(code)=='400':
        current_app.logger.warn(request.headers)
        current_app.logger.warn(request.data)
        current_app.logger.warn(str(data))
    if 'message' not in data:
        data={
            'message':'ok',
            'data':data
        }
    settings=current_app.config.get('RESTFUL_JSON',{})
    if current_app.debug:
        settings.setdefault('indent',4)
        settings.setdefault('sort_keys',not PY3)

    dumped=dumps(data,**settings)

    resp=make_response(dumped,code)
    resp.headers.extend(headers or {})
    return resp
