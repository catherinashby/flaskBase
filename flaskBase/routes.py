from flask import render_template
from flaskBase import app

# a simple page that says hello
@app.route('/')
@app.route('/index')
def index():
    return render_template( 'frontpage.html', user={} )

