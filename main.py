from flask import Flask, render_template, redirect, url_for, request
# from flask_bootstrap import Bootstrap
# from flask_wtf import Form
# from wtforms.fields import DateField
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime

from sqlalchemy import desc, asc

app = Flask(__name__)
today = date.today()

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///to_dos.db"
db = SQLAlchemy(app)


# Create new DB item
class ToDo(db.Model):
    __tablename__ = "to_dos"
    id = db.Column(db.Integer, primary_key=True)
    to_do = db.Column(db.String(250), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    checked = db.Column(db.Boolean, nullable=False)


# db.create_all()


@app.route("/")
def home():
    # order tasks by ascending date
    to_dos = db.session.query(ToDo).order_by(asc(ToDo.date))
    to_dos_left = len([to_do for to_do in to_dos if not to_do.checked])
    to_dos_done = len([to_do for to_do in to_dos if to_do.checked])
    return render_template(
        "index.html",
        today=today,
        to_dos=to_dos,
        to_dos_left=to_dos_left,
        to_dos_done=to_dos_done
    )


@app.route("/add_to_do", methods=["POST"])
def add_to_do():
    to_do = request.form["new_to_do"]
    date = request.form["to_do_date"].replace("-", "/")
    date = datetime.strptime(date, '%Y/%m/%d')
    new_to_do = ToDo(
        to_do=to_do,
        date=date,
        checked=False
    )
    db.session.add(new_to_do)
    db.session.commit()
    return redirect('/')


@app.route("/update_item/<int:to_do_id>")
def update_item(to_do_id):
    update_item = ToDo.query.get(to_do_id)
    update_item.checked = False if update_item.checked else True
    db.session.commit()
    return redirect('/')


@app.route("/delete/<int:to_do_id>")
def delete_item(to_do_id):
    to_delete = ToDo.query.get(to_do_id)
    db.session.delete(to_delete)
    db.session.commit()
    return redirect('/')


@app.route("/edit/<int:to_do_id>")
def edit_item_form(to_do_id):
    edit_item = ToDo.query.get(to_do_id)
    return render_template("edit.html", today=today, to_do=edit_item)


@app.route("/edit_success/<int:to_do_id>", methods=["POST"])
def edit_success(to_do_id):
    edit_item = ToDo.query.get(to_do_id)
    edit_item.to_do = request.form["edit_to_do"]
    date = request.form["to_do_date"].replace("-", "/")
    edit_item.date = datetime.strptime(date, '%Y/%m/%d')
    db.session.commit()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
