# Custom Error Handler
from rest_framework.views import exception_handler, Response
from rest_framework import status

def custom_exception_handler(exc, context):
    # 使用 exception_handler 來處理預設的異常處理，並進行加工
    response = exception_handler(exc, context)
    print(type(exc))
    if response is None:
        return Response({
            'error': 'Internal Server Error:{exc}'.format(exc=exc)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR, exception=True)
    else:
        return Response({
            'error':'{exc}'.format(exc=exc),
        }, status=response.status_code, exception=True)