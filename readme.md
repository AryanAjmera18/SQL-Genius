# 🧠 SQL Genius — Chat with Your Database using LangChain + GROQ

Welcome to **SQL Genius**, a modern Streamlit app that allows you to interact with your SQL databases (SQLite or MySQL) using natural language powered by **LangChain** and **GROQ’s LLMs**.

> “Query your data like you talk.”

---

## 🚀 Features

* 🗣️ Natural language chat interface
* 🔌 Works with both SQLite and MySQL
* ⚡ Powered by GROQ’s blazing fast Llama 3 (8B) model
* 📊 Automatically renders SQL results as tables
* 🧠 Built using LangChain SQL Agent Toolkit
* 🎛️ Streamlit-based responsive UI

---



---

## 🛠️ Requirements

* Python 3.8+
* A valid [GROQ API key](https://console.groq.com/)
* `student.db` file or access to your own MySQL instance

---

## 🧪 Installation

```bash
git clone https://github.com/AryanAjmera18/SQL-Genius
cd sql-genius
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

## 🧠 Usage

1. Run the Streamlit app:

```bash
streamlit run app.py
```

2. In the sidebar:

   * Select your database type (SQLite or MySQL)
   * Provide connection details
   * Enter your GROQ API key

3. Start chatting! Example questions:

   * `"Show all records from the STUDENT table."`
   * `"What is the average score of Data Science students?"`

---

## 🧺 Technologies Used

* [LangChain](https://www.langchain.com/)
* [GROQ LLMs](https://www.groq.com/)
* [Streamlit](https://streamlit.io/)
* [SQLAlchemy](https://www.sqlalchemy.org/)

---

## 📂 File Structure

```
sql-genius/
│
├── student.db                  # Sample SQLite database
├── app.py                      # Main Streamlit app
├── requirements.txt            # Python dependencies
└── README.md                   # You're here!
```

---

## 📌 TODO

* [ ] Add support for PostgreSQL
* [ ] Enhance SQL schema visualizer
* [ ] Add chat memory and history exports

---

## 💡 License

MIT License. Feel free to fork and improve!

---

## 👨‍💼 Author

Built with 💙 by [Aryan Ajmera](https://www.linkedin.com/in/aryan-ajmera-8a8b47263/)
