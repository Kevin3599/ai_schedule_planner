import requests
import json
from datetime import datetime

# 直接设置 API key
DEEPSEEK_API_KEY = "sk-082931d1c6094a67a97be1be9d7669d2"
API_URL = "https://api.deepseek.com/v1/chat/completions"

def generate_schedule(tasks, selected_date=None):
    if not tasks:
        return "你还没有添加任务。"

    # 获取当前日期或使用选择的日期
    if selected_date:
        current_date = selected_date
    else:
        current_date = datetime.now().strftime("%Y年%m月%d日")

    # 构建提示信息
    prompt = f"现在是{current_date}，我有如下任务需要安排：\n"
    for t in tasks:
        prompt += f"- {t['task']}，截止：{t['deadline']}，优先级：{t['priority']}\n"
    
    prompt += "\n请根据以下原则为我安排这一天的时间表：\n"
    prompt += """注意事项：
1. 每天请预留 1.5 小时用于健身，可以安排在早上或傍晚。
2. 作业每天安排 1~2 小时，根据任务截止时间和紧急程度来判断分配时间。
3. 避免安排过于紧凑，适当留出休息时间。
4. 请从早上 8 点到晚上 10 点之间合理安排时间。
5. 输出格式为：时间段 - 任务内容

请考虑任务优先级和截止时间，生成这一天的详细计划安排。"""

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
