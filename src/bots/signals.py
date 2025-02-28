# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.core.signals import request_finished
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver

# Import the auth audit logger
from bots.utils.auth_audit_logger import log_auth_event, setup_auth_audit_logger, get_client_ip

# Set up the auth audit logger
logger = setup_auth_audit_logger()

@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    '''
    Log user login.
    '''
    log_auth_event(
        logger,
        'LOGIN_SUCCESS',
        user,
        {
            'ip_address': get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'session_key': request.session.session_key,
        }
    )

@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    '''
    Log user logout.
    '''
    log_auth_event(
        logger,
        'LOGOUT',
        user,
        {
            'ip_address': get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
        }
    )

@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, request, **kwargs):
    '''
    Log failed login attempt.
    '''
    log_auth_event(
        logger,
        'LOGIN_FAILURE',
        None,
        {
            'username': credentials.get('username', ''),
            'ip_address': get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
        }
    )
