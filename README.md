
# Feasto - Restaurant Food Ordering System

A comprehensive Python desktop application for restaurant food ordering with intuitive GUI interface, complete user management system, and integrated payment processing. Developed as a college project demonstrating full-stack development skills.

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![MongoDB](https://img.shields.io/badge/Database-MongoDB-brightgreen.svg)

## 🚀 Key Features

### User Management
- **Authentication System** - Secure user registration and login with input validation
- **Table Assignment** - Dynamic table number assignment for restaurant seating
- **User Profile** - Personal user dashboard with order history

### Restaurant & Menu System
- **Multi-Restaurant Support** - Browse multiple restaurants with visual interface
- **Dynamic Menu Loading** - Real-time menu fetching from MongoDB database
- **Item Management** - Add/remove items with quantity controls

### Payment Integration
- **UPI Payments** - Google Pay, PhonePe, Paytm QR code integration
- **Card Processing** - Credit/Debit card payment with validation
- **Loyalty System** - Feasto Points rewards with discount options
- **Bill Generation** - Detailed billing with GST calculation

### Order Management
- **Shopping Cart** - Advanced cart operations with persistence
- **Order Tracking** - Real-time status updates with countdown timer
- **Receipt System** - Digital order confirmation and tracking

## 🛠️ Technology Stack

- **Frontend**: Python Tkinter (GUI Framework)
- **Backend**: Python 3.x
- **Database**: MongoDB (NoSQL Database)
- **Image Processing**: Pillow (PIL)
- **Payment**: UPI QR Code Integration

## 📋 Installation & Setup

1. **Prerequisites**
   - Python 3.x
   - MongoDB Server

2. **Clone Repository**
   ```bash
   git clone https://github.com/SHUBHAM2775/Feasto-Python.git
   cd Feasto-Python
   ```

3. **Install Dependencies**
   ```bash
   pip install pymongo pillow
   ```

4. **Database Setup**
   - Start MongoDB server
   - Run `menu_db.py` to populate sample data

5. **Launch Application**
   ```bash
   python main.py
   ```

## 🎯 Project Highlights

- **Modular Architecture** - Clean separation of concerns with dedicated modules
- **Database Integration** - Complete CRUD operations with MongoDB
- **User Experience** - Intuitive GUI with professional design
- **Payment Processing** - Multiple payment gateway integration
- **Error Handling** - Comprehensive input validation and error management

## 📁 Project Structure

```
├── main.py              # Application entry point
├── home.py              # Authentication interface
├── resto.py             # Restaurant selection
├── menu.py              # Menu browsing
├── checkout.py          # Cart management
├── pay.py               # Payment gateway
├── order_status.py      # Order tracking
├── dbconnect.py         # Database operations
└── images/              # UI assets
```

## � Team


**[Team Member Name]**  
GitHub: [@S-Nitya](https://github.com/S-Nitya)

**[Team Member Name]**  
GitHub: [@siddhi-ms](https://github.com/siddhi-ms)

**Shubham Upadhyay**  
GitHub: [@SHUBHAM2775](https://github.com/SHUBHAM2775)
---
*A collaborative college project showcasing Python GUI development, database integration, and payment system implementation.*
