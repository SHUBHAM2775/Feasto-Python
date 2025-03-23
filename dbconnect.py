from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["feasto"]  # Replace with your actual DB name

def get_restaurants():
    """Fetch restaurant names and images from MongoDB"""
    restaurants = db.restaurants.find({})
    result = {r["name"]: {"image": r["image"]} for r in restaurants}
    print("Fetched Restaurants:", result)  # Debugging line
    return result

def get_menu_items(restaurant_name):
    """Fetch menu items dynamically from MongoDB"""
    menu_items = db.menu.find({"restaurant_name": restaurant_name})
    return [(m["order_id"], m["dish_name"], m["price"], m["description"]) for m in menu_items]
