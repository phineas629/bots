# Authentication Auditing System for Bots

This document provides an overview of the authentication auditing system that has been installed in the Bots application.

## Overview

The authentication auditing system logs all authentication-related events (login success, login failure, logout) to a dedicated log file. This helps with security monitoring and compliance requirements.

## Components

The system consists of the following components:

1. **Auth Audit Logger** (`auth_audit_logger.py`): A dedicated logger for authentication events.
2. **Auth Monitoring Middleware** (`middleware/auth_monitoring.py`): Middleware that intercepts authentication requests and logs relevant events.
3. **Test Suite** (`tests/test_auth.py`): A comprehensive test suite that verifies the functionality of the authentication system.

## Log File

Authentication events are logged to `/app/logs/auth_audit.log`. Each log entry includes:

- Timestamp
- Event type (LOGIN_SUCCESS, LOGIN_FAILURE, LOGOUT)
- Username (if available)
- IP address (if available)
- User agent (if available)

## Running the Tests

To run the authentication tests, use the provided test runner:

```bash
cd /app/bots/src
python /tmp/run_auth_tests.py
```

The test runner handles the necessary environment setup and mocks the `botsglobal.ini` object to avoid initialization errors.

## Test Coverage

The test suite covers the following scenarios:

1. Login URL accessibility
2. CSRF token presence in login form
3. Successful login
4. Failed login with invalid credentials
5. Logout functionality
6. Login-required views protection
7. Admin interface access control
8. Session persistence
9. Authenticated user redirection

## Troubleshooting

If you encounter issues with the tests, check the following:

1. Make sure the `botsglobal.ini` object is properly mocked in the test runner.
2. Verify that the authentication middleware is correctly installed in the Django settings.
3. Check that the log directory (`/app/logs`) exists and is writable.

## Security Considerations

The authentication auditing system enhances security by:

1. Logging all authentication attempts, successful or not.
2. Providing an audit trail for security investigations.
3. Helping to detect potential brute force attacks.

## Maintenance

Regularly review the authentication logs for suspicious activity. Consider implementing log rotation to manage the size of the log file over time.
