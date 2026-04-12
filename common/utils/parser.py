#对信息格式的验证
import re
import imghdr
def email(email_str):
    if re.match(r'^[A-Za-z0-9_\-\.\u4e00-\u9fa5]+@([A-Za-z0-9_\-|.]+\.([A-Za-z]{2,8}))$',email_str):
        return email_str
    else:
        raise ValueError("邮箱格式不正确")
def mobile(mobile_str):
    if re.match(r'^1[3-9]\d{9}$',mobile_str):
        return mobile_str
    else:
        raise ValueError("手机号格式不正确")
def id_number(value):
    if re.match(r'^[1-9]\d{5}(18|19|20)\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$',value):
        return value
    else:
        raise ValueError("身份证号码格式不正确")
def img_type(value):
    try:
        typpe=imghdr.what(value)
    except Exception as e:
        raise ValueError("e")
    else:
        if type:
            return value
        else:
            raise ValueError("图片格式不正确")

        
    
