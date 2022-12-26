from django.utils.deprecation import MiddlewareMixin

class XFrameOptionsMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response['x-frame-options'] = 'sameorigin'
        return response
