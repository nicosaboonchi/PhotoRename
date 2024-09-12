import time

def timer(function):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        function(*args, **kwargs)
        end_time = time.time()
        print(f"Took {end_time - start_time} seconds")

    return wrapper