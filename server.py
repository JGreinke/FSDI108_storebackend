#  this is the actual back end server
from flask import Flask, abort
from mock_data import catalog
from about_me import me, test
import json 

app = Flask("server")


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
    return json.dumps(catalog)
    # this will parse the catalog and return it as a json string

@app.route("/api/catalog/count")
def catalog_count():
    count = len(catalog)
    return json.dumps(count)

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
    return abort(404) # 404 = not found

@app.route("/api/product/most_expensive")
def get_most_expensive():
    pivot = catalog[0]

    for prod in catalog: 
        if prod["price"] >= pivot["price"]:
            pivot = prod
    return json.dumps(pivot)



# start the server
app.run(debug=True)