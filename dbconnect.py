from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["feasto"]  # Ensure database name is correct

# Use a fixed document for storing user details
USERS_DOC_ID = "master_user_log"

def get_restaurants():
    """Fetch restaurant names and images from MongoDB"""
    restaurants = db.restaurants.find({})

    result = {}
    for r in restaurants:
        image_path = r.get("image", "images/default.jpg")  # Use default if image is missing
        result[r["name"]] = {"image": image_path}

    print("Fetched Restaurants:", result)  # Debugging line
    return result

def get_menu_items(restaurant_name):
    """Fetch menu items dynamically from MongoDB with image paths"""
    menu_items = db.menu.find({"restaurant_name": restaurant_name})

    result = []
    for m in menu_items:
        image_path = m.get("image_path", "images/default.jpg")  # Use default if missing
        result.append((
            m.get("order_id", 0),
            m.get("dish_name", "Unnamed"),
            m.get("price", 0),
            m.get("description", "No description"),
            image_path
        ))

    return result

def insert_user_entry(table_number, name, mobile):
    """Insert a new user entry into the database"""
    new_entry = {
        "table_number": table_number,
        "name": name,
        "mobile": mobile,
        "timestamp": datetime.utcnow()
    }

    # Insert into MongoDB collection
    db.users.insert_one(new_entry)
    print("✅ New user entry inserted:", new_entry)

def get_all_user_entries():
    """Return all stored user entries"""
    return list(db.users.find({}, {"_id": 0}))  # Exclude MongoDB's default `_id` field

# Example usage for testing
if __name__ == "__main__":
    insert_user_entry("7", "Aarya", "9876543211")
    all_entries = get_all_user_entries()
    for user in all_entries:
        print(user)
