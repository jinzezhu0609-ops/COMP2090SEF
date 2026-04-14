def heapify(arr, n, i):
    """Sift Down: Move element down to maintain max-heap property"""
    largest = i        # Suppose i is the largest 
    l = 2 * i + 1       # Left subset
    r = 2 * i + 2     # Right subset
    
    # Check if children are larger than current node
    if l < n and arr[largest] < arr[l]:   
        largest = l 
    if r < n and arr[largest] < arr[r]:  
        largest = r
        
    if largest != i:   # Swap and continue heapifying if parent is not the largest
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heap_sort(arr):
    """Heap Sort: Returns the array sorted in ascending order"""
    n = len(arr)  
    # Build a maxheap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    
    # Swap max element to the end and reduce heap size
    for i in range(n - 1, 0, -1):  
        arr[i], arr[0] = arr[0], arr[i] # Move the max-heap to the end.
        heapify(arr, i, 0) 
    return arr


arr = [3, 9, 2, 1, 4, 5]
print("Original array:", arr)
sorted_arr = heap_sort(arr)
print("Sorted array:", sorted_arr)