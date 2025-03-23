from pymongo import MongoClient

# Replace with your MongoDB connection string
MONGO_URI = "mongodb://localhost:27017"  # Change if using MongoDB Atlas
DATABASE_NAME = "feasto"  # Change to your database name
COLLECTION_NAME = "menu"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
menu_collection = db[COLLECTION_NAME]

# Menu data to insert
menu_items = [
    {
        "order_id": 1,
        "restaurant_name": "McDonald's",
        "dish_name": "McAloo Tikki",
        "price": 2,
        "description": "Crispy Potato patty with lettuce, mayo & lots of cheese"
    },
    {
        "order_id": 2,
        "restaurant_name": "McDonald's",
        "dish_name": "McSpicy Paneer",
        "price": 5,
        "description": "Flavourful Paneer layered with lettuce & spicy sauce"
    },
    {
        "order_id": 3,
        "restaurant_name": "McDonald's",
        "dish_name": "McChicken",
        "price": 4,
        "description": "Crispy Chicken patty loaded with mayo &  lettuce"
    },
    {
        "order_id": 4,
        "restaurant_name": "McDonald's",
        "dish_name": "Big Mac",
        "price": 6,
        "description": "Two chicken patties along with our special sauce, lettuce & cheese"
    },
    {
        "order_id": 5,
        "restaurant_name": "McDonald's",
        "dish_name": "McVeggie",
        "price": 3,
        "description": "Delicious Vegetable patty layered with lettuce & mayo"
    },
    {
        "order_id": 6,
        "restaurant_name": "McDonald's",
        "dish_name": "Filet-O-Fish",
        "price": 4,
        "description": "Fish fillets with tartar sauce & cheese"
    },
    {
        "order_id": 7,
        "restaurant_name": "McDonald's",
        "dish_name": "McFlurry Oreo",
        "price": 3,
        "description": "Classic Vanilla ice cream with Oreo crumbles"
    },
    {
        "order_id": 8,
        "restaurant_name": "McDonald's",
        "dish_name": "French Fries",
        "price": 2,
        "description": "Crispy golden fries"
    },
    {
        "order_id": 9,
        "restaurant_name": "McDonald's",
        "dish_name": "McCafé Latte",
        "price": 3,
        "description": "Smooth espresso with steamed milk"
    },
    {
        "order_id": 10,
        "restaurant_name": "McDonald's",
        "dish_name": "Chocolate Shake",
        "price": 4,
        "description": "Rich chocolate milkshake"
    },

    {
        "order_id": 11,
        "restaurant_name": "Domino's",
        "dish_name": "Classic Margarita",
        "price": 19,
        "description": "None required for this one right ?"
    },
    {
        "order_id": 12,
        "restaurant_name": "Domino's",
        "dish_name": "Paneer Pizza",
        "price": 5,
        "description": "Spicy paneer, bell peppers and mushroom topped along with loads of cheese"
    },
    {
        "order_id": 13,
        "restaurant_name": "Domino's",
        "dish_name": "Veggie Supreme",
        "price": 7,
        "description": "Capsicum, onion, olives & cheese"
    },
    {
        "order_id": 14,
        "restaurant_name": "Domino's",
        "dish_name": "Pepperoni Pizza",
        "price": 10,
        "description": "Pepperoni, mozzarella & tomato sauce"
    },
    {
        "order_id": 15,
        "restaurant_name": "Domino's",
        "dish_name": "Garlic Bread",
        "price": 4,
        "description": "Garlic butter, herbs, cheese"
    },

    {
        "order_id": 21,
        "restaurant_name": "Burger King",
        "dish_name": "Whopper",
        "price": 8,
        "description": "Vegetable patty, cheese, lettuce & tomato"
    },
    {
        "order_id": 22,
        "restaurant_name": "Burger King",
        "dish_name": "Crispy Veg Burger",
        "price": 3,
        "description": "Crispy veg patty, lettuce &  mayo"
    },
    {
        "order_id": 23,
        "restaurant_name": "Burger King",
        "dish_name": "Veggie Strips",
        "price": 4,
        "description": "Cheesy & crispy vegetable strips"
    },

    {
        "order_id": 31,
        "restaurant_name": "Starbucks",
        "dish_name": "Caramel Macchiato",
        "price": 4.99,
        "description": "Espresso with steamed milk, vanilla syrup, and caramel drizzle"
    },
    {
        "order_id": 32,
        "restaurant_name": "Starbucks",
        "dish_name": "Caffè Latte",
        "price": 3.99,
        "description": "Smooth espresso blended with steamed milk"
    },
    {
        "order_id": 33,
        "restaurant_name": "Starbucks",
        "dish_name": "Mocha Frappuccino",
        "price": 5.49,
        "description": "Coffee, milk, and ice blended with rich mocha sauce"
    },
    {
        "order_id": 34,
        "restaurant_name": "Starbucks",
        "dish_name": "Pumpkin Spice Latte",
        "price": 5.99,
        "description": "Espresso and steamed milk with pumpkin spice flavors"
    }
]

# Insert data into MongoDB
result = menu_collection.insert_many(menu_items)

# Print inserted IDs
print(f"Inserted {len(result.inserted_ids)} menu items into MongoDB.")
