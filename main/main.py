from dataclasses import dataclass

import requests
from flask import Flask, abort, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

from producer import publish

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql://root:root@db/main"  # mysql://USER:PASSWORD@HOST/DATABASE
CORS(app)

db = SQLAlchemy(app)

@dataclass # to make Product class json serializable
class Product(db.Model):
    id: int
    title: str
    image: str

    id = db.Column(
        db.Integer, primary_key=True, autoincrement=False
    )  # Product id is created in Django app, so autoincrement is False. It just recieve Product from RabbitMQ.
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))

@dataclass # to make ProductUser class json serializable
class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    UniqueConstraint("user_id", "product_id", name="user_product_unique")


@app.route("/api/products")
def index():
    print("Ge")
    return jsonify(Product.query.all())

@app.route("/api/products/<int:id>/like", methods=["POST"])
def like(id):
    req = requests.get("http://docker.for.mac.localhost:8000/api/user") # docker.for.mac.localhost refers to local's localhost. if you just write localhost then it refers to docker's localhost.
    json = req.json()

    try:
        product_user = ProductUser(user_id=json["id"], product_id=id)
        db.session.add(product_user)
        db.session.commit()

        # event
        publish("product_liked", id)

    except:
        # exception occurs if same user liked the same product since user_id and product_id is UniqueConstraint for ProductUser tale.
        abort(400, "Your already liked this product.")


    return jsonify({"message": "success"})




if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
