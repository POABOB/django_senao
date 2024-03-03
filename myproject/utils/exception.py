# Custom Error Handler
from rest_framework.views import exception_handler, Response
from rest_framework import status

def custom_exception_handler(exc, context):
    # 使用 exception_handler 來處理預設的異常處理，並進行加工
    response = exception_handler(exc, context)
    
    if response is None:
        return Response({
            'error': 'Internal Server Error:{exc}'.format(exc=exc)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR, exception=True)
    else:
        msg = exc.args

        if len(exc.args) == 1:
            msg = exc.args[0]
            if isinstance(msg, float):
                return Response({
                    'error': "Too Many Requests.",
                }, status=response.status_code, exception=True)

        if "non_field_errors" in msg:
            msg = msg["non_field_errors"][0]

        return Response({
            'error': msg,
        }, status=response.status_code, exception=True)