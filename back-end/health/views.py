from django.http import JsonResponse
from django.db import connection

'''
    Health Check View
    -----------------
    Purpose is to use this route before main request to ensure API and database are awake
'''
def health_check(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
        return JsonResponse({'status': 'ready'})
    except Exception as error:
        return JsonResponse({'status': 'error', 'messsage': str(error)}, status=500)
