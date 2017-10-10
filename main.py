from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/', methods=['POST', 'GET'])
def index():
### Currently this only shows the blog posts that are created
    # TODO add a post form to the html page above the blog posts. Current code support pulling that info and handling request
    # TODO after we have that functionality working, split into /blog and /newpost. make index redirect to /blog
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        new_blog = Blog(title, body)
        db.session.add(new_blog)
        db.session.commit()

    blogs = Blog.query.all()
    
    return render_template('blog.html',title="Build a Blog", 
        blogs=blogs)


if __name__ == '__main__':
    app.run()