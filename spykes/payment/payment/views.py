from django.http import HttpResponse
import stripe
from rest_framework.decorators import api_view
from django.conf import settings
from payment.models import PaymentHistory
import json


def generate_response(status: dict, client_secret: str) -> HttpResponse:
    if status == "requires_payment_method":
        print("Requires payment method")
        return HttpResponse(status=400)
    elif status in ["requires_action", "succeeded"]:
        response_data = {
            "client_secret": client_secret,
            "requires_action": status == "requires_action"
        }
    else:
        print("Error {}".format(status))
        return HttpResponse(status=400)

    print("Response: " + str(response_data))
    return HttpResponse(
        status=200,
        content=json.dumps(response_data)
    )


@api_view(['POST'])
def pay_view(request):
    payload = request.body
    payload = json.loads(payload)
    subs_id = payload.get("subs_id")
    pay_id = payload.get("pay_id")

    if not subs_id:
        print("Not subs_id")
        return HttpResponse(status=400)
    if not pay_id:
        print("Not pay_id")
        return HttpResponse(status=400)
    try:
        subs_id = (int(subs_id) + 1) * 100
    except:
        print("Wrong subs_id")
        return HttpResponse(status=400)

    print("Payment: {}".format(subs_id))

    try:
        intent = stripe.PaymentIntent.create(
            api_key=settings.STRIPE_SECRET_KEY,
            amount=subs_id,  # cents
            confirm=True,
            currency="eur",
            payment_method=pay_id,
            use_stripe_sdk=True
        )
    except stripe.error.CardError as ex:
        print("Your card was declined")
        print(str(ex).split(": ")[-1])
        return HttpResponse(status=400)
    except Exception as ex:
        print(type(ex))
        print(ex)
        return HttpResponse(status=400)

    PaymentHistory.objects.create(payment_status=True)

    return generate_response(intent.status, intent.client_secret)


@api_view(['POST'])
def pay_confirm_view(request):
    payload = request.body
    payload = json.loads(payload)
    pay_id = payload.get("pay_id")

    if not pay_id:
        print("Not pay_id")
        return HttpResponse(status=400)

    try:
        intent = stripe.PaymentIntent.confirm(
            api_key=settings.STRIPE_SECRET_KEY,
            payment_method=pay_id
        )
    except stripe.error.CardError as ex:
        print("Your card was declined")
        print(str(ex).split(": ")[-1])
        return HttpResponse(status=400)
    except Exception as ex:
        print(type(ex))
        print(ex)
        return HttpResponse(status=400)

    return generate_response(intent.status, intent.client_secret)
