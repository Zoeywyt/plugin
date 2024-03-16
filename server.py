#!/usr/env python3
# -*- coding: UTF-8 -*-

from flask import Flask, request, send_file, make_response
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://agents.baidu.com"}})

activitylist = []

def make_json_response(data, status_code=200):
    response = make_response(json.dumps(data), status_code)
    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/add_activity", methods=['POST'])
async def add_activity():
    """
        添加一个活动
    """
    activity = request.json.get('activity', "")
    activitylist.append(activity)
    return make_json_response({"message": "活动添加成功"})


@app.route("/delete_activity", methods=['DELETE'])
async def delete_activity():
    """
        删除一个活动
    """
    activity = request.json.get('activity', "")
    if activity in activitylist:
        activitylist.remove(activity)
    return make_json_response({"message": "活动删除成功"})


@app.route("/get_activitylist")
async def get_activitylist():
    """
        获得活动列表
    """
    return make_json_response({"activitylist": activitylist})


@app.route("/generate_activities", methods=['POST'])
async def generate_activities():
    """
        生成活动
    """
    character = request.get_json()['character']
    mood = request.get_json()['mood']
    number = request.get_json()['activity_number']
    prompt = "根据用户性格{character}和心情{mood}推荐符合该用户性格和心情的相应数量{number}的活动{activititylist}，要求这些活动内容推荐听的音乐，适合吃的食物，可以读的书籍和观看的电影，推荐穿的衣服颜色等类似个性化活动，以列表的形式打印出,请注意要符合用户的mbti性格特点和心情个性化推荐具体著名的书籍电影和适合的活动"
    # API返回字段"prompt"有特殊含义：开发者可以通过调试它来调试输出效果
    return make_json_response({"character":character,"mood":mood,"number":number,  "prompt": prompt})


@app.route("/logo.png")
async def plugin_logo():
    """
        注册用的：返回插件的 logo，要求 48 x 48 大小的 png 文件.
        注意：API路由是固定的，事先约定的。
    """
    return send_file('logo.png', mimetype='image/png')


@app.route("/.well-known/ai-plugin.json")
async def plugin_manifest():
    """
        注册用的：返回插件的描述文件，描述了插件是什么等信息。
        注意：API 路由是固定的，事先约定的。
    """
    host = request.host_url
    with open("plugin/.well-known/ai-plugin.json", encoding="utf-8") as f:
        text = f.read().replace("PLUGIN_HOST", host)
        return text, 200, {"Content-Type": "application/json"}


@app.route("/.well-known/openapi.yaml")
async def openapi_spec():
    """
        注册用的：返回插件所依赖的插件服务的API接口描述，参照 openapi 规范编写。
        注意：API 路由是固定的，事先约定的。
    """
    with open("plugin/.well-known/openapi.yaml", encoding="utf-8") as f:
        text = f.read()
        return text, 200, {"Content-Type": "text/yaml"}

@app.route("/example.yaml")
async def exampleSpec():
    with open("plugin/example.yaml") as f:
        text = f.read()
        return text, 200, {"Content-Type": "text/yaml"}



@app.route('/')
def index():
    return 'welcome to my plugin!'

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8081)