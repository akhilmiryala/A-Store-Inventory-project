from peewee import *
from datetime import datetime
import csv

db = SqliteDatabase('inventory.db')

class Product(Model):
    product_id = AutoField(primary_key=True)
    product_name = CharField(max_length = 255)
    product_quantity = IntegerField()
    product_price = IntegerField()
    date_updated = DateTimeField()

    class Meta:
        database = db

if __name__ == "__main__":
    db.connect()
    db.create_tables([Product],safe=True)

    with open('inventory.csv',newline='') as csvfile:
        product_reader = csv.reader(csvfile,delimiter=',')
        rows = list(product_reader)
        for row in rows:
            Product.create(content=row)