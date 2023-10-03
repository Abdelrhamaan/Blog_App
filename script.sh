#!/bin/bash

# Start PostgreSQL
service postgresql start

# Wait for PostgreSQL to start (optional, but recommended)
sleep 5

# Create PostgreSQL user and database
# su - postgres
#!/bin/bash

# Start PostgreSQL
service postgresql start

# Wait for PostgreSQL to start (optional, but recommended)
sleep 5

# Create PostgreSQL user and database
su - postgres -c "psql -U postgres -c \"CREATE USER blog WITH SUPERUSER PASSWORD 'blog';\""
su - postgres -c "psql -U postgres -c \"CREATE DATABASE blog;\""
su - postgres -c "psql -U postgres -c \"GRANT ALL PRIVILEGES ON DATABASE blog TO blog;\""

# Activate the virtual environment and run Django migrations
source myenv/bin/activate
cd myblog
python manage.py makemigrations
python manage.py migrate

# Start the Django development server
python manage.py runserver 0.0.0.0:8000

# exit

# Activate the virtual environment and run Django migrations
source myenv/bin/activate
cd myblog
python manage.py makemigrations
python manage.py migrate

# Start the Django development server
python manage.py runserver 0.0.0.0:8000



 
