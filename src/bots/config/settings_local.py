import os

# Debug settings
DEBUG = True
TEMPLATE_DEBUG = True

# Template directories will be appended to TEMPLATES if it exists
def setup_templates():
    global TEMPLATES
    if 'TEMPLATES' in globals():
        TEMPLATES[0]['DIRS'] = [
            '/app/bots/src/bots/templates',
            # Keep the original directory as fallback
            '/usr/local/lib/python3.9/site-packages/bots-3.3.1.dev0-py3.9.egg/bots/templates'
        ]

# Call setup_templates after it's imported
setup_templates()