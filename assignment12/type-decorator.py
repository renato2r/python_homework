# type-decorator.py

# Define the decorator factory
def type_converter(type_of_output):
    def decorator(func):
        def wrapper(*args, **kwargs):
            x = func(*args, **kwargs)
            return type_of_output(x)
        return wrapper
    return decorator

# Function that returns an integer, decorated to return a string
@type_converter(str)
def return_int():
    return 5

# Function that returns a string, decorated to convert it to int
@type_converter(int)
def return_string():
    return "not a number"

# Main execution
if __name__ == "__main__":
    y = return_int()
    print(type(y).__name__)  # Should print "str"

    try:
        y = return_string()
        print("shouldn't get here!")
    except ValueError:
        print("can't convert that string to an integer!")  # This is what should happen
