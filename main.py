from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:finalunit2project@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key='ijustwannafinishthisprojectandgotosleep'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def __repr__(self):
        return self.username

@app.before_request
def require_login():
    allowed_routes = ['login', 'blog', 'index', 'signup']
    if request.endpoint not in allowed_routes and 'user' not in session:
        flash('you need to sign in first')
        return redirect('/login')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = User.query.filter_by(username=username)
        if users.count() != 1:
            flash('uhm...Username does not exist')
            return redirect('/login')
        else:
            user = users.first()
        
            if password == user.password:      
                session['user'] = user.username
                flash('welcome back, '+user.username)
                return redirect("/newpost")
            else:
                flash('Oops! Incorrect Password')
                return redirect('/login')

        
        


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        if not username or not password or not verify:
            flash("all information is required")
            return redirect('/signup')
        if len(username) < 3 :
            flash('zoiks! "' + username + '" needs to be more than 3 characters long')
            return redirect('/signup')
        username_db_count = User.query.filter_by(username=username).count()
        if username_db_count > 0:
            flash('yikes! "' + username + '" is already taken and password reminders are not implemented')
            return redirect('/signup')
        if password != verify:
            flash('passwords did not match')
            return redirect('/signup')
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        session['user'] = user.username
        flash('start posting, '+user.username)
        return redirect("/newpost")
    else:
        return render_template('signup.html')


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        owner = User.query.filter_by(username=session['user']).first()
        
        if not title or not body:
            flash('Incomplete post. Fill in the rest!')
            
            return render_template('newpost.html', title=title, body=body)
       
        new_blog = Blog(title, body, owner)
        db.session.add(new_blog)
        db.session.commit()

        this_post=Blog.query.filter(Blog.id==new_blog.id).first()
        
        return render_template('displaypost.html', this_post=this_post)
    
    return render_template('newpost.html')

@app.route('/blog')
def blog():

    all_posts = Blog.query.all()
    writers =User.query.all()
    id=request.args.get('id')
    user=request.args.get('user')
    
   
    if id:
        int_id=int(id)
        this_post=Blog.query.filter(Blog.id==int_id).first()
        return render_template('displaypost.html', this_post=this_post)
    if user:
        #user is user's name 'john'
        #query the database for all blog posts that john owns
        this_user=User.query.filter(User.username==user).first()
        all_posts=Blog.query.filter(Blog.owner_id==this_user.id).all()
        
    return render_template('blog.html',title="Build a Blog", 
        blogs=all_posts)


@app.route('/logout')
def logout():
    del session['user']
    return redirect('/blog')

@app.route('/')
def index():
    all_users=User.query.all()

    return render_template('index.html', all_users=all_users)

if __name__ == '__main__':
    app.run()