import models
import session

from werkzeug.security import check_password_hash, generate_password_hash


def check_security():
    local_session = session.SessionLocal()
    emails_banned = ["admin", "developer", "root", "sysadmin", "dev@dev.com", "test", "tester", "admin@admin.com", "admin@localhost", "admin@localdomain"]

    for email in emails_banned:
        user = local_session.query(models.User).filter(models.User.email.contains(email)).first()
        if user:
            print("User {} deleted".format(user.email))
            local_session.delete(user)
            local_session.commit()
    local_session.close()

def init_db():
    models.base.metadata.drop_all(session.engine)
    models.base.metadata.create_all(session.engine)
    create_users()
    create_products()
    create_reviews()

    check_security()


def create_users():
    users = [
        {
            "first_name": "Admin",
            "last_name": "Admin",
            "email": "admin@admin.com",
            "role": "admin",
            "password": "admin",
        },
        {
            "first_name": "João",
            "last_name": "Silva",
            "email": "joao.silva@email.com",
            "role": "admin",
            "password": generate_password_hash("asdasdasd"),
        },
        {
            "first_name": "Maria",
            "last_name": "Santos",
            "email": "maria.santos@email.com",
            "role": "admin",
            "password":  generate_password_hash("sadasdsa"),
        },
        {
            "first_name": "Pedro",
            "last_name": "Ferreira",
            "email": "pedro.ferreira@email.com",
            "role": "client",
            "password":  generate_password_hash("1234"),
        },
        {
            "first_name": "Ana",
            "last_name": "Oliveira",
            "email": "ana.oliveira@email.com",
            "role": "client",
            "password":  generate_password_hash("rasrsa"),
        },
        {
            "first_name": "Rui",
            "last_name": "Pereira",
            "email": "rui.pereira@email.com",
            "role": "client",
            "password":  generate_password_hash("gsdgsdf"),
        },
        {
            "first_name": "Sofia",
            "last_name": "Costa",
            "email": "sofia.costa@email.com",
            "role": "client",
            "password":  generate_password_hash("125as4"),
        },
        {
            "first_name": "Miguel",
            "last_name": "Fonseca",
            "email": "miguel.fonseca@email.com",
            "role": "client",
            "password":  generate_password_hash("sadz5342"),
        },
        {
            "first_name": "Carla",
            "last_name": "Ribeiro",
            "email": "carla.ribeiro@email.com",
            "role": "client",
            "password":  generate_password_hash('s"a42dz'),
        },
        {
            "first_name": "Daniel",
            "last_name": "Martins",
            "email": "daniel.martins@email.com",
            "role": "client",
            "password":  generate_password_hash("5325sad"),
        },
        {
            "first_name": "Isabel",
            "last_name": "Rodrigues",
            "email": "isabel.rodrigues@email.com",
            "role": "client",
            "password":  generate_password_hash("5325asdzxc"),
        },
    ]

    local_session = session.SessionLocal()
    for user in users:
        local_session.add(models.User(**user))
    local_session.commit()
    local_session.close()

def create_products():
    products = [
        {
            "name": "DETI's Cap",
            "description": "Descrição do produto 1",
            "price": 10,
            "image": "cap.png", # "static/images/cap.jpg
            "in_stock": True,
            "stock_quantity": 10,
        },
        {
            "name": "DETI's T-shirt",
            "description": "Descrição do produto 2",
            "price": 20,
            "image": "t-shirt.png", # "static/images/t-shirt.jpg", 
            "in_stock": True,
            "stock_quantity": 20,
        },
        {
            "name": "DETI's Hoodie",
            "description": "Descrição do produto 3",
            "image": "sweat.png", # "static/images/hoodie.jpg
            "price": 30,
            "in_stock": True,
            "stock_quantity": 30,

        },
        {
            "name": "DETI's Mug",
            "description": "Descrição do produto 4",
            "image": "mug.png", # "static/images/mug.jpg
            "price": 40,
            "in_stock": True,
            "stock_quantity": 40,
        },
        {
            "name": "DETI's Socks",
            "description": "Descrição do produto 10",
            "image": "socks.png", # "static/images/socks.jpg
            "price": 100,
            "in_stock": False,
        },
        {
            "name": "DETI's Notebook",
            "description": "Descrição do produto 6",
            "image": "notebook.png", # "static/images/notebook.jpg
            "price": 60,
            "in_stock": True,
            "stock_quantity": 60,
        },
        {
            "name": "DETI's Pen",
            "description": "Descrição do produto 5",
            "price": 50,
            "in_stock": True,
            "stock_quantity": 50,
        },
        {
            "name": "DETI's Mousepad",
            "description": "Descrição do produto 7",
            "price": 70,
            "in_stock": True,
            "stock_quantity": 70,
        },
        {
            "name": "DETI's Keychain",
            "description": "Descrição do produto 8",
            "price": 80,
            "in_stock": True,
            "stock_quantity": 80,
        },
        {
            "name": "DETI's Sticker",
            "description": "Descrição do produto 9",
            "price": 90,
            "in_stock": True,
            "stock_quantity": 90,
        },
    ]
    local_session = session.SessionLocal()
    for product in products:
        local_session.add(models.Product(**product))
    local_session.commit()
    print("Products created")
    local_session.close()

def create_reviews():
    reviews = [
        {
            "user_id": 1,
            "product_id": 1,
            "rating": 5,
            "comment": "Comentário 1",
        },
        {
            "user_id": 2,
            "product_id": 2,
            "rating": 4,
            "comment": "Comentário 2",
        },
        {
            "user_id": 3,
            "product_id": 3,
            "rating": 3,
            "comment": "Comentário 3",
        },
        {
            "user_id": 4,
            "product_id": 4,
            "rating": 2,
            "comment": "Comentário 4",
        },
        {
            "user_id": 5,
            "product_id": 5,
            "rating": 1,
            "comment": "Comentário 5",
        },
        {
            "user_id": 6,
            "product_id": 6,
            "rating": 5,
            "comment": "Comentário 6",
        },
        {
            "user_id": 7,
            "product_id": 7,
            "rating": 4,
            "comment": "Comentário 7",
        },
        {
            "user_id": 8,
            "product_id": 8,
            "rating": 3,
            "comment": "Comentário 8",
        },
        {
            "user_id": 9,
            "product_id": 9,
            "rating": 2,
            "comment": "Comentário 9",
        },
        {
            "user_id": 10,
            "product_id": 10,
            "rating": 1,
            "comment": "Comentário 10",
        },
    ]
    local_session = session.SessionLocal()
    for review in reviews:
        local_session.add(models.Review(**review))
    local_session.commit()
    print("Reviews created")
    local_session.close()
