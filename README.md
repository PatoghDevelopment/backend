# TickSy Server

## Get Start :

#### **1. git clone https://github.com/PatoghDevelopment/backend.git** (terminal)

#### **2. pip install -r requirements.txt** (terminal, with active virtualenv)

#### **3. create database with this info:**  (mysql)

    'NAME': 'patogh_db'
    
    'USER': 'user'
    
    'PASSWORD': '123'
    
    - Set the **Charset to utf8mb4**, and **Collaction to utf8mb4_general** when creating database in mysql.

##### **3.1. for convenience :**

    CREATE USER 'user'@'%' IDENTIFIED BY '123';
    
    GRANT ALL PRIVILEGES ON *.* TO 'user'@'%';
    
    CREATE DATABASE patogh_db DEFAULT CHARACTER SET utf8mb4  DEFAULT COLLATE utf8mb4_general_ci;


#### **4. python manage.py makemigrations** (terminal)

#### **5. python manage.py migrate** (terminal)

#### **6. python manage.py runserver** (terminal)

- **Admin panel**:
    - http://localhost:8000/admin/ 
- **API Documentation**: (pick one)
    - http://localhost:8000/swagger/
    - http://localhost:8000/redoc/

## Done!
