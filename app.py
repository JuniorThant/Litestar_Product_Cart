from litestar import Litestar, get, post,delete,patch
from modal import Product
from connect import products
from bson.objectid import ObjectId 

@get("/")
async def index() -> str:
    return "This server is running on port 8000"

#retrieve all the products
@get("/products")
async def get_products() -> list[dict]:
    return[
        {"id": str(product["_id"]), "name": product["name"], "description":product["description"],"price":product["price"], "quantity": product["quantity"]}
        for product in products.find() #retrieve the products from mongodb and return
    ]

#retrieve the product by id
@get("/products/{id:str}")
async def product_details(id:str)->dict:
    product=products.find_one({"_id":ObjectId(id)}) #find the product that match with object id from mongodb
    return {"id": str(product["_id"]), "name": product["name"],"description":product["description"],"price":product["price"], "quantity": product["quantity"]}

#add new product
@post("/products/add")
async def add_product(data: Product) -> Product:
    new_product = Product( name=data.name, description=data.description, price=data.price, quantity=data.quantity) #add new product into modal
    products.insert_one(new_product.__dict__) #add new product into mongodb as dictionary
    return new_product

#delete product by id
@delete("/products/{id:str}",status_code=200)
async def delete_product(id:str)->dict:
    product=products.find_one_and_delete({"_id":ObjectId(id)}) #find the product by id and delete
    return {"message":"Product Deleted Successfully"}

#increase product quantity by id
@patch("/products/{id:str}/increase")
async def increase_product(id:str)->dict:
    #update product by id #mongo db aggregation to increase quantity #return document to keep the data updated
    updated_product=products.find_one_and_update({"_id":ObjectId(id)},{"$inc":{"quantity":1}},return_document=True)
    product=Product(name=updated_product["name"],description=updated_product["description"],price=updated_product["price"],quantity=updated_product["quantity"])
    return{
        "message":"Product Quantity Increased Successfully",
        "updated_product":{"id": str(updated_product["_id"]),"name":product.name,"quantity":product.quantity}
    }

#decrease product quantity by id
@patch("/products/{id:str}/decrease")
async def decrease_product(id:str)->dict:
    #update product by id #mongo db aggregation to decrease quantity #return document to keep the data updated
    updated_product=products.find_one_and_update({"_id":ObjectId(id)},{"$inc":{"quantity":-1}},return_document=True)
    product=Product(name=updated_product["name"],description=updated_product["description"],price=updated_product["price"],quantity=updated_product["quantity"])
    return{
        "message":"Product Quantity Decreased Successfully",
        "updated_product":{"id": str(updated_product["_id"]),"name":product.name,"quantity":product.quantity}
    }

#running the application by calling the above controller functions
app = Litestar(route_handlers=[index, get_products, add_product,product_details,delete_product,increase_product,decrease_product])
