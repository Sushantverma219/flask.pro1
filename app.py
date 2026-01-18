from flask import Flask,request,render_template,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import check_password_hash,generate_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db"

db = SQLAlchemy(app)

class user(db.Model):
    ID = db.Column(db.Integer,primary_key = True)
    Username = db.Column(db.String(200),nullable = False)
    Email = db.Column(db.String(200),unique = True)
    Password = db.Column(db.String(200),nullable = False)
    created_at = db.Column(db.DateTime,default = datetime.utcnow)
    
with app.app_context():
    db.create_all()

@app.route('/')
def main():
    return render_template("main.html")

@app.route('/Register',methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        Username = request.form['Username']
        Email = request.form['Email']
        Password = request.form['Password']

        hash_password = generate_password_hash(Password)

        new_user = user(
            Username = Username,
            Email = Email,
            Password = hash_password
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect('/')

    return render_template("register.html")

if __name__ == '__main__':
    app.run(debug=True)