# Authentication Testing and Auditing

This module provides a comprehensive testing and auditing system for the authentication functionality in the Bots application.

## Features

### 1. Authentication Test Suite

Located at `bots/tests/test_auth.py`, this test suite includes:

- Tests for login/logout functionality
- Session persistence verification
- Authentication redirect validation
- Access control tests
- CSRF protection tests

### 2. Authentication Audit Logging

Located at `bots/utils/auth_audit_logger.py`, this system:

- Logs all authentication events (logins, logouts, failures)
- Provides detailed session information
- Tracks user actions with IP addresses and user agents
- Formats logs as JSON for easy analysis
- Integrates with Django signals

### 3. Authentication Monitoring Middleware

Located at `bots/middleware/auth_monitoring.py`, this middleware:

- Detects suspicious authentication requests
- Logs slow authentication operations
- Tracks authentication failures
- Captures exceptions in authentication flows

## Running Tests

To run the authentication tests:

```bash
cd /app/bots/src
python -m django test bots.tests.test_auth
```

## Viewing Audit Logs

Authentication audit logs are stored in `/app/logs/auth_audit.log` in JSON format.

## Best Practices

1. **Regular Testing**: Run the authentication test suite before deploying changes
2. **Audit Log Review**: Regularly review audit logs for security issues
3. **Security Monitoring**: Set up alerts for suspicious authentication patterns
4. **Compliance**: Ensure audit logs meet regulatory requirements

## Extending the System

### Adding New Tests

To add new authentication tests, extend the `AuthenticationTestCase` class in `bots/tests/test_auth.py`.

### Adding New Audit Events

To track new types of events, add them to the `AUTH_EVENTS` dictionary in `bots/utils/auth_audit_logger.py`.

### Custom Middleware Checks

To add new security checks, modify the `AuthMonitoringMiddleware` class in `bots/middleware/auth_monitoring.py`.
