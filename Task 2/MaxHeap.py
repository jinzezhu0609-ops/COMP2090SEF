class MaxHeap:
    def __init__(self, arr = None):  
        ''' Initialize the array and use a None as a placeholder at the 0th position, 
        and the data will start from index 1'''
        if arr is None:
            self.arr = [None]
        else:
            self.arr = [None] + arr  
            
        if len(self.arr) > 1:    # Start building the heap
            n = len(self.arr) - 1    # The true total number of elements
            for i in range(n // 2, 0, -1):  # Starting from the last element with a child, proceed in reverse order and make adjustments one by one
                self.heapify(self.arr, n, i)

    def heapify(self, arr, n, i):
        largest = i        # Suppose i is the largest 
        l = 2 * i          # Left subset
        r = 2 * i + 1      # Right subset
        
        # If the left child node exists and is large than the parent node, update the index
        if l <= n and arr[i] < arr[l]:   
            largest = l 
        # If the right child exists and is large than the maximum value just now, update the index again
        if r <= n and arr[largest] < arr[r]:  
            largest = r
            
        if largest != i:   # If after a round of comparison, it is that the largest one is not the parent node
            arr[i], arr[largest] = arr[largest], arr[i]
            self.heapify(arr, n, largest)

    def heapSort(self):
        temp_arr = self.arr.copy()
        n = len(temp_arr) - 1  
        # In each iteration, swap the top of the heap (the overall maximum) with the last element in the current range
        for i in range(n, 1, -1):  
        # After swapping, the element from the end is now at the top. We need to sift it down within the remaining unsorted range (i - 1).
            temp_arr[i], temp_arr[1] = temp_arr[1], temp_arr[i] 
            self.heapify(temp_arr, i - 1, 1) 
        return temp_arr[1:]

    def get_max(self):         # Changed from get_min to get_max
        if len(self.arr) <= 1:  
            return None
        return self.arr[1]      
    
    def insert(self, val):
        self.arr.append(val)  # append the new element to the very end of the array
        curr = len(self.arr) - 1  
        # Start upward adjustment (Sift Up): As long as it hasn't reached the top of the heap (index 1)
        while curr > 1:
            parent = curr // 2    
            # If the new element is large than its parent, swap them
            if self.arr[curr] > self.arr[parent]:
                self.arr[curr], self.arr[parent] = self.arr[parent], self.arr[curr]
                curr = parent
            else:
                break

    def remove_max(self):    
        if len(self.arr) <= 1:  # Cannot delete when the heap is empty
            print("The heap is empty and deletion failed")
            return None
            
        if len(self.arr) == 2:    
            return self.arr.pop()

        max_val = self.arr[1]      # Save the maximum value at the top of the heap to return 
        self.arr[1] = self.arr.pop()
        self.heapify(self.arr, len(self.arr) - 1, 1)
        
        return max_val


if __name__ == "__main__":
    arr = [4, 10, 3, 5, 1, 2]
    my_heap = MaxHeap(arr)
    print(f"Output the initialized object {my_heap.arr}")      # Output the initialized object [None, 1, 4, 2, 5, 10, 3]
    my_heap.heapSort()
    print(f"Sorted output: {my_heap.heapSort()}")              # Sorted output [10, 5, 4, 3, 2, 1]
    my_heap.get_max()
    print(f"The minimum value: {my_heap.get_max()}")           # The minimum value: 1
    my_heap.insert(15)
    print(f"Output the object: {my_heap.arr}")                 # [None, 1, 4, 2, 5, 10, 3, 15]
    print(f"The object after deleting the minimum value: {my_heap.remove_max()}")       # 15
