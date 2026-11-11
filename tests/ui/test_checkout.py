from playwright.sync_api import Page, expect
from pages.cart_page import CartPage
from pages.products_page import ProductsPage
from pages.checkout_page import CheckoutPage

def test_full_checkout(logged_in_page: Page):
    products_page = ProductsPage(logged_in_page)
    products_page.add_to_cart("Sauce Labs Backpack")
    products_page.open_cart()


    cart_page = CartPage(logged_in_page)
    expect(cart_page.cart_items).to_have_count(1)
    cart_page.go_to_checkout()


    checkout_page = CheckoutPage(logged_in_page)
    checkout_page.fill_information("Test", "User", "M5V 2T6")
    checkout_page.finish_order()

    expect(checkout_page.complete_header).to_have_text("Thank you for your order!")
    
