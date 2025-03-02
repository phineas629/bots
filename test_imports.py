#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# Try to import bots
print("Attempting to import bots...")
try:
    import bots

    print("Successfully imported bots")
    print(("Bots package location:", bots.__file__))
    print(("Bots package attributes:", dir(bots)))

    # Try to import specific modules
    try:
        from bots import botslib

        print("Successfully imported botslib")
        print(("botslib location:", botslib.__file__))
    except ImportError as e:
        print(f"Failed to import botslib: {e}")

    try:
        from bots import botsglobal

        print("Successfully imported botsglobal")
        print(("botsglobal location:", botsglobal.__file__))
    except ImportError as e:
        print(f"Failed to import botsglobal: {e}")

except ImportError as e:
    print(f"Failed to import bots: {e}")
