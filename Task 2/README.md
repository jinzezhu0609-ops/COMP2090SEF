# How to Run the Program

You can easily execute the programs by directly running the `MinHeap.py` and `MaxHeap.py` files. 

> **Note:** The necessary execution code has already been written inside these programs, so they are ready to run out of the box.
--------------------------------------------------

**Take Min heap as an example** 
**First, we need to modify the VS Code Settings to make it output in the Terminal panel.**
* **Step 1:** Open settings
  * Shortcut key: `Ctrl + ,` (Windows) or `Cmd + ,` (Mac)
* **Step 2:** Enter in the search box
  * Plaintext: `code runner run in terminal`
* **Step 3:** Check the box
  * Check `Code-runner: Run in Terminal`
* **Step 4:** Then click the button
  * Click the play button and the program will automatically start in the Terminal panel
 
-------------------------------------------------

**Second, before invoking the entire program, some calling measures need to be taken.**
* We need to write it down below the entire program:
  
  ```python
     if __name__ == "__main__" :
*  (Let a piece of code only be executed when this file is directly run, and not when it is imported by another file) 

-------------------------------------------------

**Third, start creating an object**
* Step 1: Input an array at random 

  e.g. arr = [4, 10, 3, 5, 1, 2]
* Step 2: Create an object

  e.g. my_heap = MinHeap(arr)  #Initialize the defined object directly and build a heap directly to satisfy the heap properties
* Step 3: Output the initialized object

  e.g. print(f"Output the initialized object: {my_heap.arr}")  # Output the initialized object: [None, 1, 4, 2, 5, 10, 3]

-------------------------------------------------

**Fourth, perform heap sort method**
* step 1: Call the heapSort() method
 
  e.g. my_heap.heapSort()
* step 2: Output the result
 
  e.g. print(f"Sorted output: {my_heap.heapSort()}")  # Sorted output [10, 5, 4, 3, 2, 1]

------------------------------------------------

**Fifth, find the minimum value of the object list**
* step 1: Call the get_min() method
 
  e.g. my_heap.get_min()
* step 2: Output the result
 
  e.g. print(f"The minimum value: {my_heap.get_min()}")  # The minimum value: 1

------------------------------------------------

**Sixth, insert an element into the list**
* step 1: Call the insert() method
 
  e.g. my_heap.insert(15)
* step 2: Output the list of object
 
  e.g. print(f"Output the object: {my_heap.arr}")  # Output the object: [None, 1, 4, 2, 5, 10, 3, 15]

> ***Attention: Why did I sort before but insert a new element, and the resulting list is not in reverse chronological order?
>
>***Answer: Because I used a copy list in the heapSort() method, the actual list has not been changed   ( e.g. temp_arr = self.arr.copy() )
   
------------------------------------------------

**Seventh, delete the minimum value in the heap**
* step 1: Output the result
 
  e.g. print(f"The object after deleting the minimum value: {my_heap.remove_min()}")  # The object after deleting the minimum value: [None, 2, 4, 3, 5, 10, 15]

------------------------------------------------

**Last, sort out all the above operation steps**

  ```pyhton
  if __name__ == "__main__":
     
     arr = [4, 10, 3, 5, 1, 2]
     
     my_heap = MinHeap(arr)
     
     print(f"Output the initialized object: {my_heap.arr}")      # Output the initialized object: [None, 1, 4, 2, 5, 10, 3]
     
     my_heap.heapSort()
     
     print(f"Sorted output: {my_heap.heapSort()}")              # Sorted output: [10, 5, 4, 3, 2, 1]
     
     my_heap.get_min()
     
     print(f"The minimum value: {my_heap.get_min()}")           # The minimum value: 1
     
     my_heap.insert(15)
     
     print(f"Output the object: {my_heap.arr}")                 # Output the object: [None, 1, 4, 2, 5, 10, 3, 15]
     
     print(f"The object after deleting the minimum value: {my_heap.remove_min()}")       # The object after deleting the minimum value: 1 
    
