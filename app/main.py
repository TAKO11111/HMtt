#启动文件
from app import create_app
from flask import jsonify
import os
os.environ['FLASK_ENV'] = 'production'
app=create_app('dev')

@app.route('/')
def index():
    #返回所有路由信息   
    route_dict={rule.rule:rule.endpoint for rule in app.url_map.iter_rules()}
    return jsonify(route_dict)
if __name__ == '__main__':
    app.run()