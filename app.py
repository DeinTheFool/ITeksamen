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
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()

        if not name or not email or not message:
            error = 'Please provide your name, email, and a message.'
        else:
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO messages (name, email, message) VALUES (%s, %s, %s)",
                    (name, email, message),
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
            "SELECT id, name, email, message, created_at FROM messages ORDER BY created_at DESC LIMIT 10"
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        messages = [
            {
                'id': row[0],
                'name': row[1],
                'email': row[2],
                'message': row[3],
                'created_at': row[4],
            }
            for row in rows
        ]
    except Exception:
        messages = []

    return render_template('index.html', error=error, success=success, messages=messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
