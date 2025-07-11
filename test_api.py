#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Suno API 测试脚本
用于测试不同的API端点
"""

import requests
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()
SUNO_API_KEY = os.getenv('SUNO_API_KEY')

if not SUNO_API_KEY:
    print("错误: 未找到SUNO_API_KEY环境变量")
    exit(1)

def test_generate():
    """测试音乐生成API"""
    print("=== 测试音乐生成API ===")
    
    headers = {
        "Authorization": f"Bearer {SUNO_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": "一首关于宇宙的音乐",
        "model": "V4",
        "make_instrumental": False,
        "instrumental": False,
        "wait_audio": False,
        "is_public": False,
        "custom_mode": False,
        "is_custom": False,
        "callBackUrl": "https://yourdomain.com/callback",
        "is_callback": False
    }
    
    endpoint = "https://api.sunoapi.org/api/v1/generate"
    
    try:
        response = requests.post(endpoint, json=payload, headers=headers, timeout=60)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            task_id = result.get("data", {}).get("taskId")
            if task_id:
                print(f"任务ID: {task_id}")
                return task_id
        
    except Exception as e:
        print(f"生成请求失败: {e}")
    
    return None

def test_status_endpoints(task_id):
    """测试状态查询端点"""
    print(f"\n=== 测试状态查询端点 (任务ID: {task_id}) ===")
    
    headers = {
        "Authorization": f"Bearer {SUNO_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # 使用官方文档中的正确端点，将task_id作为查询参数
    endpoint = f"https://api.sunoapi.org/api/v1/generate/record-info?task_id={task_id}"
    
    print(f"--- 测试端点: {endpoint} ---")
    try:
        response = requests.get(endpoint, headers=headers, timeout=30)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text[:500]}...")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 成功获取状态!")
            print(f"完整响应: {result}")
            return endpoint, result
        elif response.status_code == 404:
            print("任务还在处理中...")
            return endpoint, None
        else:
            print(f"❌ 状态查询失败: {response.status_code}")
            return None, None
            
    except Exception as e:
        print(f"请求失败: {e}")
        return None, None

if __name__ == "__main__":
    print("开始测试Suno API...")
    
    # 测试生成API
    task_id = test_generate()
    
    if task_id:
        # 等待一段时间让任务开始处理
        import time
        print(f"\n等待5秒让任务开始处理...")
        time.sleep(5)
        
        # 测试状态查询端点
        working_endpoint, result = test_status_endpoints(task_id)
        
        if working_endpoint:
            print(f"\n✅ 找到可用的状态查询端点: {working_endpoint}")
        else:
            print(f"\n❌ 所有状态查询端点都失败")
    else:
        print("❌ 音乐生成失败") 