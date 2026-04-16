#启动文件
from app import create_app
from flask import jsonify
import os
from flask import Blueprint, render_template

resume_bp = Blueprint('resume', __name__)

@resume_bp.route('/resume')
def show_resume():
    return render_template('resume.html')
os.environ['FLASK_ENV'] = 'production'
app=create_app('dev')

@app.route('/')
def index():
    #返回所有路由信息   
    route_dict={rule.rule:rule.endpoint for rule in app.url_map.iter_rules()}
    return jsonify(route_dict)

# ====================== 只添加这一段 ======================
# 简历页面
@app.route('/resume')
def resume():
    return render_template('resume.html')
# ==========================================================

if __name__ == '__main__':
    app.run()