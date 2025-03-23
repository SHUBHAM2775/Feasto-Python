from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")  # Update with your MongoDB URI
db = client["feasto"]
collection = db["menu"]

starbucks_menu = [
    {"order_id": 10, "restaurant_name": "Starbucks", "dish_name": "Caramel Macchiato", "price": 4.99, "description": "Espresso with steamed milk, vanilla syrup, and caramel drizzle"},
    {"order_id": 11, "restaurant_name": "Starbucks", "dish_name": "Caffè Latte", "price": 3.99, "description": "Smooth espresso blended with steamed milk"},
    {"order_id": 12, "restaurant_name": "Starbucks", "dish_name": "Mocha Frappuccino", "price": 5.49, "description": "Coffee, milk, and ice blended with rich mocha sauce"},
    {"order_id": 13, "restaurant_name": "Starbucks", "dish_name": "Pumpkin Spice Latte", "price": 5.99, "description": "Espresso and steamed milk with pumpkin spice flavors"}
]

collection.insert_many(starbucks_menu)
print("Starbucks menu added successfully!")
