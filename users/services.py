import stripe

from config.settings import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY


def create_stripe_product(course_title):
    """Создаём продукт в Stripe и возвращаем ID продукта."""
    stripe_product = stripe.Product.create(name=course_title)
    return stripe_product["id"]


def create_stripe_price(course_price, stripe_product_id):
    """Создаём цену для указанного продукта и возвращаем ID цены."""
    stripe_price = stripe.Price.create(
        currency="rub",
        unit_amount=round(course_price * 100),
        product=stripe_product_id,
    )
    return stripe_price["id"]


def create_stripe_session(stripe_price_id):
    """Создаёт Checkout Session для указанной цены."""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/payment-success/",
        cancel_url="http://127.0.0.1:8000/payment-cancelled/",
        line_items=[
            {
                "price": stripe_price_id,
                "quantity": 1,
            }
        ],
        mode="payment",
    )
    return session["id"], session["url"]


# Пример полного использования
def initiate_payment(course_title, course_price):
    """Функция для инициализации всей цепочки операций:"""
    try:
        product_id = create_stripe_product(course_title)
        price_id = create_stripe_price(course_price, product_id)
        session_id, session_url = create_stripe_session(price_id)
        return {"session_id": session_id, "session_url": session_url}
    except stripe.error.StripeError as e:
        print(f"Ошибка Stripe: {e}")
        return None
