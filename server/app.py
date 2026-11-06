import os
import time
from flask import Flask, request, send_from_directory, render_template_string

app = Flask(__name__)
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

PAGE = """
<h1>DayLens</h1>
<p>{{ files|length }} photos</p>
{% for f in files %}
  <img src="/img/{{ f }}" width="320" title="{{ f }}">
{% endfor %}
"""

@app.route("/upload", methods=["POST"])
def upload():
    name = os.path.basename(request.headers.get("X-Filename", f"{int(time.time())}.jpg"))
    with open(os.path.join(UPLOAD_DIR, name), "wb") as f:
        f.write(request.get_data())
    return "ok"

@app.route("/img/<name>")
def img(name):
    return send_from_directory(UPLOAD_DIR, name)

@app.route("/")
def index():
    files = sorted(os.listdir(UPLOAD_DIR), reverse=True)
    return render_template_string(PAGE, files=files)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)