from flask import Flask, jsonify, request 

app= Flask(__name__)

#voy a empezar a crear rutas, 
# vamos a primero llamar la otra carpeta
from products import products
#hago la ruta, cuando el servidor pida la ruta localhost:5000/ping va a devolver algo
@app.route('/ping')
def ping():
    return "pong!"
#pero yo quiero que me devuelva un json , jsonify lo que hace es convierte todo a json
@app.route("/ping1")
def ping1():
    return jsonify({'message':'pong!'})


#por defecto siempre el route es con GET que es la peticion
#POST= guardar datos
#PUT = actualizar datos
#DELETE = borrar datos
@app.route('/products',methods=['GET'])
#def getProducts():
#    return jsonify(products)
#podria devolver la lista adentro de una propiedad
def getProductss():
    return jsonify({"productos":products,"mensage":"aca tenes la lista de productos"})

#me va a devolver solo el producto que quiero (el string me sirve para decir que si o si tiene que ser string)
@app.route("/products/<string:product_name>")
def getProducts(product_name):
    #print(product_name) me devuelve en la consola lo que buscan en la url, me sirve para ver si funciona la variable
    productoFound= [products for products in products if products["name"]== product_name]
    if productoFound:
        return jsonify({'elProducto':productoFound[0]})
    return jsonify({"mensaje":"producto no encontrado"})

@app.route('/products',methods=['POST'])
def addProduct():
    print(request.json)
    new_product= {
        "name": request.json['name'],
        "price":request.json['price'],
        "quantity":request.json['quantity']
    }
    products.append(new_product)
    return jsonify({"message":"Product Added Succesfully", "products":products})

@app.route('/products/<string:product_name>',methods=['PUT'])
def editProdcut(product_name):
    productoEncontrado=[products for products in products if products["name"]==product_name]
    if product_name:
        productoEncontrado[0]["name"]= request.json['name']
        productoEncontrado[0]["price"]= request.json['price']
        productoEncontrado[0]["quantity"]= request.json['quantity']
        return jsonify({
            "message": "producto actualizado",
            "product": productoEncontrado[0]
        })
    return jsonify({"message":"product no found"})


@app.route('/products/<string:product_name>',methods=["DELETE"])
def deleteProduct(product_name):
    productFound=[product for product in products if product["name"]==product_name]
    if productFound:
        products.remove(productFound[0])
        return jsonify({
            "message":"producto Deleted",
            "products": products
        })
    return jsonify({"message":"Product not found"})
#inicio el servidor
#debug permite decir que si hay un cambio se reinicie
if __name__ =="__main__":
    app.run(debug=True,port=5000)