import os

from flask import Flask, flash, redirect, jsonify, render_template, request, url_for
from db import insert_message, fetch_messages


app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "change-this-secret")

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    success = None
    if request.method == 'POST':
        message = request.form.get('message', '').strip()

        if not message:
            error = 'Please provide a message.'
        else:
            try:
                # no name/email fields in the current form; store as Anonymous
                insert_message(name='Anonymous', email=None, message=message)
                success = 'Your message was saved successfully.'
            except Exception as exc:
                error = f'Unable to save your message: {exc}'

    messages = []
    try:
        rows = fetch_messages(limit=10)
        # rows from Supabase are dict-like with keys matching column names
        messages = [
            {
                'id': r.get('id'),
                'name': r.get('name'),
                'email': r.get('email'),
                'message': r.get('message'),
                'created_at': r.get('created_at'),
            }
            for r in (rows or [])
        ]
    except Exception:
        messages = []

    # Pass Supabase client info for the browser script (anon key is safe for public use)
    supabase_url = os.environ.get('SUPABASE_URL', '')
    supabase_anon = os.environ.get('SUPABASE_ANON', os.environ.get('SUPABASE_ANON_KEY', os.environ.get('SUPABASE_KEY', '')))

    return render_template(
        'index.html',
        error=error,
        success=success,
        messages=messages,
        supabase_url=supabase_url,
        supabase_anon=supabase_anon,
    )


@app.route('/env')
def env():
    """Expose selected browser-safe environment values for debugging."""
    return jsonify({
        'SUPABASE_URL': os.environ.get('SUPABASE_URL', ''),
        'SUPABASE_ANON': os.environ.get('SUPABASE_ANON', ''),
        'SUPABASE_URL_loaded': bool(os.environ.get('SUPABASE_URL')),
        'SUPABASE_ANON_loaded': bool(os.environ.get('SUPABASE_ANON')),
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
