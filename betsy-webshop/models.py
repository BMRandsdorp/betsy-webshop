# Models go here
import peewee

# db = peewee.SqliteDatabase(":memory:")
db = peewee.SqliteDatabase("database.db")


# tag model
class Tag(peewee.Model):
    name = peewee.CharField(unique=True)

    class Meta:
        database = db


# product model
class Product(peewee.Model):
    name = peewee.CharField()
    description = peewee.CharField()
    price_per_unit = peewee.DecimalField()
    quantity = peewee.IntegerField()
    tags = peewee.ManyToManyField(Tag)

    class Meta:
        database = db


Product.add_index(Product.name, Product.description, Product.tags)
# store price of product, no rounding errors # no duplicate tags


# user model
class User(peewee.Model):
    name = peewee.CharField()
    address = peewee.CharField()
    billing_info = peewee.CharField()
    products = peewee.ManyToManyField(Product)

    class Meta:
        database = db


# transaction model
class Transaction(peewee.Model):
    buyer = peewee.ForeignKeyField(User)
    product = peewee.ForeignKeyField(Product)
    amount = peewee.IntegerField()

    class Meta:
        database = db


ProductTags = Product.tags.get_through_model()
UserProduct = User.products.get_through_model()
