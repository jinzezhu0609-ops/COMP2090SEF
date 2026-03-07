def heapify(arr, n, i):
    largest = i       # Initialize largest as root
    l = 2 * i + 1     # Left child index
    r = 2 * i + 2     # Right child index
    if l < n and arr[i] < arr[l]:   # If left child exists and is larger than root
        largest = l 
    if r < n and arr[largest] < arr[r]:  # If right child exists and is larger than current largest
        largest = r
    if largest != i:   # If largest is not root, swap and continue heapifying
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heapSort(arr):  # Perform heap sort
    n = len(arr)
    for i in range(n, -1, -1):  # Build a max-heap from the array
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):  # Extract elements from the heap
        arr[i], arr[0] = arr[0], arr[i] # Swap
        heapify(arr, i, 0)


arr = [12, 14, 13, 11, 10, 8, 4, 2, 5, 1]
li = []
print(arr)
heapSort(arr)
n = len(arr)
for i in range(n):
    li.append(arr[i])
print(li)