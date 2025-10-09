from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    """
    Custom exception handler for consistent error responses.
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    # Now add the custom format
    if response is not None:
        custom_response_data = {
            'success': False,
            'message': str(response.data.get('detail', 'An error occurred.'))
        }
        
        # If there are field errors, include them
        if isinstance(response.data, dict) and 'detail' not in response.data:
            errors = []
            for field, messages in response.data.items():
                if isinstance(messages, list):
                    errors.append(f"{field}: {', '.join(messages)}")
                else:
                    errors.append(f"{field}: {messages}")
            custom_response_data['message'] = '; '.join(errors)
        
        response.data = custom_response_data

    return response

