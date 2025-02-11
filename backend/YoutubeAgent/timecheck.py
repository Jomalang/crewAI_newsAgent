import time

def time_check(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        execution_time = end_time - start_time
        execution_time = round(execution_time, 2)
        print(f"💡실행 시간: {execution_time} 초")
        return result
    return wrapper





