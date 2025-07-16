from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Payment  # 👈 modelni chaqirishni unutmang
import hashlib, json

@csrf_exempt
def fake_click(request):
    if request.method == "POST":
        data = request.POST
        click_trans_id = data.get("click_trans_id", "123456")
        service_id = data.get("service_id", "1")
        order_id = data.get("merchant_trans_id", "ORDER123")
        amount = data.get("amount", "1000")

        fake_secret = "test_secret_key"
        sign_string = f"{click_trans_id}{service_id}{fake_secret}{order_id}{amount}"
        sign = hashlib.md5(sign_string.encode()).hexdigest()

        # ✅ Yangi fake payment yozamiz
        Payment.objects.create(
            click_trans_id=click_trans_id,
            merchant_trans_id=order_id,
            merchant_confirm_id="FAKE_CONFIRM_ID",
            sign_string=sign,
            error=0,
            error_note="Test click success ✅"
        )

        return JsonResponse({
            "click_trans_id": click_trans_id,
            "merchant_trans_id": order_id,
            "merchant_confirm_id": "FAKE_CONFIRM_ID",
            "sign_string": sign,
            "error": 0,
            "error_note": "Test click success ✅"
        })

    return JsonResponse({"error": -1, "error_note": "Invalid method"}, status=405)

@csrf_exempt
def fake_payme(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            method = body.get("method")

            if method == "CheckPerformTransaction":
                return JsonResponse({"result": {"allow": True}})

            elif method == "CreateTransaction":
                click_trans_id = body.get("click_trans_id", "PM123")
                merchant_trans_id = body.get("merchant_trans_id", "ORDER_PM")
                merchant_confirm_id = "PM_CONFIRM_1"
                sign_string = "fake_sign_pm"
                error = 0
                error_note = "CreateTransaction success 🚀"

                Payment.objects.create(
                    click_trans_id=click_trans_id,
                    merchant_trans_id=merchant_trans_id,
                    merchant_confirm_id=merchant_confirm_id,
                    sign_string=sign_string,
                    error=error,
                    error_note=error_note
                )

                return JsonResponse({
                    "result": {
                        "transaction": "FAKE_TXN",
                        "state": 1,
                        "create_time": 123456
                    }
                })

            elif method == "PerformTransaction":
                return JsonResponse({"result": {"state": 2}})

            return JsonResponse({"error": {"message": "Unknown method"}}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": {"message": "Invalid JSON"}}, status=400)

    return JsonResponse({"error": {"message": "Invalid method"}}, status=405)
