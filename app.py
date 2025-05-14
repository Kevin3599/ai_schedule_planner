from flask import Flask, render_template, request
import json
from planner import generate_schedule

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 添加此行确保 JSON 正确处理中文
TASK_FILE = 'tasks.json'

def load_tasks():
    try:
        with open(TASK_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def save_tasks(tasks):
    with open(TASK_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    tasks = load_tasks()

    if request.method == 'POST':
        # 确保接收到的表单数据使用 UTF-8 解码
        task = request.form['task'].strip()
        deadline = request.form['deadline'].strip()
        priority = request.form['priority'].strip()
        
        if task and deadline and priority:
            tasks.append({
                'task': task,
                'deadline': deadline,
                'priority': priority
            })
            save_tasks(tasks)

    schedule = generate_schedule(tasks)
    return render_template('index.html', tasks=tasks, schedule=schedule)

if __name__ == '__main__':
    app.run(debug=True)
