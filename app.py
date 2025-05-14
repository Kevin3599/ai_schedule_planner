from flask import Flask, render_template, request
import json
from datetime import datetime
import locale
from planner import generate_schedule

# 设置 locale 为中文
try:
    locale.setlocale(locale.LC_ALL, 'zh_CN.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_ALL, 'Chinese_China.936')
    except:
        pass  # 如果都失败了，使用默认的日期格式

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
    selected_date = request.form.get('selected_date')
    
    if selected_date:
        try:
            date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
            formatted_date = date_obj.strftime('%Y-%m-%d')  # 使用连字符格式
        except ValueError:
            formatted_date = datetime.now().strftime('%Y-%m-%d')
    else:
        formatted_date = datetime.now().strftime('%Y-%m-%d')

    # 将日期格式转换为中文显示
    display_date = formatted_date.replace('-', '年', 1).replace('-', '月', 1) + '日'

    if request.method == 'POST':
        if 'task' in request.form:  # 添加新任务
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

    schedule = generate_schedule(tasks, display_date)
    return render_template('index.html', 
                         tasks=tasks, 
                         schedule=schedule, 
                         current_date=datetime.now().strftime('%Y-%m-%d'),
                         selected_date=selected_date or datetime.now().strftime('%Y-%m-%d'))

if __name__ == '__main__':
    app.run(debug=True)
