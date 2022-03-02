#  this is the actual back end server
from flask import Flask, abort, request
from mock_data import catalog
from about_me import me, test
import json
import random
from flask_cors import CORS
from config import db

app = Flask("server")
CORS(app)  
# this allows the server to be called from any origin


@app.route("/", methods=["get"])
def home_page():
    return "Under construction!"


@app.route("/test")
def test():
    return "I'm a simple test"


@app.route("/about")
def about():
    return "My name is Jasmine Greinke"


@app.route("/myaddress")
def add():
    test()
    address = me["address"]
    return (address["street"] + " " + address["city"])


@app.route("/api/catalog")
def get_catalog():

    cursor = db.products.find({})
    results = []
    for prod in cursor: 
        prod["_id"] = str(prod["_id"])
        results.append(prod)

    return json.dumps(results)
    # this will parse the catalog and return it as a json string


@app.route("/api/catalog", methods=["POST"])
def save_product():
    product = request.get_json()  # read the payload as a dictionary from json string
    if not "title" in product or len(product["title"]) < 5:
        return abort(400, "There should be a title with a minimum of 5 chars.")

    if not "price" in product:
        return abort(400, "There should be a price for the product with a minimum of $50")
    if not isinstance(product["price"], int) and not isinstance("price", float):
        return abort(400, "Price is invalid. Must be a number")
    if product["price"] <= 0:
        return abort(400, "Product must me more than $0")
    # assign a unique _id
    # product["_id"] = random.randint(10, 100)
    # save to catalog
    # catalog.append(product)
    # return the product

    db.products.insert_one(product)

    product["_id"] = str(product["_id"])

    return json.dumps(product)


@app.route("/api/catalog/count")
def catalog_count():
    cursor = db.products.find({})
    count = 0; 
    for prod in cursor: 
        count =+ 1
    json.dumps(count)


@app.route("/api/catalog/sum")
def get_sum():
    total = 0
    for prod in catalog:
        total += prod["price"]
    # res = "$ " + str(total)
    res = f"${total}"
    return json.dumps(res)

# <id> means it can be whatever endpoint


@app.route("/api/product/<id>")
def get_product(id):
    for prod in catalog:
        if (id == prod["_id"]):
            return prod
    return abort(404)  # 404 = not found


@app.route("/api/product/most_expensive")
def get_most_expensive():
    pivot = catalog[0]
    for prod in catalog:
        if prod["price"] >= pivot["price"]:
            pivot = prod
    return json.dumps(pivot)


@app.route("/api/product/cheapest")
def get_cheapest():
    pivot = catalog[0]
    for prod in catalog:
        if prod["price"] <= pivot["price"]:
            pivot = prod
    return json.dumps(pivot)


@app.route("/api/categories")
def get_categories():
    res = []
    for prod in catalog:
        category = prod["category"]
        if not category in res:
            res.append(category)
        print(prod["category"])

    return json.dumps(res)


@app.route("/api/catalog/<category>")
def products_by_category(category):
    res = []
    cursor = db.products.find({"category" : category})
    for prod in cursor: 
        prod["_id"] = str(prod["_id"])
        res.append(prod)

    # for prod in catalog:
    #     list = prod["title"]
    #     if prod["category"] == category:
    #         res.append(list)
    #     print(prod["title"])

    return json.dumps(res)


savings = []


@app.route("/api/coupons")
def get_coupons():
    return json.dumps(savings)


@app.route("/api/coupons", methods=["POST"])
def save_coupon():
    coupon = request.get_json()
    if not "code" in coupon:
        return abort(400, "Coupon code required")
    if not "discount" in coupon:
        return abort(400, "Discount amount required")
    # save to catalog
    savings.append(coupon)
    # return the product
    return json.dumps(coupon)


@app.route("/api/coupons/<code>")
def get_coupon(code):
    for coupon in savings:
        if (code == coupon["code"]):
            return coupon
    return abort(404)  # 404 = not found


# start the server
app.run(debug=True)
