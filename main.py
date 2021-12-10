from prettytable import PrettyTable
import mysql.connector as sq
import os

fields = [' Item Type', 'Company', 'Quantity', 'Price Per Unit']


def heading():
    print("------ Welcome to Kings Store ------\n\n")


def main_menu():
    print("Press (1) to see the list of item available to buy")
    print("Press (2) to buy items from the store")
    print("Press (3) to exit the program")


def show_list():
    conn = sq.connect(host='localhost', user='root',
                      password='student', database='shop')
    cursor = conn.cursor()

    item_table = PrettyTable()
    item_table.field_names = fields

    cursor.execute(f"SELECT * FROM items")
    data = cursor.fetchall()

    conn.commit()
    conn.close()

    for item, company, qty, price in data:
        item_table.add_row([item, company, qty, price])

    print(f"\n{item_table}\n")


def validate_item_qty(type, company, quantity):
    conn = sq.connect(host='localhost', user='root',
                      password='student', database='shop')
    cursor = conn.cursor()

    cursor.execute(
        f"SELECT * FROM items WHERE type = '{type}' and company = '{company}'")
    data = cursor.fetchone()

    conn.close()

    if data is None:
        return 'Item not found'

    else:
        if quantity < data[2]:
            return 'Validated'
        else:
            return 'Quantity exceeded'


def calculate_amount(dict):
    conn = sq.connect(host='localhost', user='root',
                      password='student', database='shop')
    cursor = conn.cursor()
    amount = 0
    for item in dict:
        company = dict[item][0]
        qty = dict[item][1]

        cursor.execute(
            f"SELECT price FROM items WHERE type = '{item}' and company = '{company}'")
        price_data = int(cursor.fetchone()[0])
        price = price_data * qty
        amount += price
        update_quantity(item, company, qty)

    else:
        conn.close()
        return amount


def update_quantity(item, company, qty):

    conn = sq.connect(host='localhost', user='root',
                      password='student', database='shop')
    cursor = conn.cursor()

    cursor.execute(
        f"SELECT qty from items WHERE type = '{item}' and company = '{company}'")
    table_qty = int(cursor.fetchone()[0])

    set_qty = table_qty - qty

    cursor.execute(
        f"UPDATE items SET quantity = '{set_qty}' WHERE type = '{item}' and company = '{company}'")
    conn.commit()
    conn.close()


def make_user_items_table(dict):

    item_table = PrettyTable()
    item_table.field_names = ['Item Type', 'Company', 'Quantity']

    for item in dict:
        item_table.add_row(item, dict[item][0], dict[item][1])

    print(item_table)


def buy_main():
    conn = sq.connect(host='localhost', user='root',
                      password='student', database='shop')
    cursor = conn.cursor()

    print("You chose to buy from the store.")
    print("NOTE : Once an item is bought it can't be returned or refunded.")

    user_items = {}

    while True:
        show_list()

        user_item = input("Enter the item type from the above table : ")
        user_company = input("Enter the company name you want to buy from : ")
        user_qty = input("Enter the qty you want to buy : ")

        item_validation = validate_item_qty(user_item, user_company, user_qty)

        if item_validation == 'Item not found':
            print("\nThe Entered Item is not found please. Try Again\n")
            continue

        elif item_validation == 'Quantity exceeded':
            print(
                "\nThe Entered quantity of the item is not available. Please Enter less quantity")
            continue

        elif item_validation == 'Validated':
            user_items[user_item] = (user_company, user_qty)
            print("\nItem Added successfully.\n")

            user_input = input("\nDo you want to buy more items (Y / N): ")

            if user_input in ['y', 'Y']:
                print("\nYou chose to buy another item\n")
                continue

            else:
                if len(user_items) == 0:
                    print(
                        "\nYou didn't add any items to purchase. You purchase has been cancelled")
                    break

                else:
                    print("\nThe following items are to be purchased from store by you")
                    make_user_items_table(user_items)
                    user_confirm = input(
                        "\nDo you want to complete the purchase of the following items (Y / N): ")
                    if user_confirm in ['y', 'Y']:
                        amount = calculate_amount(user_items)
                        print(
                            f"The total amount of your purchase is rupees {amount}")
                        print(f"Please collect cash and take your items")
                        print(f"Thank you for shopping with us. Have a nice day.")
                        exit()

                    else:
                        print(
                            "You chose to cancel the order. All the items that you added will be deleted")
                        exit()


os.system('cls')
heading()
while True:

    main_menu()

    user_dict = {
        '1': show_list,
        '2': buy_main,
    }

    user_input = input("Please Enter your choice from the above options: ")

    if user_input in user_dict:
        user_dict[user_input]()

    elif user_input == '3':
        print("\nYou chose to exit the program")
        print("Thank you for using our program\n")
        exit()

    else:
        print("\nYou have entered and invalid input. Please try again\n")
        continue
