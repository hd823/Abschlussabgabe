def bubble_sort(arr):
    """
    Bubble Sort Algorithm
    Algorithm sorts an array in ascending order using the bubble sort method. Function needs one given array as input and returns the sorted array.
    Time Complexity: O(n^2)
    Space Complexity: O(1)
    """
    n = len(arr)

    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr

def invert_array(arr):
    """
    Function inverts the given array. It needs one given array as input and returns the inverted array.
    """
    arr = arr[::-1]
    return arr

def sort_and_invert(arr):
    """
    Function sorts the given array in ascending order and then inverts it. It needs one given array as input and returns the inverted sorted array.
    """
    arr = bubble_sort(arr)
    arr = invert_array(arr)
    return arr


if __name__ == "__main__":
    # Example usage
    arr = [64, 34, 25, 12, 22, 11, 90]
    print("sorted array is:", bubble_sort(arr))