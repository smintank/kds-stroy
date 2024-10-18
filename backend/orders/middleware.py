class OrderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        order_id = request.session.get("order_id")
        order_created = 1 if request.session.get("order_created") else 0

        if request.COOKIES.get('order_id') != str(order_id) or request.COOKIES.get('order_created') != str(order_created):
            response.set_cookie('order_id', order_id, max_age=360000)
            response.set_cookie('order_created', order_created, max_age=360000)

        return response
