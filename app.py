from flask import Flask,render_template
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
    description = db.Column(db.String(1000), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.srno} -{self.title}"
@app.route('/')
def hello_world():
    todo = Todo(title="First Todo",description="Start Investing")
    db.session.add(todo)
    db.session.commit()
    return render_template('index.html',allTodo=allTodo)
    #return 'Hello, World!'

@app.route('/show')
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return hello_world

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)