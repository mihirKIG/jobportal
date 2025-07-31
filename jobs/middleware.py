import logging
import time

logger = logging.getLogger('jobs')

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log request start
        start_time = time.time()
        user = "Anonymous"
        if request.user.is_authenticated:
            user = request.user.username
        
        logger.info(f"[{request.method}] {request.path} | User: {user} | IP: {request.META.get('REMOTE_ADDR', 'Unknown')}")
        
        response = self.get_response(request)
        
        # Log request completion
        duration = time.time() - start_time
        logger.info(f"[{request.method}] {request.path} | Status: {response.status_code} | Duration: {duration:.2f}s")
        
        return response

    def process_exception(self, request, exception):
        logger.error(f"Exception in {request.path}: {str(exception)}")
        logger.exception("Full exception traceback:")
        return None
