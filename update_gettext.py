import os

def update_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    content = content.replace('from django.utils.translation import ugettext as _', 
                              'from django.utils.translation import gettext as _')
    content = content.replace('from django.utils.translation import ugettext_lazy as _', 
                              'from django.utils.translation import gettext_lazy as _')
    
    with open(file_path, 'w') as file:
        file.write(content)

def traverse_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                update_file(file_path)

traverse_directory('bots')
print("All .py files in the 'bots' directory have been updated.")