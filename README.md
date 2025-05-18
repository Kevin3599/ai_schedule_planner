# 👁️ AI 日程规划器项目文档

## 📖 项目简介

AI 日程规划器是一个基于 GPT/ DeepSeek API 实现的日程生成应用，适用于无需手动排时的智能化日程管理，支持任务录入，自动经 GPT/模型解析后生成合理时间表。

---

## ✨ 功能特色

* ✅ 支持添加任务（含截止日期与优先级）
* ✅ 自动调用 AI 生成日程计划
* ✅ 每天固定预留 1.5 小时健身时间
* ✅ 根据任务量每天分配 1-2 小时作业时间
* ✅ 简洁 Web 界面 (Flask)
* ✅ 任务本地数据存储 (JSON)

---

## 🛠 技术栈

* Python 3.x
* Flask
* requests
* JSON 本地存储
* DeepSeek API / OpenAI API
* HTML + Jinja2

---

## 🚀 项目运行

### 🔧 安装依赖

```bash
pip install flask requests
```

### ▶ 启动服务

```bash
# OpenAI 版本
export OPENAI_API_KEY=sk-xxx    # Windows 用 set
python app.py

# DeepSeek 版本
export DEEPSEEK_API_KEY=ds-xxx
python app.py
```

打开浏览器访问 [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

---

## 🔄 策略系统 Prompt 示例

```text
今天是2025年5月15日，请根据以下任务为我定制一份详细的时间表：

- 每天必须预留1.5小时用于健身
- 作业每天分配1~2小时，根据截止日期和优先级分配
- 时间范围为早上8:00~晚上22:00

任务列表：
- 写物理实验报告，截止日期：5月17日，优先级：高
- 完成 AI 项目代码，截止日期：5月20日，优先级：中
```

---

---

## 📄 版权 LICENSE

MIT License - 此项目允许自由使用、修改、分发
