# Flask Message Board

This project is a Flask website that stores messages in MariaDB. It is designed to run on a Linux VM behind Nginx.

## Install dependencies

Activate the virtual environment and install dependencies:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## MariaDB setup

Create a database and table in MariaDB:

```sql
CREATE DATABASE IF NOT EXISTS messages_db;
USE messages_db;

CREATE TABLE IF NOT EXISTS messages (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  message TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Environment variables

Set these before running the app:

- `MARIADB_HOST`
- `MARIADB_PORT`
- `MARIADB_USER`
- `MARIADB_PASSWORD`
- `MARIADB_DATABASE`
- `FLASK_SECRET`

Example:

```bash
export MARIADB_HOST=127.0.0.1
export MARIADB_PORT=3306
export MARIADB_USER=root
export MARIADB_PASSWORD=secret
export MARIADB_DATABASE=messages_db
export FLASK_SECRET="change-this-secret"
```

## Run with Gunicorn

Start the app using Gunicorn on port 5000:

```bash
gunicorn --bind 127.0.0.1:5000 wsgi:application
```

## Nginx configuration

Use the included `nginx.conf` as a starting point for proxying requests to Gunicorn.

- `proxy_pass http://127.0.0.1:5000;`
- Static files are served from the `static/` folder

Reload Nginx after updating the site config:

```bash
sudo nginx -t
sudo systemctl reload nginx
```
