from django.conf import settings

def user_info(request):
    return {
        'logged_in_user': request.user
    }