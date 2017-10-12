from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key='ijustwannafinishthisprojectandgotosleep'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        
        if not title or not body:
            flash('Incomplete post. Fill in the rest!')
            
            return render_template('newpost.html', title=title, body=body)
       
        new_blog = Blog(title, body)
        db.session.add(new_blog)
        db.session.commit()

        return return render_template('displaypost.html', title=title, body=body)

    return render_template('newpost.html')

#@app.route('/displaypost')
#def displaypost():
 #   title = 'Test title'
  #  body= 'test body and shit'
   # return render_template('displaypost.html', title=title, body=body)


@app.route('/blog')
def blog():

    blogs = Blog.query.all()
    
    return render_template('blog.html',title="Build a Blog", 
        blogs=blogs)


@app.route('/')
def index():
    return redirect('/blog')

if __name__ == '__main__':
    app.run()