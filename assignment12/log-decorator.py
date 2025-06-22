# log-decorator.py

import logging

# One-time setup for logger
logger = logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("./decorator.log", "a"))

# Decorator definition
def logger_decorator(func):
    def wrapper(*args, **kwargs):
        # Prepare the log components
        func_name = func.__name__
        pos_params = args if args else "none"
        kw_params = kwargs if kwargs else "none"

        # Execute the function and capture return value
        result = func(*args, **kwargs)

        # Write log entry
        logger.info(f"\nfunction: {func_name}\n"
                    f"positional parameters: {pos_params}\n"
                    f"keyword parameters: {kw_params}\n"
                    f"return: {result}")

        return result
    return wrapper

# Function 1: No parameters, no return
@logger_decorator
def say_hello():
    print("Hello, World!")

# Function 2: Variable number of positional arguments
@logger_decorator
def accept_args(*args):
    return True

# Function 3: Variable number of keyword arguments, returns the decorator function
@logger_decorator
def keyword_args_only(**kwargs):
    return logger_decorator

# Main execution
if __name__ == "__main__":
    say_hello()
    accept_args(1, 2, 3, 4)
    keyword_args_only(name="Renato", age=38, country="USA")
