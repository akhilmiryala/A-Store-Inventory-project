from peewee import *
from datetime import datetime
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

if __name__ == "__main__":
    initialize()

    with open('inventory.csv',newline='') as csvfile:
        product_reader = csv.reader(csvfile,delimiter=',')
        rows = list(product_reader)
        for row in rows:
            Product.create(content=row)

print(db.select())