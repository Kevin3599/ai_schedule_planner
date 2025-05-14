from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_schedule(tasks):
    if not tasks:
        return "你还没有添加任务。"

    prompt = "今天我有如下任务，请帮我安排一个合理的日程表：\n"
    for t in tasks:
        prompt += f"- {t['task']}，截止：{t['deadline']}，优先级：{t['priority']}\n"

    prompt += "\n请从早上开始安排具体时间段，并合理分配任务时间。"

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"OpenAI 错误：{e}"
