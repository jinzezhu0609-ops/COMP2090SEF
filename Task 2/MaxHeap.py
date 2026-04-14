class MaxHeap:
    def __init__(self, arr = None):  
        ''' Initialize with None at index 0 so data starts at index 1'''
        if arr is None:
            self.arr = [None]
        else:
            self.arr = [None] + arr  
            
        if len(self.arr) > 1:    # Start building the heap
            n = len(self.arr) - 1    # The true total number of elements
            for i in range(n // 2, 0, -1):  
                self.heapify(self.arr, n, i)

    def heapify(self, arr, n, i):
        """Sift Down: Move element down to maintain max-heap property"""
        largest = i        # Suppose i is the largest 
        l = 2 * i          # Left subset
        r = 2 * i + 1      # Right subset
        
       # Check if children are larger than current node
        if l <= n and arr[i] < arr[l]:   
            largest = l 
        if r <= n and arr[largest] < arr[r]:  
            largest = r
            
        if largest != i:   # Swap and continue heapifying if parent is not the largest
            arr[i], arr[largest] = arr[largest], arr[i]
            self.heapify(arr, n, largest)

    def heapSort(self):
        """Heap Sort: Returns the array sorted in ascending order"""
        temp_arr = self.arr.copy()
        n = len(temp_arr) - 1  
        # Swap max element to the end and reduce heap size
        for i in range(n, 1, -1):  
            temp_arr[i], temp_arr[1] = temp_arr[1], temp_arr[i] 
            self.heapify(temp_arr, i - 1, 1) 
        return temp_arr[1:]

    def get_max(self):
        '''Get the maximum value'''
        if len(self.arr) <= 1:  
            return None
        return self.arr[1]      
    
    def insert(self, val):
        """Insert new value and Sift Up to maintain order"""
        self.arr.append(val)  # append the new element to the very end of the array
        curr = len(self.arr) - 1  
        while curr > 1:
            parent = curr // 2    
            # If the new element is large than its parent, swap them
            if self.arr[curr] > self.arr[parent]:
                self.arr[curr], self.arr[parent] = self.arr[parent], self.arr[curr]
                curr = parent
            else:
                break

    def remove_max(self):
        """Remove and return the root (maximum) element""" 
        if len(self.arr) <= 1:  # Cannot delete when the heap is empty
            print("The heap is empty and deletion failed")
            return None
            
        if len(self.arr) == 2:    
            return self.arr.pop()

        max_val = self.arr[1]  # Save the maximum value at the top of the heap to return 
        self.arr[1] = self.arr.pop()
        self.heapify(self.arr, len(self.arr) - 1, 1)
        return max_val



if __name__ == "__main__":
    arr = [4, 10, 3, 5, 1, 2]
    my_heap = MaxHeap(arr)
    print(f"Output the initialized object: {my_heap.arr}")      # Output the initialized object: [None, 10, 5, 3, 4, 1, 2]
    my_heap.heapSort()
    print(f"Sorted output: {my_heap.heapSort()}")              # Sorted output [1, 2, 3, 4, 5, 10]
    my_heap.get_max()
    print(f"The maximum value: {my_heap.get_max()}")           # The maximum value: 10
    my_heap.insert(15)
    print(f"Output the object: {my_heap.arr}")                 # Output the object: [None, 15, 5, 10, 4, 1, 2, 3]
    print(f"Deleting the maximum value: {my_heap.remove_max()}")       # Deleting the maximum value: 15
