from urllib.parse import quote_plus, urlencode
from flask import Flask,render_template,request,redirect,url_for,session,abort
#from flask_graphql import GraphQLView
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from authlib.integrations.flask_oauth2 import ResourceProtector
from authlib.jose.rfc7517.jwk import JsonWebKey
from authlib.oauth2.rfc7523 import JWTBearerTokenValidator
from urllib.request import urlopen
from authlib.integrations.flask_client import OAuth
import json

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


#oauth 2 setup
appConf = {
    "OAUTH2_CLIENT_ID": "web_app",
    "OAUTH2_CLIENT_SECRET": "BhSDZFLpMMkC28cdhxxfBM5eAIMIJoGe",
    "OAUTH2_ISSUER": "http://localhost:8080/realms/myorg",
    "FLASK_SECRET": "stringggg",
    "FLASK_PORT": 3000
} 

#app = Flask(__name__)
app.secret_key = appConf.get("FLASK_SECRET")

oauth = OAuth(app)
oauth.register(
    "myApp",
    client_id=appConf.get("OAUTH2_CLIENT_ID"),
    client_secret=appConf.get("OAUTH2_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
        # 'code_challenge_method': 'S256'  # enable PKCE
    },
    server_metadata_url=f'{appConf.get("OAUTH2_ISSUER")}/.well-known/openid-configuration',
)


@app.route('/login')
def login():
    if "user" in session:
        abort(404)
    return oauth.myApp.authorize_redirect(redirect_uri=url_for("callback", _external=True))


@app.route("/callback")
def callback():
    token = oauth.myApp.authorize_access_token()
    session["user"] = token
    return redirect(url_for("home"))




#dont -----------------------------><-----------------
@app.route('/',methods=['GET','POST'])
def home():
    if request.method == "POST":
        title = request.form['title']
        description = request.form['description']
        todo = Todo(title=title, description=description)
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.all()
    user_session = session.get("user")  # Renamed the local variable
    pretty = json.dumps(user_session, indent=4)  # Updated variable name
    return render_template('index.html', allTodo=allTodo)



#update todo
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


#delete todo

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

#to create db use from app import app,db
#>>> with app.app_context():        
#...     db.create_all()
#to start env using cmd .\env\Scripts\activate
#'kc.bat start-dev' to start kecloak dev port-'localhost:8080 '
    