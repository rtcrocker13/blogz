from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:launchcode@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'



class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    entry = db.Column(db.String(21844))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __init__(self, title, entry, owner):
        self.title = title
        self.entry = entry
        self.owner = owner
        
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    blogs = db.relationship('Blog', backref='owner')
    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'blog', 'index']
    if (('user.id' not in session) and (request.endpoint not in allowed_routes)):
        return redirect('/login')

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    

    id = request.args.get('id')
    bloguser = request.args.get('userid')
    user = User.query.filter_by(id=bloguser).first()

    if id == None and bloguser == None: 
        blogs = Blog.query.all()
        return render_template('blog.html',title= "Blogz!", 
        blogs=blogs)
    if id:
        blog = Blog.query.get(id)
        return render_template('blog-entry.html', blog=blog)
    if bloguser:
        return render_template('blog.html', blogs=user.blogs)  

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            print('a')
            session['user.id'] = user.id
            print('b')
            flash("Logged in")
            return redirect('/newpost')
        else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    username= ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        if username == "" or password == "" or verify == "":
            print('a')
            flash('One or more fields is invalid!')
        elif password != verify:
            flash('Passwords do not match!')
        elif len(username) < 3:
            flash('Invalid Username!')
        elif len(password) < 3:
            flash('Invalid Password') 
        else:
            existing_user = User.query.filter_by(username=username).first()
            if not existing_user:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                #existing_user = User.query.filter_by(username=username).first()
                session['user.id'] = new_user.id
                return redirect('/newpost')
            else:
                flash('Username already exists!')

    return render_template('signup.html', username=username)

@app.route('/', methods=['POST', 'GET'])
def index():
    
    users = User.query.all()
    return render_template('index.html',title= "Blogz!", 
        users=users)     


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    owner_id = User.query.filter_by(id=session['user.id']).first()
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
            new_post = Blog(blog_title, blog_post, owner_id)
            db.session.add(new_post)
            db.session.commit()
            url = '/blog?id='+ str(new_post.id)
            return redirect(url)
    else:
        return render_template('newpost.html')

@app.route('/logout')
def logout():
    del session['user.id']
    flash('You have logged out, log back in to submit a post!')
    return redirect('/blog')

if __name__ == '__main__':
    app.run()