#对手机格式的验证
from werkzeug.routing import BaseConverter
class MobileConverter(BaseConverter):
    regex = r'1[3-9]\d{9}'
def register_converters(app):
    app.url_map.converters['mobile'] = MobileConverter