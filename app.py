import os

from flask import Flask, flash, redirect, render_template, request, url_for
from db import get_db_connection


app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "change-this-secret")

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    success = None
    if request.method == 'POST':
        message = request.form.get('message', '').strip()

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                  "INSERT INTO messages (message) VALUES (%s)",
                  (message),
                )
            conn.commit()
            cursor.close()
            conn.close()
            success = 'Your message was saved successfully.'
        except Exception as exc:
            error = f'Unable to save your message: {exc}'

    messages = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, message, time FROM messages ORDER BY time DESC LIMIT 10"
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        messages = [
            {
                'id': row[0],
                'message': row[3],
                'time': row[4],
            }
            for row in rows
        ]
    except Exception:
        messages = []

    return render_template('index.html', error=error, success=success, messages=messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
