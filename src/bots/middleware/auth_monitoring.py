# -*- coding: utf-8 -*-
import logging
import time
import traceback
from django.utils.deprecation import MiddlewareMixin
from bots.utils.auth_audit_logger import get_client_ip

# Set up logger
logger = logging.getLogger('auth_audit')

class AuthMonitoringMiddleware(MiddlewareMixin):
    '''
    Middleware to monitor and log authentication-related activities.
    '''
    
    def process_request(self, request):
        '''
        Process the request.
        '''
        # Add request start time for performance monitoring
        request.start_time = time.time()
        
        # Log suspicious requests that might indicate security issues
        if self._is_suspicious_request(request):
            self._log_suspicious_request(request)
        
        return None
    
    def process_response(self, request, response):
        '''
        Process the response.
        '''
        # Calculate request processing time
        if hasattr(request, 'start_time'):
            processing_time = time.time() - request.start_time
            
            # Log slow authentication requests (more than 1 second)
            if processing_time > 1.0 and self._is_auth_url(request.path):
                self._log_slow_auth_request(request, response, processing_time)
        
        # Log authentication failures (401, 403)
        if response.status_code in (401, 403) and hasattr(request, 'user'):
            self._log_auth_failure_response(request, response)
        
        return response
    
    def process_exception(self, request, exception):
        '''
        Process any exception that occurs during request handling.
        '''
        # Log exceptions in authentication views
        if self._is_auth_url(request.path):
            self._log_auth_exception(request, exception)
        
        return None
    
    def _is_auth_url(self, path):
        '''
        Check if the URL is authentication-related.
        '''
        auth_paths = ('/login/', '/logout/', '/admin/login/', '/password_change/')
        return any(path.startswith(p) for p in auth_paths)
    
    def _is_suspicious_request(self, request):
        '''
        Check if the request looks suspicious.
        '''
        # Examples of suspicious patterns:
        # - SQL injection attempts
        # - Path traversal attacks
        # - Known malicious user agents
        
        path = request.path.lower()
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        
        suspicious_patterns = [
            'union select',
            '../',
            'exec(',
            'eval(',
            '<script',
            'sqlmap',
            'nikto',
            'dirbuster'
        ]
        
        return any(pattern in path or pattern in user_agent for pattern in suspicious_patterns)
    
    def _log_suspicious_request(self, request):
        '''
        Log a suspicious request.
        '''
        logger.warning(
            f"Suspicious request detected",
            extra={
                'data': {
                    'path': request.path,
                    'method': request.method,
                    'ip_address': get_client_ip(request),
                    'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                    'user': request.user.username if request.user.is_authenticated else 'anonymous',
                }
            }
        )
    
    def _log_slow_auth_request(self, request, response, processing_time):
        '''
        Log a slow authentication request.
        '''
        logger.warning(
            f"Slow authentication request: {processing_time:.2f}s",
            extra={
                'data': {
                    'path': request.path,
                    'method': request.method,
                    'status_code': response.status_code,
                    'processing_time': f"{processing_time:.2f}s",
                    'ip_address': get_client_ip(request),
                    'user': request.user.username if request.user.is_authenticated else 'anonymous',
                }
            }
        )
    
    def _log_auth_failure_response(self, request, response):
        '''
        Log authentication failure response.
        '''
        logger.warning(
            f"Authentication failure: {response.status_code}",
            extra={
                'data': {
                    'path': request.path,
                    'method': request.method,
                    'status_code': response.status_code,
                    'ip_address': get_client_ip(request),
                    'user': request.user.username if request.user.is_authenticated else 'anonymous',
                }
            }
        )
    
    def _log_auth_exception(self, request, exception):
        '''
        Log exception in authentication view.
        '''
        logger.error(
            f"Exception in authentication view: {str(exception)}",
            extra={
                'data': {
                    'path': request.path,
                    'method': request.method,
                    'exception': str(exception),
                    'traceback': traceback.format_exc(),
                    'ip_address': get_client_ip(request),
                    'user': request.user.username if request.user.is_authenticated else 'anonymous',
                }
            }
        )
