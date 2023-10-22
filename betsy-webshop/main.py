# Do not modify these lines
__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

# Add your code after this line
import models
from spellchecker import SpellChecker


def main():
    return
    """
        # search("Jcket")
        # search("Coat")
        # search("snowborad")
        # list_user_products(1)
        # list_user_products(3)
        # list_products_per_tag(2)
        # list_products_per_tag(5)
        # add_product_to_catalog(2, product=(name := 'Ski', description := 'pair of old skis used for few years', price_per_unit := 40, quantity := 1, tags := ['sport']))
        # update_stock(4, 8)
        # purchase_product(3, 2, 1)  # 1 x product 3 bought by user 2
        # purchase_product(6, 1, 2)
        # remove_product(6)
    """

# search products containing term (case sensitive)
def search(term):
    # check term for spelling errors
    spell = SpellChecker()
    term_checked = spell.correction(term)
    print(f"checking for {term_checked}")
    query = models.Product.select()
    product_list = []
    for product in query:
        if term_checked in product.name or term_checked in product.description:
            product_list.append(product.name)
    if product_list == []:
        print(f"No matching products found for search: {term_checked}")
        return
    print(product_list)
    return product_list


# View the products of a given user.
# get user.products list
def list_user_products(user_id):
    query = models.User.select()   # .where(models.User.id == user_id)
    user_product_list = []
    for user in query:
        if user.id == user_id:
            for product in user.products:
                user_product_list.append(product.name)
    print(user_product_list)
    return user_product_list


# View all products for a given tag.
def list_products_per_tag(tag_id):
    query = models.Product.select()
    product_tag_list = []
    # add products to list if product.tag matches
    for product in query:
        for tag in product.tags:
            if tag.id == tag_id:
                product_tag_list.append(product.name)
    print(product_tag_list)
    return product_tag_list


# create new product and add to user.products Add a product to a user.
def add_product_to_catalog(user_id, product):
    # create var new product first, create product in model
    print(product)
    # get_or_create() in case product exists?
    new_product = models.Product.create(
        name=product[0],
        description=product[1],
        price_per_unit=product[2],
        quantity=product[3],
    )
    tag_list = []
    for tag in product[4]:
        add_tag, created = models.Tag.get_or_create(name=tag)
        tag_list.append(add_tag)
    print(tag_list)
    new_product.tags.add(tag_list)
    print(new_product)

    # query user model to get user by id and add newest product
    query = models.User.select()
    for user in query:
        if user.id == user_id:
            user.products.add(new_product)


# change product.quantity to new quantity Update the stock quantity of a product.
def update_stock(product_id, new_quantity):
    query = models.Product.update(quantity=new_quantity).where(models.Product.id == product_id)
    query.execute()
    print("updated stock")
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
    user_query = models.User.select()
    product_query = models.Product.select()
    for product in product_query:
        if product.id == product_id:
            # check Product.quantity for sale
            if product.quantity < quantity:
                print("not enough in stock adjust quantity to sell")
                return
            if product.quantity > quantity:
                # create new product with bought quantity
                bought_product = models.Product.create(
                    name=product.name,
                    description=product.description,
                    price_per_unit=product.price_per_unit,
                    quantity=quantity
                )
                # add tags to bough_products
                for tag in product.tags:
                    bought_product.tags.add(tag)
                print(bought_product)
                # update leftover product quantity
                new_quantity = product.quantity - quantity
                update_stock(product_id, new_quantity)
                # < move product x quantity to buyer
                for user in user_query:
                    if user.id == buyer_id:
                        user.products.add(bought_product)
                        models.Transaction.create(buyer=buyer_id, product=product_id, amount=quantity)
                print(f"sold {quantity} amount of {product}")
            if product.quantity == quantity:
                # == move product id from seller to buyer
                for user in user_query:
                    for product in user.products:
                        if product.id == product_id:
                            user.products.remove(product_id)
                # add product to buyer
                for user in user_query:
                    if user.id == buyer_id:
                        user.products.add(product_id)
                # register sale
                models.Transaction.create(buyer=buyer_id, product=product_id, amount=quantity)
                # register_sale.execute()
                print("sold entire stock to buyer")


# Remove a product from a user. Get user if product_id is in User.products and remove
def remove_product(product_id):
    # query = models.Product.delete().where(models.Product.id == product_id)
    # query = models.User.products.remove().where(product_id in models.User.products)
    query = models.User.select()
    for user in query:
        for product in user.products:
            if product.id == product_id:
                user.products.remove(product)
                print(f"removed {product.name} from {user.name}")


if __name__ == "__main__":
    main()
