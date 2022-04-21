import os


def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

def dinput(message, default_value=None):
    if default_value is not None:
        _x = input(f"{message} (default={default_value}): ")
        if _x is None: return default_value 
        else: return _x 
    else:
        return input(message)