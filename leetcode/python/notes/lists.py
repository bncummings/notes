# initialize an empty list
empty_list = []

# initialize a list with some values
list_with_values = [1, 2, 3, 4, 5]

# list of size n with the same vlaue
n = 5
value = 0
list_of_size_n = [value] * n  # [0, 0, 0, 0, 0]

# access elements
first_element = list_with_values[0]  # 1
last_element = list_with_values[-1]  # 5

# slicing syntax: [first_to_include : stop_before]
example = [1, 2, 3, 4, 5]

sublist = example[1:4]  # [2, 3, 4]
sublist_from_start = example[:3]  # [1, 2, 3]
sublist_to_end = example[2:]  # [3, 4, 5]

# iterate through a list`
# 1. using a for loop
for item in list_with_values:
    print(item) # prints 1, 2, 3, 4, 5

# 2. using indexes
for i in range(len(list_with_values)):
    print(list_with_values[i])  # prints 1, 2, 3,   

# add an element to the end of the list
example.append(6)  # [1, 2, 3, 4, 5, 6]

# remove an element from the list by value
example.remove(3)  # [1, 2, 4, 5, 6]`

# remove an element from the list by index
removed_element = example.pop(2)  # removed_element = 4, example = [1, 2, 5, 6]

# find the index of an element
index_of_5 = example.index(5)  # 2  

# check if an element is in the list
is_in_list = 4 in example  # False
is_in_list = 5 in example  # True

# get the length of the list
length = len(example)  # 4

# iterate through a list with both index and value
for index, value in enumerate(example):
    print(f"Index: {index}, Value: {value}")  # prints Index: 0, Value: 1 ... Index: 3, Value:


# list comprehension
# syntax: [expression for item in iterable if condition]
squared = [x**2 for x in range(10)]  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# deleting vs removing
# remove() removes the first occurrence of a value
# del removes an element at a specific index or slice
example = [1, 2, 3, 4, 5, 3]
example.remove(3)  # example = [1, 2, 4, 5, 3]
del example[1]    # example = [1, 4, 5, 3]
del example[1:3] # example = [1, 3]

# sorting a list
unsorted_list = [5, 2, 9, 1, 5, 6]
# .sort() method
unsorted_list.sort()  # unsorted_list = [1, 2, 5, 5, 6, 9]
# or use stlb sorted(list[]) function
sorted_list = sorted(unsorted_list)  # sorted_list = [1, 2, 5, 5, 6, 9]
