from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["feasto"]  # Ensure this matches your database name

def get_restaurants():
    """Fetch restaurant names and images from MongoDB"""
    restaurants = db.restaurants.find({})
    
    result = {}
    for r in restaurants:
        image_path = r.get("image", "images/default.jpg")  # Default if missing
        result[r["name"]] = {"image": image_path}

    return result

def get_menu_items(restaurant_name):
    """Fetch menu items dynamically from MongoDB with image paths"""
    menu_items = db.menu.find({"restaurant_name": restaurant_name})

    result = []
    for m in menu_items:
        image_path = m.get("image_path", "images/default.jpg")  # Use default if missing
        result.append((m["order_id"], m["dish_name"], m["price"], m["description"], image_path))

    return result
