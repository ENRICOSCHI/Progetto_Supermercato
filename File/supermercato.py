import threading
import random
import time
import json
import xml.etree.ElementTree as ET

class Supermarket:
    def __init__(self, products_file, cash_file):
        self.products_file = products_file
        self.cash_file = cash_file
        self.products = self.load_products()
        self.cash = {"cash1": 0, "cash2": 0, "cash3": 0}
        self.cash_locks = {"cash1": threading.Lock(), "cash2": threading.Lock(), "cash3": threading.Lock()}

    def load_products(self):
        try:
            with open(self.products_file, 'r') as file:
                if self.products_file.endswith('.json'):
                    return json.load(file)
                elif self.products_file.endswith('.xml'):
                    root = ET.parse(file).getroot()
                    products = {}
                    for product in root:
                        products[product.attrib['name']] = int(product.text)
                    return products
        except FileNotFoundError:
            print(f"File {self.products_file} not found. Exiting.")
            exit()

    def save_cash(self):
        cash_file_format = 'json' if self.cash_file.endswith('.xml') else 'xml'
        with open(self.cash_file, 'w') as file:
            if cash_file_format == 'json':
                json.dump(self.cash, file, indent=2)
            elif cash_file_format == 'xml':
                root = ET.Element('cash')
                for cash, amount in self.cash.items():
                    ET.SubElement(root, cash).text = str(amount)
                tree = ET.ElementTree(root)
                tree.write(file)

    def purchase_product(self, product, quantity):
        if product in self.products and self.products[product] >= quantity:
            self.products[product] -= quantity
            return True
        return False

    def ask_for_product_location(self, product):
        print(f"Customer asks for the location of '{product}' to a store clerk.")

    def put_back_product(self, product, quantity):
        if product in self.products:
            self.products[product] += quantity

    def checkout(self, cash_register, total_amount):
        with self.cash_locks[cash_register]:
            self.cash[cash_register] += total_amount

def customer_behavior(customer_id, supermarket):
    cart = {}
    for _ in range(5):  # Simulating customer shopping for 5 products
        event = random.randint(1, 3)
        if event == 1:  # Acquista un prodotto disponibile
            product = random.choice(list(supermarket.products.keys()))
            quantity = random.randint(1, 3)
            if supermarket.purchase_product(product, quantity):
                if product in cart:
                    cart[product] += quantity
                else:
                    cart[product] = quantity
            time.sleep(2)
        elif event == 2:  # Chiedi dove si trova un prodotto ad un commesso
            product = random.choice(list(supermarket.products.keys()))
            supermarket.ask_for_product_location(product)
            time.sleep(2)
        elif event == 3:  # Riponi un prodotto del tuo carrello a posto perché sbagliato
            if cart:
                product = random.choice(list(cart.keys()))
                quantity = random.randint(1, cart[product])
                cart[product] -= quantity
                if cart[product] == 0:
                    del cart[product]
                supermarket.put_back_product(product, quantity)
            time.sleep(2)

    time.sleep(6)  # Solo dopo che siano passati 6 secondi, il cliente si dirige in cassa
    cash_register = f"cash{random.randint(1, 3)}"
    total_amount = sum(supermarket.products[product] for product in cart)
    supermarket.checkout(cash_register, total_amount)
    print(f"Customer {customer_id} completed the checkout at Cash Register {cash_register} with total amount {total_amount}.")
    print(f"Updated products in the supermarket: {supermarket.products}")
    supermarket.save_cash()

if __name__ == "__main__":
    products_file = "magazzino.json"  # Replace with your product file name (json or xml)
    cash_file = "magazzino.xml"  # Replace with your cash file name (json or xml)

    supermarket = Supermarket(products_file, cash_file)

    # Simulate 10 customers
    for i in range(10):
        customer_thread = threading.Thread(target=customer_behavior, args=(i+1, supermarket))
        customer_thread.start()

    # Wait for all customer threads to finish
    for thread in threading.enumerate():
        if thread != threading.current_thread():
            thread.join()
