# Do not modify these lines
__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

# Add your code after this line
import models
# import peewee


# search products containing term (case sensitive)
def search(term):
    query = models.Product.select()
    product_list = []
    for product in query:
        if term in product.name:
            product_list.append(product)
    if product_list == []:
        print("No matching term found")
    print(product_list)
    return product_list


# View the products of a given user.
# get user.products list
def list_user_products(user_id):
    query = models.User.select()
    user_product_list = []
    for user in query[user_id]:
        user_product_list.append(user.products)
    print(user_product_list)
    return user_product_list


# View all products for a given tag.
# get products list if product.tag is in product
def list_products_per_tag(tag_id):
    query = models.Product.select()
    product_tag_list = []
    for product in query:
        if tag_id in product.tags:
            product_tag_list.append(product)
    print(product_tag_list)
    return product_tag_list


# create new product and add to user.products Add a product to a user.
def add_product_to_catalog(user_id, product):
    # create var new product first, create product in model
    new_product = models.Product.create(product)
    # get_or_create() in case product exists?
    # new_product = models.Product.get_or_create(product)

    # query user model to get user by id and add newest product
    query = models.User.select()
    for user in query[user_id]:
        user.products.add(new_product)


# change product.quantity to new quantity Update the stock quantity of a product.
def update_stock(product_id, new_quantity):
    query = models.Product.update(quantity=new_quantity).where(models.Product.id == product_id)
    query.execute()
    """
        # query = models.Product.select()
        print(query[product_id])

        for product in query[product_id]:
            product.quantity = new_quantity

        # print(query[product_id])
    """


# Handle a purchase between a buyer and a seller for a given product
# move product x amount to buyer from seller and register amount in transaction model
def purchase_product(product_id, buyer_id, quantity):
    # register sale var to call
    register_sale = models.Transaction.create(
        buyer=buyer_id,
        product=product_id,
        amount=quantity
        )

    buyer_query = models.User.select()
    # check Product.quantity for sale
    product_query = models.Product.select()
    for product in product_query[product_id]:
        if product.quantity > quantity:
            # > give error
            print("not enough in stock adjust quantity to sell")
            return
        if product.quantity < quantity:
            # < move product x quantity to buyer
            for user in buyer_query[buyer_id]:
                user.products.add(product_id)
            register_sale.execute()
            print(f"sold {quantity} amount of product")
        if product.quantity == quantity:
            # == move product id from seller to buyer
            # remove product from seller
            models.User.products.delete().where(product_id in models.User.products)
            # add product to buyer
            for user in buyer_query[buyer_id]:
                user.products.add(product_id)
            # register sale
            register_sale.execute()
            print("sold entire stock to buyer")


# Remove a product from a user. Get user if product_id is in User.products and remove
def remove_product(product_id):
    # query = models.Product.delete().where(models.Product.id == product_id)
    query = models.User.products.delete().where(product_id in models.User.products)
    query.execute()

if __name__ == "__main__":
    search("Jacket")
    search("Coat")
    list_user_products(1)
    list_products_per_tag(2)
    add_product_to_catalog(2, (name="Ski's", description="pair of old ski's used for few years", price_per_unit=40, quantity=1, tags=["sport"]))
    update_stock(4, 4)
    purchase_product(3, 2, 1)
    remove_product(1)
