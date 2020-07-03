from django.utils.deprecation import MiddlewareMixin


class SessionLogoutMiddleware(MiddlewareMixin):

    @staticmethod
    def process_request(request):
        if request.user.is_superuser:
            request.session.set_expiry(None)
        else:
            request.session.set_expiry(5 * 60)
