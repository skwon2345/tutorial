from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql://root:root@db/main"  # mysql://USER:PASSWORD@HOST/DATABASE
CORS(app)

db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(
        db.Integer, primary_key=True, autoincrement=False
    )  # Product id is created in Django app, so autoincrement is False. It just recieve Product from RabbitMQ.
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))


class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    UniqueConstraint("user_id", "product_id", name="user_product_unique")


@app.route("/")
def index():
    return "Hello"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
