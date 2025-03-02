#!/usr/bin/env python
import datetime
import json
import logging
import os
import sys
import traceback
from functools import wraps

# Add the bots/src directory to the Python path
sys.path.append("/app/bots/src")


# Configure logging
class JsonFormatter(logging.Formatter):
    """Format logs as JSON for better parsing and analysis."""

    def format(self, record):
        """Format the log record as a JSON string."""
        log_data = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add exception info if available
        if record.exc_info:
            log_data["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": traceback.format_exception(*record.exc_info),
            }

        # Add extra fields if available
        if hasattr(record, "data"):
            log_data["data"] = record.data

        return json.dumps(log_data)


# Set up loggers
def setup_auth_audit_logger():
    """Set up a logger for authentication audit events."""
    logger = logging.getLogger("auth_audit")
    logger.setLevel(logging.INFO)

    # File handler for audit logs
    file_handler = logging.FileHandler("/app/logs/auth_audit.log")
    file_handler.setFormatter(JsonFormatter())

    # Console handler for debugging
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Authentication event types
AUTH_EVENTS = {
    "LOGIN_SUCCESS": "User successfully logged in",
    "LOGIN_FAILURE": "User login failed",
    "LOGOUT": "User logged out",
    "PASSWORD_CHANGE": "User changed password",
    "ACCOUNT_LOCKED": "Account locked due to too many failed attempts",
    "ACCESS_DENIED": "Access denied to protected resource",
    "CSRF_FAILURE": "CSRF token validation failed",
    "SESSION_EXPIRED": "User session expired",
}


# Audit logging function
def log_auth_event(logger, event_type, user=None, extra_data=None):
    """Log an authentication event with relevant details."""
    if event_type not in AUTH_EVENTS:
        raise ValueError(f"Unknown event type: {event_type}")

    # Prepare log data
    data = {
        "event_type": event_type,
        "event_description": AUTH_EVENTS[event_type],
        "timestamp": datetime.datetime.utcnow().isoformat(),
    }

    # Add user information if available
    if user:
        if user.is_authenticated:
            data["user"] = {
                "id": user.id,
                "username": user.username,
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,
            }
        else:
            data["user"] = "anonymous"

    # Add extra data if available
    if extra_data:
        data["details"] = extra_data

    # Create a log record with the data
    logger_extra = {"data": data}
    logger.info(f"AUTH EVENT: {event_type}", extra=logger_extra)

    return data


# Django signal handlers
def setup_auth_signals():
    """Set up Django signal handlers for authentication events."""
    # Only run this if Django is available
    try:
        from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
        from django.dispatch import receiver

        logger = setup_auth_audit_logger()

        @receiver(user_logged_in)
        def log_user_login(sender, request, user, **kwargs):
            """Log successful login."""
            log_auth_event(
                logger,
                "LOGIN_SUCCESS",
                user,
                {
                    "ip_address": get_client_ip(request),
                    "user_agent": request.META.get("HTTP_USER_AGENT", ""),
                    "session_key": request.session.session_key,
                },
            )

        @receiver(user_logged_out)
        def log_user_logout(sender, request, user, **kwargs):
            """Log logout."""
            log_auth_event(
                logger,
                "LOGOUT",
                user,
                {
                    "ip_address": get_client_ip(request),
                    "user_agent": request.META.get("HTTP_USER_AGENT", ""),
                },
            )

        @receiver(user_login_failed)
        def log_user_login_failed(sender, credentials, request, **kwargs):
            """Log failed login."""
            log_auth_event(
                logger,
                "LOGIN_FAILURE",
                None,
                {
                    "username": credentials.get("username", ""),
                    "ip_address": get_client_ip(request),
                    "user_agent": request.META.get("HTTP_USER_AGENT", ""),
                },
            )

        print("Authentication signal handlers registered")
        return True

    except ImportError:
        print("Django auth signals not available")
        return False


# Utility functions
def get_client_ip(request):
    """Get client IP address from request."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


# Decorator for audit logging
def audit_auth_action(event_type):
    """Decorator to audit authentication-related actions."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = setup_auth_audit_logger()

            # Try to find request and user objects
            request = None
            user = None

            # Look for request in args or kwargs
            for arg in args:
                if hasattr(arg, "META") and hasattr(arg, "session"):
                    request = arg
                    break

            if not request and "request" in kwargs:
                request = kwargs["request"]

            # Get user from request or kwargs
            if request and hasattr(request, "user"):
                user = request.user
            elif "user" in kwargs:
                user = kwargs["user"]

            # Extra data for logging
            extra_data = {
                "function": func.__name__,
                "args": str(args),
                "kwargs": str(kwargs),
            }

            if request:
                extra_data.update(
                    {
                        "ip_address": get_client_ip(request),
                        "user_agent": request.META.get("HTTP_USER_AGENT", ""),
                    }
                )

            # Log before executing function
            log_auth_event(logger, event_type, user, extra_data)

            try:
                # Call the original function
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                # Log exception
                logger.exception(f"Exception in {func.__name__}: {str(e)}")
                raise

        return wrapper

    return decorator


# Initialize if run directly
if __name__ == "__main__":
    logger = setup_auth_audit_logger()
    logger.info("Authentication audit logger initialized")

    # Try to set up Django signal handlers
    setup_auth_signals()
