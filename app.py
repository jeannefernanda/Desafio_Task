from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

DATABASE = "tasks.db"

def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    status TEXT NOT NULL)
    """)
    conn.commit()
    conn.close()

@app.route('/', methods=['GET','POST'])
def tasks():
    create_table()

    if request.method == 'GET':
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM tasks
        """)
        tasks = cursor.fetchall()
        tasks_json = [{"id" : task[0], "title" : task[1], "description" : task[2], "status" : task[3],} for task in tasks]
        return jsonify(tasks_json)
    
    elif request.method == 'POST':
        data = request.json
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (title, description, status) VALUES (?, ?, ?)", (data['title'], data['description'], data['status']))
        conn.commit()
        conn.close()
        return jsonify({"message": "Task created successfully"})
   
    


if __name__ == '__main__':
    app.run(debug=True)