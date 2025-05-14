import requests
import json

# 直接设置 API key
DEEPSEEK_API_KEY = "sk-082931d1c6094a67a97be1be9d7669d2"
API_URL = "https://api.deepseek.com/v1/chat/completions"

def generate_schedule(tasks):
    if not tasks:
        return "你还没有添加任务。"

    # 构建提示信息
    prompt = "今天我有如下任务，请帮我安排一个合理的日程表：\n"
    for t in tasks:
        prompt += f"- {t['task']}，截止：{t['deadline']}，优先级：{t['priority']}\n"
    prompt += "\n请从早上开始安排具体时间段，并合理分配任务时间。"

    try:
        # 准备请求数据
        request_data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}]
        }

        # 发送请求
        response = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            },
            json=request_data  # 使用 json 参数自动处理序列化
        )
        
        # 检查响应状态
        response.raise_for_status()
        
        result = response.json()
        return result['choices'][0]['message']['content']

    except requests.exceptions.RequestException as e:
        return f"网络请求错误: {str(e)}"
    except Exception as e:
        return f"意外错误: {str(e)}"
