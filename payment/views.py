from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .models import Payment
import hashlib

class FakeClickAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        click_trans_id = data.get("click_trans_id", "123456")
        service_id = data.get("service_id", "1")
        order_id = data.get("merchant_trans_id", "ORDER123")
        amount = data.get("amount", "1000")

        fake_secret = "test_secret_key"
        sign_string = f"{click_trans_id}{service_id}{fake_secret}{order_id}{amount}"
        sign = hashlib.md5(sign_string.encode()).hexdigest()

        Payment.objects.create(
            click_trans_id=click_trans_id,
            merchant_trans_id=order_id,
            merchant_confirm_id="FAKE_CONFIRM_ID",
            sign_string=sign,
            error=0,
            error_note="Test click success ✅"
        )

        return Response({
            "click_trans_id": click_trans_id,
            "merchant_trans_id": order_id,
            "merchant_confirm_id": "FAKE_CONFIRM_ID",
            "sign_string": sign,
            "error": 0,
            "error_note": "Test click success ✅"
        }, status=status.HTTP_201_CREATED)

class FakePaymeAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            method = request.data.get("method")

            if method == "CheckPerformTransaction":
                return Response({"result": {"allow": True}})

            elif method == "CreateTransaction":
                click_trans_id = request.data.get("click_trans_id", "PM123")
                merchant_trans_id = request.data.get("merchant_trans_id", "ORDER_PM")
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

                return Response({
                    "result": {
                        "transaction": "FAKE_TXN",
                        "state": 1,
                        "create_time": 123456
                    }
                })

            elif method == "PerformTransaction":
                return Response({"result": {"state": 2}})

            return Response({"error": {"message": "Unknown method"}}, status=400)

        except Exception:
            return Response({"error": {"message": "Invalid JSON"}}, status=400)
