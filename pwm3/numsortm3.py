import concurrent.futures
import time
import multiprocessing


def factorize(num):
    factors = [1]
    step = 2 if num % 2 == 1 else 1
    for i in range(2, (num // 2) + 1, step):
        if num % i == 0:
            factors.extend([i, num // i])
    factors.append(num)
    return factors


def factorize_parallel(num):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(factorize, num)
    return results


def measure_time_parallel(numbers):
    start_time = time.time()
    result = factorize_parallel(numbers)
    end_time = time.time()
    elapsed_time = end_time - start_time
    return result, elapsed_time


def measure_time(numbers):
    start_time = time.time()
    result = [factorize(num) for num in numbers]
    end_time = time.time()
    elapsed_time = end_time - start_time
    return result, elapsed_time


if __name__ == "__main__":
    numbers_to_factorize = [128, 255, 99999, 10651060]

    num_cores = multiprocessing.cpu_count() * 2 + 1
    print(f"Number of CPU cores: {num_cores}")

    result, time_serial = measure_time(numbers_to_factorize)
    result_parallel, time_parallel = measure_time_parallel(numbers_to_factorize)

    print("Serial Results:", result)
    print(f"Serial Time: {time_serial} seconds")

    print("Parallel Results:", list(result_parallel))
    print(f"Parallel Time: {time_parallel} seconds")
