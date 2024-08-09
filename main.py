from app import create_app
from app.models import setup_database
import os

# Ensure uploads directory exists
os.makedirs('uploads', exist_ok=True)

# Setup the database if it doesn't exist
setup_database()

# Create and run the app
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
