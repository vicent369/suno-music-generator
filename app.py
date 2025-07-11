from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv
import traceback
import socket

# 加载环境变量
load_dotenv()
SUNO_API_KEY = os.getenv('SUNO_API_KEY')

if not SUNO_API_KEY:
    raise ValueError("未检测到有效的SUNO_API_KEY，请检查.env文件")

app = Flask(__name__)

# 添加WSGI入口点，用于Vercel部署
app.debug = False

# 确保在Vercel环境中也能正常工作
if __name__ == '__main__':
    # 获取环境变量中的端口，用于生产环境部署
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

# 首页路由
@app.route('/')
def index():
    return render_template('index.html')

# 音乐生成API
@app.route('/api/generate', methods=['POST'])
def generate_music():
    try:
        data = request.json
        if data is None:
            return jsonify({
                "code": 400,
                "msg": "请求体必须是有效的JSON格式",
                "data": None
            }), 400
            
        prompt = data.get('prompt')
        if not prompt:
            return jsonify({
                "code": 400,
                "msg": "prompt是必填参数",
                "data": None
            }), 400

        headers = {
            "Authorization": f"Bearer {SUNO_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # 使用动态回调URL，支持外部访问
        # 获取本机IP地址
        try:
            # 获取本机IP地址
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            callback_url = f"http://{local_ip}:5000/api/callback"
        except:
            # 如果获取IP失败，使用localhost
            callback_url = "http://localhost:5000/api/callback"
        
        payload = {
            "prompt": prompt,
            "model": data.get("model", "V4"),
            "make_instrumental": bool(data.get("make_instrumental", False)),
            "instrumental": bool(data.get("make_instrumental", False)),
            "wait_audio": bool(data.get("wait_audio", False)),
            "is_public": bool(data.get("is_public", False)),
            "custom_mode": bool(data.get("custom_mode", False)),
            "is_custom": bool(data.get("is_custom", False)),
            "callBackUrl": callback_url,
            "is_callback": True  # 启用回调
        }

        endpoint = "https://api.sunoapi.org/api/v1/generate"
        
        print(f"请求Suno API: {endpoint}")
        print(f"请求参数: {payload}")
        
        response = requests.post(
            endpoint,
            json=payload,
            headers=headers,
            timeout=60
        )
        
        print(f"响应状态码: {response.status_code}")
        print(f"原始响应: {response.text}")
        
        try:
            result = response.json()
        except:
            return jsonify({
                "code": 500,
                "msg": "无效的JSON响应",
                "data": None
            }), 500

        if response.status_code != 200 or result.get("code") != 200:
            return jsonify({
                "code": result.get("code", response.status_code),
                "msg": result.get("msg", "API调用失败"),
                "data": result.get("data")
            }), response.status_code if response.status_code != 200 else 500
            
        task_id = result.get("data", {}).get("taskId") or result.get("data", {}).get("id")
        if not task_id:
            return jsonify({
                "code": 500,
                "msg": "缺少任务ID",
                "data": result
            }), 500
        
        return jsonify({
            "code": 200,
            "msg": "success",
            "data": {
                "id": task_id,
                "status": "processing"
            }
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "code": 500,
            "msg": "服务器内部错误",
            "data": str(e)
        }), 500

# 回调处理接口
@app.route('/api/callback', methods=['POST'])
def callback_handler():
    try:
        data = request.json
        if data is None:
            return jsonify({"code": 400, "msg": "无效的回调数据"}), 400
            
        print(f"收到回调数据: {data}")
        
        # 根据官方示例处理回调数据
        callback_type = data.get("callbackType")
        task_id = data.get("task_id")
        
        if callback_type == "complete" and task_id:
            # 处理完成回调
            audio_data = data.get("data", [])
            if audio_data and len(audio_data) > 0:
                first_audio = audio_data[0]
                audio_url = first_audio.get("audio_url")
                image_url = first_audio.get("image_url")
                title = first_audio.get("title", "未命名音乐")
                duration = first_audio.get("duration", 0)
                
                print(f"任务ID: {task_id}")
                print(f"音频URL: {audio_url}")
                print(f"图片URL: {image_url}")
                print(f"标题: {title}")
                print(f"时长: {duration}秒")
                
                # 这里可以存储结果到数据库或文件
                # 暂时只打印日志
            else:
                print("回调数据中没有音频信息")
        else:
            print(f"回调类型: {callback_type}, 任务ID: {task_id}")
        
        return jsonify({"code": 200, "msg": "回调处理成功"})
        
    except Exception as e:
        traceback.print_exc()
        return jsonify({"code": 500, "msg": "回调处理失败"}), 500

# 状态查询接口（官方标准实现，参数名为taskId）
@app.route('/api/status/<task_id>', methods=['GET'])
def check_status(task_id):
    try:
        headers = {
            "Authorization": f"Bearer {SUNO_API_KEY}",
            "Accept": "application/json"
        }
        # 关键修正：参数名为taskId
        endpoint = f"https://api.sunoapi.org/api/v1/generate/record-info?taskId={task_id}"
        print(f"尝试状态查询端点: {endpoint}")
        response = requests.get(endpoint, headers=headers, timeout=30)
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text[:500]}...")
        result = response.json()
        if response.status_code == 200 and result.get("code") == 200:
            data = result.get("data", {})
            status = data.get("status", "unknown")
            
            # 提取音频URL - 检查多个可能的位置
            audio_url = None
            image_url = None
            video_url = None
            
            # 1. 检查response字段（Suno API的主要音频URL位置）
            response_data = data.get("response")
            if response_data:
                print(f"Response数据结构: {type(response_data)}")
                if isinstance(response_data, dict):
                    # 检查sunoData数组
                    suno_data = response_data.get("sunoData", [])
                    print(f"SunoData数组长度: {len(suno_data)}")
                    if suno_data and len(suno_data) > 0:
                        # 取第一个音频数据
                        first_audio = suno_data[0]
                        print(f"第一个音频数据: {first_audio}")
                        # 根据官方示例，使用audioUrl字段
                        audio_url = first_audio.get("audioUrl")
                        image_url = first_audio.get("imageUrl")
                        video_url = first_audio.get("videoUrl")
                        print(f"提取的audioUrl: {audio_url}")
                        print(f"提取的imageUrl: {image_url}")
                    else:
                        # 如果没有sunoData，检查response的其他字段
                        audio_url = response_data.get("audio_url") or response_data.get("audioUrl")
                        image_url = response_data.get("image_url") or response_data.get("imageUrl")
                        video_url = response_data.get("video_url") or response_data.get("videoUrl")
                elif isinstance(response_data, str):
                    # 如果response是字符串，可能是直接的音频URL
                    audio_url = response_data
            
            # 2. 如果response中没有，检查data字段的其他位置
            if not audio_url:
                audio_url = data.get("audio_url") or data.get("audioUrl")
            if not image_url:
                image_url = data.get("image_url") or data.get("imageUrl")
            if not video_url:
                video_url = data.get("video_url") or data.get("videoUrl")
            
            print(f"提取的音频URL: {audio_url}")
            print(f"提取的图片URL: {image_url}")
            print(f"提取的视频URL: {video_url}")
            
            return jsonify({
                "code": 200,
                "msg": "success",
                "data": {
                    "id": task_id,
                    "status": status,
                    "audio_url": audio_url,
                    "image_url": image_url,
                    "video_url": video_url,
                    "metadata": data.get("metadata", {})
                }
            })
        elif result.get("code") == 404:
            return jsonify({
                "code": 404,
                "msg": "任务正在处理中，请稍后再试",
                "data": {
                    "id": task_id,
                    "status": "processing"
                }
            }), 404
        else:
            return jsonify({
                "code": result.get("code", response.status_code),
                "msg": result.get("msg", "API调用失败"),
                "data": result.get("data")
            }), response.status_code
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "code": 500,
            "msg": "服务器内部错误",
            "data": str(e)
        }), 500