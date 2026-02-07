# Simple Django E-Commerce Platform

This is a beginner-friendly e-commerce platform I developed while learning Django. It features product listings, shopping cart functionality, and uses Django templates for the frontend. 

The project serves as a hands-on exploration of Django's core features and sets the foundation for much more to come.

## 🚀 Features

- Product catalog with simple styling  
- Add-to-cart functionality (session-based)
- Dynamic routing using Django views and URLs
- Built with Django templates (HTML/CSS)

## 🛠 Tech Stack

- *Backend*: Django (Python)
- *Frontend*: HTML + CSS via Django templates
- *Database*: pstgress
- *Hosting*: Railway (in progress)

## 📦 Installation

1. Clone the repo  
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
2. Set up a virtual environment
   ```bash
    python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies
   ```bash
    pip install -r requirements.txt

3. Run migrations
   ```bash
   python manage.py migrate

4. Start the development server
   ```bash
   python manage.py runserver
   Open your browser at http://127.0.0.1:8000/

🧠 What's Next
I'm planning several big updates:

Razorpay integration for payments

REST API with Django REST Framework
