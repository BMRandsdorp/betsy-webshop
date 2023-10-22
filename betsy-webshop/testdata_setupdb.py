import models
import os


def main():
    delete_database()
    populate_test_database()


def populate_test_database():
    models.db.connect()

    models.db.create_tables(
        [
            models.Tag,
            models.Product,
            models.User,
            models.Transaction,
            models.ProductTags,
            models.UserProduct,
        ]
    )

    tags = [
        "clothes",
        "furniture",
        "antique",
        "art",
        "tools",
        "kitchenwares",
        "vintage",
        "sport",
        ]

    # map tags b4 create to itterate over in product_tags
    tags_map = {
        n: models.Tag.create(name=n)
        for n in tags
    }

    products = [
        ["Jacket", "jacket for winter or ski vacation", 55.5, 1, ["clothes", "sport"]],
        ["Couch", "black leather couch, with some small wear and tear", 179.99, 1, ["furniture", "antique", "vintage"]],
        ["Handmixer", "antique handmixer, still works after years of use", 59.99, 1, ["art", "kitchenwares"]],
        ["Tie dye shirt", "collection of various tie dye tshirts made at woodstock 69", 12.99, 6, ["clothes", "art", "vintage"]],
        ["Stone drill", "electric drill, can be used on concrete and brick walls", 75.50, 1, ["tools"]],
        ["Dining chairs", "chairs to go with dining table", 12.33, 6, ["furniture", "antique"]],
        ["Snowboard", "snowboard used on the slopes for total of a month", 55, 1, ["sport"]],
        ]

    # create map products to make itteratable version
    product_map = {}

    for product_data in products:
        product = models.Product.create(
            name=product_data[0],
            description=product_data[1],
            price_per_unit=product_data[2],
            quantity=product_data[3],
            )

        # fill product map
        product_map[product_data[0]] = product

        product_tags = [tags_map[x] for x in product_data[4]]
        product.tags.add(product_tags)

    users = [
        ["Chris Redfield", "Main str. 102 Raccoon city", "Main ave. 102 Raccoon city", ["Stone drill"]],
        ["Leon S. Kennedy", "Zombie avenue Raccoon city", "White house 1 Washington DC", ["Jacket", "Snowboard"]],
        ["Eric foreman", "Old road 34 Pointplace", "Old road 34 Pointplace", ["Couch", "Tie dye shirt"]],
        ["Tom Nook", "Main Office 102 Desert Isle", "AC head office 1 AC isle", ["Handmixer", "Dining chairs"]]
        ]

    for user_data in users:
        user = models.User.create(
            name=user_data[0],
            address=user_data[1],
            billing_info=user_data[2]
            )
        user_products = [product_map[x] for x in user_data[3]]
        user.products.add(user_products)

    transactions = [
        [1, 0, 1],
        [0, 4, 1],
        ]

    for transaction in transactions:
        models.Transaction.create(
            buyer=transaction[0],
            product=transaction[1],
            amount=transaction[2]
            )

    print("created database")

    models.db.close()


def delete_database():
    cwd = os.getcwd()
    database_path = os.path.join(cwd, "database.db")
    if os.path.exists(database_path):
        os.remove(database_path)
        print("removed db")


if __name__ == "__main__":
    main()
