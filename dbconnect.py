from pymongo import MongoClient

def get_restaurants():
    """Fetch restaurant data from MongoDB."""
    client = MongoClient("mongodb://localhost:27017/")  # Adjust if needed
    db = client["feasto"]  # Database name
    collection = db["restaurants"]  # Collection name

    restaurants_data = {}
    for doc in collection.find():
        restaurants_data[doc["name"]] = {
            "image": doc["image_path"],  
            "menu": doc["menu_items"]    
        }
    return restaurants_data
