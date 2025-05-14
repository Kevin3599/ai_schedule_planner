from flask import Flask, render_template, request
import json
from planner import generate_schedule

app = Flask(__name__)
TASK_FILE = 'tasks.json'

def load_tasks():
    try:
        with open(TASK_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_tasks(tasks):
   with open(TASK_FILE, 'w', encoding='utf-8') as f:
    json.dump(tasks, f, indent=2, ensure_ascii=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    tasks = load_tasks()

    if request.method == 'POST':
        task = request.form['task']
        deadline = request.form['deadline']
        priority = request.form['priority']
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
