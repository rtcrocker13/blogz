from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:launchcode@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    entry = db.Column(db.String(21844))

    def __init__(self, title, entry):
        self.title = title
        self.entry = entry
        


@app.route('/blog', methods=['POST', 'GET'])
def blog():

    if request.method == 'POST':
        task_name = request.form['task']
        new_task = Task(task_name)
        db.session.add(new_task)
        db.session.commit()
    
    id = request.args.get('id')

    if id == None: 
        blogs = Blog.query.all()
        return render_template('blog.html',title= "build-a-blog!", 
        blogs=blogs)
    else:
        blog = Blog.query.get(id)
        return render_template('blog-entry.html', blog=blog)   




@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    blog_title = ""
    blog_post = ""
    new_post = ""
    empty_title = ""
    empty_post = ""
    no_content = ""

    if request.method == 'POST':
        blog_title = request.form['a']
        blog_post = request.form['b']
        if blog_title == "":
            empty_title = "You Must Have A Title!"
        if blog_post == "":
            empty_post = "You Must Have Content!"
        if blog_post == "" and blog_title == "":
            no_content = "You've Got To Fill In The Blanks!"
        if empty_post or empty_title or no_content:
            return render_template ('newpost.html', empty_title=empty_title, empty_post=empty_post, no_content=no_content,
                blog_title=blog_title, blog_entry=blog_post)
        else:
            new_post = Blog(blog_title, blog_post)
            db.session.add(new_post)
            db.session.commit()
            url = '/blog?id='+ str(new_post.id)
            return redirect(url)
    else:
        return render_template('newpost.html')


if __name__ == '__main__':
    app.run()