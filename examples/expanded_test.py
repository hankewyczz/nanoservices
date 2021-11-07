import time
import random


# Generates a random list of length SIZE, such that each element is
# 	between 1 and 5,000,000
def generate_list(size):
    return random.sample(range(1, 5_000_000), size)


#############
## Sorting algorithms
#################


def bubble_sort(A):
    end = len(A) - 1
    swapped = True
    i = end
    while swapped:
        i -= 1
        if i % 1_000 == 0:
            print(i)
        swapped = False
        for i in range(0, end):
            if A[i] > A[i + 1]:
                A[i], A[i + 1] = A[i + 1], A[i]


def selection_sort(A):
    for i in range(len(A)):

        min_idx = i
        for j in range(i + 1, len(A)):
            if A[min_idx] > A[j]:
                min_idx = j
        A[i], A[min_idx] = A[min_idx], A[i]


def insertion_sort(arr):
    for i in range(1, len(arr)):

        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

        arr = [12, 11, 13, 5, 6]
        insertion_sort(arr)


def merge(arr, l, m, r):
    n1 = m - l + 1
    n2 = r - m

    # create temp arrays
    L = [0] * (n1)
    R = [0] * (n2)

    # Copy data to temp arrays L[] and R[]
    for i in range(0, n1):
        L[i] = arr[l + i]

    for j in range(0, n2):
        R[j] = arr[m + 1 + j]

    # Merge the temp arrays back into arr[l..r]
    i = 0  # Initial index of first subarray
    j = 0  # Initial index of second subarray
    k = l  # Initial index of merged subarray

    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    # Copy the remaining elements of L[], if there
    # are any
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1

    # Copy the remaining elements of R[], if there
    # are any
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1


def merge_sort_helper(arr, l, r):
    if l < r:
        m = l + (r - l) // 2

        # Sort first and second halves
        merge_sort_helper(arr, l, m)
        merge_sort_helper(arr, m + 1, r)
        merge(arr, l, m, r)

    n = len(arr)
    merge_sort_helper(arr, 0, n - 1)


def merge_sort(A):
    return merge_sort_helper(A, 0, len(A) - 1)


def shell_sort(A):
    n = len(A)
    gap = n // 2

    while gap > 0:
        for i in range(gap, n):
            temp = A[i]

            j = i
            while j >= gap and A[j - gap] > temp:
                A[j] = A[j - gap]
                j -= gap

            A[j] = temp
        gap = gap // 2


# def partition(arr, low, high):
#     i = low - 1
#     pivot = arr[high]
#     for j in range(low, high):
#         if arr[j] <= pivot:
#             i = i + 1
#             arr[i], arr[j] = arr[j], arr[i]
#     arr[i + 1], arr[high] = arr[high], arr[i + 1]
#     return i + 1
#
#
# def quicksort_helper(arr, low, high):
#     if low < high:
#         partition_index = partition(arr, low, high)
#         quicksort_helper(arr, low, partition_index - 1)
#         quicksort_helper(arr, partition_index + 1, high)
#
#
# def quicksort(A):
#     return quicksort_helper(A, 0, len(A) - 1)


sorting_algos = {
    "quicksort": quicksort,
    "shellsort": shell_sort,
    "mergesort": merge_sort,
    "insertionsort": insertion_sort,
    "selectionsort": selection_sort,
    "bubblesort": bubble_sort
}

algo_name = ""
while algo_name not in sorting_algos:
    print(f"Pick a sorting algorithm: {', '.join(sorting_algos.keys())}")
    algo_name = input().strip()

print("Enter a set size: ")
size = int(input().strip())

start = time.time()
print(f"Running {algo_name} on set of size {size}")
sorting_algos[algo_name](generate_list(size))

end = time.time()
print(f"Took {end - start} seconds")