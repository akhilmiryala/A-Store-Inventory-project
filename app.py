from peewee import *
from datetime import datetime
from collections import OrderedDict
import csv

db = SqliteDatabase('inventory.db')

class Product(Model):
    product_id = AutoField(primary_key=True)
    product_name = TextField(default="")
    product_quantity = IntegerField(default=0)
    product_price = IntegerField(default=0)
    date_updated = DateTimeField(default=0)

    class Meta:
        database = db

def initialize():
    db.connect()
    db.create_tables([Product],safe=True)


def read_in_csv_data():
    with open('inventory.csv',newline='') as csvfile:
        product_reader = csv.DictReader(csvfile,delimiter=',')
        product_list = list(product_reader)
        return product_list

def add_csv_data_to_database():
    product_list = read_in_csv_data()
    for product in product_list:
        Product.create( product_name = product['product_name'],
                        product_price = product['product_price'],
                        product_quantity = product['product_quantity'],
                        date_updated = product['date_updated'])


def menu_loop():
    menu_choice = None
    while menu_choice != 'q':
        print("Enter 'q' to quit.")
        for key,value in menu.items():
            print(f'{key}) {value.__doc__}')
        menu_choice = input('Action: ').lower().strip()

        if menu_choice in menu:
            menu[menu_choice]()


def add_product():
    """Add a product"""
    product_name = input("Enter the name of the product: ")
    product_price = input("Enter price of product without '$' and decimal: ")
    product_price = int(product_price)
    product_price = convert_price_to_cents(product_price)
    product_quantity = input("Enter the product quantity: ")
    date_string = input("Enter the date updated in Month/Day/Year format: ")
    date_updated = datetime.strptime(date_string,'%m/%d/%Y')
    if input('Enter Product? [Yn]  '.lower()) != 'n':
        Product.create( product_name = product_name,
                        product_price = product_price,
                        product_quantity = product_quantity,
                        date_updated = date_updated)
        print("Product added successfully!")

    
def convert_price_to_cents(price):
    price = float(price)
    price = price/100
    price = str(price)
    price = '$' + price
    return price


def view_product():
    """Display a product"""
    next_action = None
    
    input_product_id = input("Enter id of product you wish to view: ")
    input_product_id = int(input_product_id)
    products = Product.select()

    for product in products:
        if product.product_id == input_product_id:
            print(f"product_name: {product.product_name}")
            print(f'product_quantity: {product.product_quantity}')
            print(f'product_price: {product.product_price}')
            print(f'date_updated: {product.date_updated}')
            return
    print('Product not found.')


def backup_database():
    """Backup Database"""
    with open('product_list_backup.csv','a') as csvfile:
        fieldnames = ['product_name','product_price','product_quantity','date_updated']
        product_writer = csv.DictWriter(csvfile,fieldnames = fieldnames)
        products = Product.select()
        product_writer.writeheader()
        for product in products:
            product_writer.writerow({
                'product_name': product.product_name,
                'product_quantity': product.product_quantity,
                'product_price': product.product_price,
                'date_updated': product.date_updated

            })

menu = OrderedDict([
    ('a',add_product),
    ('v',view_product),
    ('b',backup_database)
])

if __name__ == "__main__":
    initialize()
    add_csv_data_to_database()
    menu_loop()