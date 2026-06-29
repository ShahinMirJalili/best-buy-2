import products
import store
import promotions


def list_products(store_obj):
    all_products = store_obj.get_all_products()
    print("------")
    number = 1
    for product in all_products:
        print(f"{number}. ", end="")
        product.show()
        number += 1
    print("------")


def show_total(store_obj):
    print(f"Total of {store_obj.get_total_quantity()} items in store")


def make_order(store_obj):
    all_products = store_obj.get_all_products()
    list_products(store_obj)
    print("When you want to finish order, enter empty text.")

    shopping_list = []
    while True:
        product_choice = input("Which product # do you want? ")
        amount = input("What amount do you want? ")
        if product_choice == "" or amount == "":
            break
        try:
            product = all_products[int(product_choice) - 1]
            shopping_list.append((product, int(amount)))
            print("Product added to list!\n")
        except (ValueError, IndexError):
            print("Error adding product, try again!\n")

    if shopping_list:
        try:
            total = store_obj.order(shopping_list)
            print(f"********\nOrder made! Total payment: ${total}")
        except ValueError as error:
            print(f"Error while making order! {error}")


def start(store_obj):
    while True:
        print("\n   Store Menu")
        print("   ----------")
        print("1. List all products in store")
        print("2. Show total amount in store")
        print("3. Make an order")
        print("4. Quit")
        choice = input("Please choose a number: ")

        if choice == "1":
            list_products(store_obj)
        elif choice == "2":
            show_total(store_obj)
        elif choice == "3":
            make_order(store_obj)
        elif choice == "4":
            break
        else:
            print("Error with your choice! Try again!")


def main():
    mac = products.Product("MacBook Air M2", price=1450, quantity=100)
    bose = products.Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    pixel = products.Product("Google Pixel 7", price=500, quantity=250)
    windows = products.NonStockedProduct("Windows License", price=125)
    shipping = products.LimitedProduct("Shipping", price=10, quantity=250, maximum=1)

    second_half_price = promotions.SecondHalfPrice("Second Half price!")
    third_one_free = promotions.ThirdOneFree("Third One Free!")
    thirty_percent = promotions.PercentDiscount("30% off!", percent=30)

    mac.set_promotion(second_half_price)
    bose.set_promotion(third_one_free)
    windows.set_promotion(thirty_percent)

    product_list = [mac, bose, pixel, windows, shipping]
    best_buy = store.Store(product_list)
    start(best_buy)


if __name__ == "__main__":
    main()
