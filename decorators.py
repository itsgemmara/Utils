import time


def run_time(function):

    def wrapper(*args, **kwargs):
        start = time.time()
        returned_value = function(*args, **kwargs)
        f_name = function.__name__
        end = time.time()
        print(f"{f_name} took {end-start} to execute!")
        return returned_value
    
    return wrapper

