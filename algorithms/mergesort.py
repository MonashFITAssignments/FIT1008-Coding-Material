from __future__ import annotations
from data_structures.referential_array import ArrayR
from data_structures.abstract_list import List
from typing import TypeVar

T = TypeVar("T")

def merge(items1: List[T] | ArrayR[T], items2: List[T] | ArrayR[T], key = lambda x:x) -> List[T] | ArrayR[T]:
    """
    Merges two sorted lists into one larger sorted list,
    containing all elements from the smaller lists.

    The `key` kwarg allows you to define a custom sorting order.

    returns:
    The sorted list in the same type as the input lists.

    pre:
    Both l1 and l2 are sorted, and contain comparable elements.

    complexity:
    Best/Worst Case: O(n), n = len(l1)+len(l2).
    """
    if type(items1) is not type(items2):
        raise ValueError(f"cannot merge collections '{type(items1).__name__}' '{type(items2).__name__}' of differing type")
    if type(items1) is ArrayR:
        return _merge_array(items1, items2, key)
    arr1 = ArrayR.from_list(items1)
    arr2 = ArrayR.from_list(items2)
    arr3 = _merge_array(arr1, arr2, key)
    #Create new list of same type as input
    res = type(items1)()
    for item in arr3:
        res.append(item)
    return res


def _merge_array(list1: ArrayR[T], list2: ArrayR[T], key) -> ArrayR[T]:
    
    n = len(list1) + len(list2)
    res = type(list1)(n)
    ia = 0
    ib = 0
    
    for _ in range(n):
        if ia >= len(list1):
            res[ia + ib] = list2[ib]
            ib += 1
        elif ib >= len(list2):
            res[ia + ib] = list1[ia]
            ia += 1
        elif key(list1[ia]) <= key(list2[ib]):
            res[ia + ib] = list1[ia]
            ia += 1
        else:
            res[ia + ib] = list2[ib]
            ib += 1
    return res

def _mergesort_array(my_list: ArrayR, key) -> ArrayR:
    if len(my_list) <= 1:
        return my_list
    
    # Split the list into two halves
    break_index = (len(my_list)+1) // 2
    
    # Create two new lists to hold the two halves.
    
    left_half = ArrayR(break_index)
    right_half = ArrayR(len(my_list) - break_index)

    # Now fill the two halves with the elements from the original list
    # Left half
    for i in range(break_index):
        left_half[i] = my_list[i]
    
    # Right half
    for i in range(break_index, len(my_list)):
        right_half[i - break_index] = my_list[i]
    
    # Recursively sort the two halves and merge them
    arr1 = _mergesort_array(left_half, key)
    arr2 = _mergesort_array(right_half, key)
    return _merge_array(arr1, arr2, key)

def mergesort(my_list: List[T] | ArrayR[T], key = lambda x: x) -> List[T] | ArrayR[T]:
    """
    Sort a list using the mergesort operation.

    The `key` kwarg allows you to define a custom sorting order.

    complexity:
    Best/Worst Case: O(NlogN) where N is the length of the list.

    Return type is the same as the input type.
    """
    if type(my_list) is ArrayR:
        return _mergesort_array(my_list, key)
    else:
        array = ArrayR.from_list(my_list)
        array = _mergesort_array(array, key)
        #Create new list of same type as input
        res = type(my_list)() 
        for item in array:
            res.append(item)
        return res