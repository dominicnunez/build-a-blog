from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    body = db.Column(db.String(2100))

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
@app.route("/")
def fIndex():
    return redirect('/blog')

@app.route('/blog')
def fBlog():
    if Blog.query.all() == True:
        return render_template("blog.html")
    else:
        return redirect("/newpost")

@app.route('/newpost', methods=["GET", "POST"])
def fNewPost():
    return render_template("newpost.html")

@app.route("/entry")
def fEntry():
    return render_template("entry.html")


if __name__ == '__main__':
    app.run()