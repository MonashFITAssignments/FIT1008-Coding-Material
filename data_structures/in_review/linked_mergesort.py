# def merge_linked(list1, list2, key = lambda x:x):
#     res = type(list1)()
#     iter1 = iter(list1)
#     iter2 = iter(list2)
#     is_first_list = True
#     try:
#         a = next(iter1)
#         while True:
#             for b in iter2:
#                 a_key = key(a); b_key = key(b)
#                 if a_key < b_key or a_key == b_key and is_first_list:
#                     res.append(a)
#                     iter2, iter1 = iter1, iter2
#                     is_first_list = not is_first_list
#                     a = b
#                     break
#                 else:
#                     res.append(b)
#             else:
#                 res.append(a)
#                 iter2 = iter1
#                 break
#     except StopIteration:
#         pass
#     finally:
#         for item in iter2:
#             res.append(item)
#         return res
        

# def _merge_linked(list1:Node, list2:Node, key:Callable[[T], bool]):
#     top = Node(None)
#     bottom = top
#     while list1 is not None and list2 is not None:
#         if key(list1.item) <= key(list2.item):
#             bottom.link = list1
#             list1 = list1.link
#             bottom = bottom.link
#         else:
#             bottom.link = list2
#             list2 = list2.link
#             bottom = bottom.link
#     if list1 is None:
#         bottom.link = list2
#     else:
#         bottom.link = list1
#     return top.link

# def _mergesort_linked(my_list, key=lambda x:x):
#     if len(my_list) == 0:
#         return type(my_list)()
#     front = None
#     rear = None
#     for i in my_list:    
#         front = Node(Node(i), front)
#         if rear is None:
#             rear = front
    
#     def node_iter(node:Node):
#         while node is not None:
#             yield node.item
#             node = node.link
#     queue_iter = node_iter(front)
#     for l1, l2 in zip(queue_iter, queue_iter):
#         rear.link = Node(_merge_linked(l1, l2, key))
#         rear = rear.link
#     sorted_list = rear.item
#     res = type(my_list)()
#     for item in node_iter(sorted_list):
#         res.append(item)
#     return res

