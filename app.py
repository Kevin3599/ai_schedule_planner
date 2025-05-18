from flask import Flask, render_template, request
import json
from datetime import datetime
import locale
from planner import generate_schedule
import csv
from io import StringIO
from werkzeug.utils import secure_filename
import os

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

def clear_tasks():
    try:
        with open(TASK_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)
        return True
    except Exception:
        return False

# 修改 parse_csv_tasks 函数，添加 category 参数
def parse_csv_tasks(file_content, category):
    """解析 CSV 文件内容并返回任务列表，使用文件名作为分类"""
    tasks = []
    csv_reader = csv.reader(StringIO(file_content.decode('utf-8-sig')))
    next(csv_reader, None)  # 跳过表头
    for row in csv_reader:
        if len(row) >= 3:
            tasks.append({
                'task': row[0].strip(),
                'deadline': row[1].strip(),
                'priority': row[2].strip(),
                'category': category  # 添加分类字段
            })
    return tasks

@app.route('/clear', methods=['POST'])
def clear():
    if clear_tasks():
        return {'status': 'success', 'message': '所有任务已清除'}
    return {'status': 'error', 'message': '清除任务失败'}, 500

# 修改 upload_file 函数
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return {'status': 'error', 'message': '没有上传文件'}, 400
    
    file = request.files['file']
    if file.filename == '':
        return {'status': 'error', 'message': '未选择文件'}, 400
    
    if file and file.filename.endswith('.csv'):
        try:
            # 从文件名获取分类（去掉.csv后缀）
            category = os.path.splitext(secure_filename(file.filename))[0]
            
            content = file.read()
            new_tasks = parse_csv_tasks(content, category)
            
            # 加载现有任务并合并
            existing_tasks = load_tasks()
            existing_tasks.extend(new_tasks)
            
            # 保存合并后的任务
            save_tasks(existing_tasks)
            
            # 对任务进行分类
            categorized_tasks = {}
            for task in existing_tasks:
                cat = task.get('category', '其他')
                if cat not in categorized_tasks:
                    categorized_tasks[cat] = []
                categorized_tasks[cat].append(task)
            
            # 获取当前日期并生成新的计划
            current_date = datetime.now().strftime('%Y年%m月%d日')
            schedule = generate_schedule(existing_tasks, current_date)
            
            return {
                'status': 'success', 
                'message': f'成功导入 {len(new_tasks)} 个任务到 {category} 分类',
                'schedule': schedule,
                'tasks': existing_tasks,
                'categorized_tasks': categorized_tasks
            }
            
        except Exception as e:
            return {'status': 'error', 'message': f'处理文件时出错: {str(e)}'}, 500
    
    return {'status': 'error', 'message': '不支持的文件格式'}, 400

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
