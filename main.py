from flask import Flask, flash, request, redirect, render_template, send_from_directory, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import html, os

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "dccsvxuBiec7"

class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(60), nullable=False)
    body = db.Column(db.String(2100), nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, title, body):
        self.title = title
        self.body = body

# The /blog route displays all the blog posts.

# You're able to submit a new post at the /newpost route. 
# After submitting a new post, your app displays the main blog page.

# You have two templates, one each for the /blog (main blog listings) and /newpost (post new blog entry) views. 
# Your templates should extend a base.html template which includes some boilerplate HTML that will be used on each page.

# In your base.html template, you have some navigation links that link to the main blog page and to the add new blog page.

# If either the blog title or blog body is left empty in the new post form, the form is rendered again, with a helpful error message and any previously-entered content in the same form inputs.
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/")
def fIndex():
    return redirect('/blog')

@app.route('/blog')
def fBlog():
    if Post.query.all() == True:
        lPosts = Post.query.order_by(Post.pub_date.desc()).all()
        return render_template("blog.html", posts=lPosts)
    else:
        return redirect("/newpost")

@app.route('/newpost', methods=["GET", "POST"])
def fNewPost():
    if request.method == "GET":
        return render_template("newpost.html")

    elif request.method == "POST":
        title = html.escape(request.form["title"])
        body = html.escape(request.form["body"])
        goto = request.form["goto"]

        if title == "" and body == "":
            flash("You must include a title and body!")
            return render_template("newpost.html")

        elif title == "" and body != "":
            flash("You must include title!")
            return render_template("newpost.html", body=body)
        
        elif body == "" and title != "":
            flash("You must include body!")
            return render_template("newpost.html", title=title)
        
        elif title != "" and body != "":
            entry = Post(title, body)
            db.session.add(entry)
            db.session.commit()

            if goto == "home":
                return redirect("/blog")
            else:
                return redirect("/entry")



@app.route("/entry")
def fEntry():
    return render_template("entry.html")


if __name__ == '__main__':
    app.run()