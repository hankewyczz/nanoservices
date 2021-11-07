import time
import random
from statistics import mean


# Generates a random list of length SIZE
def generate_list(size):
    return random.sample(range(1, size * 2), size)


def partition(arr, low, high):
    i = low - 1
    pivot = arr[high]
    for j in range(low, high):
        if arr[j] <= pivot:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return [arr, i + 1]


def quicksort(arr, low, high):
    if low < high:
        arr, partition_index = partition(arr, low, high)
        arr = quicksort(arr, low, partition_index - 1)
        arr = quicksort(arr, partition_index + 1, high)
    return arr


def main(list_size):
    A = generate_list(list_size)
    start = time.time()

    A = quicksort(A, 0, len(A) - 1)
    duration = time.time() - start

    return {'result': A, 'runtime': duration}



runs = (main(500) for _ in range(100))
runtimes = (result["runtime"] for result in runs)

print(f"Mean runtime: {round(mean(runtimes), 4)}")