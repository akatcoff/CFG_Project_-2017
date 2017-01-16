from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/')
def hello(name=None):
    return render_template('main_equipment_page.html', name=name)
