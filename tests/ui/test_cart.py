from playwright.sync_api import Page, expect
from pages.products_page import ProductsPage

def test_add_backpack_to_cart(logged_in_page: Page):
    product_page = ProductsPage(logged_in_page)
    product_page.add_to_cart("Sauce Labs Backpack")

    expect(product_page.cart_badge).to_have_text("1")