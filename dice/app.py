from flask import Flask, render_template, request, redirect, url_for


from .models import db

app = Flask("dice")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dice.db"
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':

        return redirect(url_for('register'))

    return render_template('index.html')

@app.route('/register', methods=['GET' , 'POST'])
def register():

    return render_template('register.html')


