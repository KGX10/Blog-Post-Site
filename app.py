from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime
app = Flask(__name__)

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(20), nullable = False)
    content = db.Column(db.Text, nullable = False)
    author = db.Column(db.String(20), nullable = False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "Blog Post" + str(self.id)

#Dummy Data
posts = [
    {
        'title':'Post 1',
        'content' : 'content of post 1'
    },
    {
        'title':'Post 2',
        'content': 'Content of post 2'
    }
]
#Pages
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/posts', methods = ['GET','POST'])
def posts():
    # if request.method == 'POST':
    #     post_title = request.form['title']
    #     post_content = request.form['content']
    #     post_author = request.form['author']
    #     new_blogpost = BlogPost(title = post_title, content = post_content, author = post_author)
    #     db.session.add(new_blogpost)
    #     db.session.commit()
    #     return redirect('/posts')

    # else:
    posts = BlogPost.query.order_by(desc(BlogPost.id)).all()
    return render_template('posts.html', posts = posts)
@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/<int:id>', methods = ['GET','POST'])
def edit(id):
    current_post = BlogPost.query.get_or_404(id)
    if request.method == "POST":
        current_post.title = request.form['new_title']
        current_post.content = request.form['new_content']
        current_post.author = request.form['new_author']
        current_post.date_posted = datetime.now()
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post = current_post)
@app.route('/posts/newpost', methods = ['GET','POST'])
def new_post():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_blogpost = BlogPost(title = post_title, content = post_content, author = post_author)
        db.session.add(new_blogpost)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new_post.html')


@app.route('/onlyget', methods =['GET'])
def only_get():
    return "Only get requests allowed, no posting"

if __name__ == "__main__":
    app.run(debug=True)