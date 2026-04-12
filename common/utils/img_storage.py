#上传图片函数
from qiniu import Auth, put_file,etag,put_data
from flask import current_app
def upload_img(data):
    #构建鉴权对象
    q = Auth(current_app.config.get("QINIU_AK"),current_app.config.get("QINIU_SK"))
    #要上传的空间
    bucket_name = current_app.config.get("QINIU_BN")
    #上传后保存的文件名，若为“”则使用默认文件名
    key = None
    #生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)
    #要上传文件的本地路径
    ret,info=put_data(token,key,data)
    if info.status_code == 200:
        return current_app.config.get("QINIU_CDN")+ret.get("key")
    else:
        raise Exception("上传图片失败")