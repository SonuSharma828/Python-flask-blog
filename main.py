from flask import Flask, render_template, request,redirect,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail
import ssl
import json
import math
app = Flask(__name__)
app.secret_key = 'jai_ram_ji_ki'
with open("config.json","r") as c:
    config = json.load(c)
    params = config["params"]
    

local_server=params['local_server'];
if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_url']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_url']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_SSL=False,
    MAIL_USE_TLS=True,
    MAIL_USERNAME=params['email-user'],
    MAIL_PASSWORD=params['email-password']
)

mail=Mail(app)

class Contact(db.Model):
    Sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone_num = db.Column(db.String(15), nullable=False)  # Adjust to match your schema
    massage = db.Column(db.Text, nullable=True)
    date = db.Column(db.TIMESTAMP, nullable=True)


class Posts(db.Model):
    Sno = db.Column(db.Integer, primary_key=True)
    image_filename=db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(120), nullable=False)
    content = db.Column(db.String(799), nullable=False)  # Adjust to match your schema
    author = db.Column(db.String(80), nullable=False)
    subtitle = db.Column(db.Text, nullable=True)
    date = db.Column(db.TIMESTAMP, nullable=True)

with app.app_context():
    db.create_all()
@app.route("/")
def home():
    posts=Posts.query.filter_by().all()
    last=math.ceil(len(posts)/int(params['num_of_post']))
    page=request.args.get('page',1)
    if (not str(page).isnumeric()):
         page=1
    page=int(page)
    posts=posts[(page-1)*int(params['num_of_post']):(page-1)*int(params['num_of_post'])+int(params['num_of_post'])]
    if(page==1):
         prev="#"
         next="/?page="+str(page+1)
    elif(page==last):
         prev="/?page="+str(page-1)
         next="#"
    else:
         prev="/?page="+str(page-1)
         next="/?page="+str(page+1)
    return render_template("index.html",params=params,posts=posts,prev=prev,next=next)


@app.route("/about")
def about():
    return render_template("about.html",params=params)

@app.route("/dashboard",methods=["GET","POST"])
def login():
       if ('user' in session and session['user']==params['admin-name']):
            posts=Posts.query.all();
            return render_template("dashboard.html",params=params,posts=posts) 
       if request.method == "POST":
            name=request.form.get("username")
            password=request.form.get("password")
            if (name == params['admin-name'] and password==params['admin-password']):
                 session['user']=name
                 posts=Posts.query.all();
                 return render_template("dashboard.html",params=params,posts=posts)
            else:
                 return redirect("/dashboard")
       return render_template("login.html",params=params)

@app.route("/logout")
def logout():
     session.pop('user')
     return redirect("/dashboard")
@app.route("/edit/<string:sno>",methods=["GET","POST"])
def edit(sno):
     if ('user' in session and session['user']==params['admin-name']):
           if request.method=="POST":
                title = request.form.get("title")
                subtitle = request.form.get("subtitle")
                slug = request.form.get("slug")
                content = request.form.get("content")
                imgfile = request.form.get("imgfile")
                author = request.form.get("author")
                if sno=='0':
                     post=Posts(image_filename=imgfile,title=title,slug=slug,content=content,author=author,subtitle=subtitle,date=datetime.now())
                     db.session.add(post)
                     db.session.commit()
                     return redirect("/")
                else:
                    post=Posts.query.filter_by(Sno=sno).first()
                    post.title=title
                    post.subtitle=subtitle
                    post.slug=slug
                    post.content=content
                    post.author=author
                    post.image_filename=imgfile
                    post.date=date
                    return redirect("/edit"+sno)
           post=Posts.query.filter_by(Sno=sno).first()
           return render_template("edit.html",params=params,post=post)
     return redirect("/dashboard")
@app.route("/delete/<string:sno>")
def delete(sno):
     if ('user' in session and session['user']==params['admin-name']):
          post=Posts.query.filter_by(Sno=sno).first()
          db.session.delete(post)
          db.session.commit()
     return redirect("/dashboard") 
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")
        if name and email and phone:  # Basic validation to check if inputs are not empty
            entry = Contact(
                name=name,
                email=email,
                phone_num=phone,
                massage=message,
                date=datetime.now()
            )
            db.session.add(entry)
            db.session.commit()
            mail.send_message('New Massage From '+name,sender=email,recipients=[params['email-user']],body=message + "\n" + phone)
            print("Data saved successfully!")  # Debugging: Confirm data is saved
        else:
            print("Form data missing or incorrect.")
    return render_template("contact.html",params=params)
@app.route("/post/<string:post_slug>",methods=["GET"])
def post_route(post_slug):
    post=Posts.query.filter_by(slug=post_slug).first();
    if not post:
        print("Post not found!")  # Debugging: Check if post is fetched
    else:
        print(f"Post found: {post.title}")  # Debugging: Confirm the post data
    
    return render_template("post.html",params=params,post=post)


if __name__ == "__main__":
    app.run(debug=True, port=8080)
