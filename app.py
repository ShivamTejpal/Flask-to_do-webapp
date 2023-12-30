from flask import Flask,render_template,request,redirect
#from flask_graphql import GraphQLView
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#app.add_url_rule(
#    '/graphql',
#    view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
#)

class Todo(db.Model):
    srno = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.srno} -{self.title}"
@app.route('/',methods=['GET','POST'])
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

@app.route('/update')
def update():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'hello_world'

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
