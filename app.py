from flask import Flask,render_template,request,redirect
#from flask_graphql import GraphQLView
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_oidc import OpenIDConnect
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#app.add_url_rule(
#    '/graphql',
#    view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
#)
app.config['SECRET_KEY'] = '123456'
app.debug = True
app.config['OIDC_CLIENT_SECRETS'] = 'client_secrets.json'
app.config['OIDC_COOKIE_SECURE'] = False
app.config['OIDC_CALLBACK_ROUTE'] = '/oidc/callback'
app.config['OIDC_SCOPES'] = 'openid','email','profile'

oidc = OpenIDConnect(app) 



class Todo(db.Model):
    srno = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.srno} -{self.title}"
@app.route('/',methods=['GET','POST'])
@oidc.require_login
def hello_world():
    if request.method == "POST":
        title = request.form['title']
        description = request.form['description']
        todo = Todo(title=title, description=description)
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.all()
    return render_template('index.html',allTodo=allTodo)
    

@app.route('/show')
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'hello_world'

@app.route('/update/<int:srno>', methods=['GET','POST'])
def update(srno):
    if request.method=='POST':
        title = request.form['title']
        description = request.form['description']
        todo = Todo.query.filter_by(srno=srno).first()
        todo.title=title
        todo.description=description
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo = Todo.query.filter_by(srno=srno).first()
    return render_template('update.html',todo=todo)

@app.route('/delete/<int:srno>')
def delete(srno):
    todo = Todo.query.filter_by(srno=srno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect ("/")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

#to create db
#use from app import app,db
#>>> with app.app_context():        
#...     db.create_all()
#to start env using cmd .\env\Scripts\activate
#'kc.bat start-dev' to start kecloak dev port-'localhost:8080 '
    