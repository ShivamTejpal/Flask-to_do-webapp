from flask import Flask, app,redirect,render_template,request
import stripe

app = Flask(__name__)


YOUR_DOMAIN = 'https:localhost:4242'


@app.route('/pay.html',methods=['POST'])
def create_checkout_session():
    try:
        stripe.api_key = 'sk_test_51OSkScSAhF7pBZltcCADRAZDjHBrenKc9P6uZB0RVyAonzZW3M5T8V5u6IUv3KPcekvMQcCZril5AnsMDf8e37gi00s6yXRbMo'
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='payment',
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': 1000,
                        'product_data': {
                            'name': 'Pro license'
                        },
                        'quantity': 1
                    },
                    'quantity': 1
                }
            ],
            success_url=YOUR_DOMAIN + '/success',
            cancel_url=YOUR_DOMAIN + '/cancel'
        )
        return redirect(session.url)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(port=4242, debug=True)