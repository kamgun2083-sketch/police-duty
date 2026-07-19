from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        conn = get_db_connection()
        conn.execute('INSERT INTO entries (date, rank, name, remarks) VALUES (?, ?, ?, ?)', 
                     (request.form['date'], request.form['rank'], request.form['name'], request.form['remarks']))
        conn.commit()
        conn.close()
        return redirect('/dashboard')
    return render_template('form.html')

@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    entries = conn.execute('SELECT * FROM entries').fetchall()
    conn.close()
    return render_template('dashboard.html', entries=entries)

if __name__ == '__main__':
    # डेटाबेस तालिका बनाउनुहोस्
    conn = sqlite3.connect('database.db')
    conn.execute('CREATE TABLE IF NOT EXISTS entries (id INTEGER PRIMARY KEY, date TEXT, rank TEXT, name TEXT, remarks TEXT)')
    conn.close()
    app.run()