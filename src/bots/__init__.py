# -*- coding: utf-8 -*-

__version__ = '3.3.1.dev0'  # Update this version number as needed

# Don't import modules at the package level that have Django dependencies
# This allows the package to be imported even if Django is not yet configured
# Only expose the version and let users import specific modules as needed

# The import statement below caused circular imports, so it's better to avoid them
# try:
#     from . import botslib
#     from . import botsglobal
#     from . import router
# except ImportError as e:
#     print(f"Error importing bots modules: {e}")

# # Expose commonly used functions and classes
# try:
#     from .botslib import join, strftime
#     # Remove or comment out the countchildrenrecursive import if it's not defined
#     # from .botslib import countchildrenrecursive
#     from .botsglobal import ini, logger
#     from .router import rundispatcher
#     # Comment out or remove the 'routes' import if it's not defined in router.py
#     # from .router import routes
#     from .router import cleanup
# except ImportError as e:
#     print(f"Error importing specific functions: {e}")

# Add any other necessary imports or initializations here
