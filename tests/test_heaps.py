from unittest import TestCase
from data_structures.array_heap import ArrayHeap
from data_structures.max_array_heap import MaxArrayHeap
from data_structures.min_array_heap import MinArrayHeap
from data_structures.unordered_array_heap import UnorderedArrayHeap
from data_structures.linked_heap import MinLinkedHeap

def check_heap_ordering(heap, ordering):
    heap_array = heap._UnorderedArrayHeap__array
    bound = len(heap)
    for i in range(1, len(heap)):
        valid = (2*i     > bound or ordering(heap_array[i], heap_array[2*i    ])) and \
                (2*i + 1 > bound or ordering(heap_array[i], heap_array[2*i + 1]))
        if not valid: 
            print(heap_array, i)
            return False

    return True

class TestArrayHeap(TestCase):
    def test_init(self):
        heap = ArrayHeap(0, 'max')

        self.assertRaises(ValueError, lambda: ArrayHeap(-1, 'max'))
        self.assertRaises(ValueError, lambda: ArrayHeap(1, 'asdf'))
        self.assertRaises(ValueError, lambda: heap.add(1))
    
    def test_str(self):

        min_heap = ArrayHeap(10, 'min')
        max_heap = ArrayHeap(10, 'max')
        empty_min = "<ArrayHeap(min, [])>"
        empty_max = "<ArrayHeap(max, [])>"
        self.assertEqual(empty_min, str(min_heap))
        self.assertEqual(empty_max, str(max_heap))

        for i in range(8):
            min_heap.add(i)
            max_heap.add(i)
        
        filled_min = "<ArrayHeap(min, [0, 1, 2, 3, 4, 5, 6, 7])>"
        filled_max = "<ArrayHeap(max, [7, 6, 5, 3, 2, 1, 4, 0])>"
        self.assertEqual(filled_min, str(min_heap))
        self.assertEqual(filled_max, str(max_heap))

class TestMinArrayHeap(TestCase):
    def test_init(self):
        self.assertRaises(ValueError, lambda: MinArrayHeap(-1))

    def test_str(self):
        heap = MinArrayHeap(10)
        empty_str = '<MinArrayHeap([])>'
        self.assertEqual(empty_str, str(heap))
        
        for i in range(6):
            heap.add(i)
        
        filled_str = '<MinArrayHeap([0, 1, 2, 3, 4, 5])>'
        self.assertEqual(filled_str, str(heap))

class TestMaxArrayHeap(TestCase):

    def test_heapify_resize(self):
        generator = (i for i in range(10))
        self.assertRaises(TypeError, lambda: len(generator))

        heap = MaxArrayHeap.heapify(generator)
        self.assertTrue(check_heap_ordering(heap, lambda a, b: a >= b))
        self.assertEqual(len(heap), 10)

        empty_generator = (i for i in range(0))
        heap = MaxArrayHeap.heapify(empty_generator)
        self.assertTrue(check_heap_ordering(heap, lambda a, b: a >= b))
        self.assertEqual(len(heap), 0)

    
    def test_str(self):
        heap = MaxArrayHeap(10)
        empty_str = '<MaxArrayHeap([])>'
        self.assertEqual(empty_str, str(heap))
        
        for i in range(6):
            heap.add(i)
        
        filled_str = '<MaxArrayHeap([5, 3, 4, 0, 2, 1])>'
        self.assertEqual(filled_str, str(heap))

class TestUnorderedHeap(TestCase):
    def test_init(self):
        """ Unordered heap is still abstract (missing ordering and heapify) """
        self.assertRaises(TypeError, lambda: UnorderedArrayHeap(10))

class TestArrayHeaps(TestCase):
    CAPACITY = 10
    def setUp(self) -> None:
        self.heaps:list[UnorderedArrayHeap]  = [MaxArrayHeap(self.CAPACITY), ArrayHeap(self.CAPACITY, 'max'), MinArrayHeap(self.CAPACITY), ArrayHeap(self.CAPACITY, 'min')]
        self.orders = ['max', 'max', 'min', 'min']
        self.max_ordering = lambda a, b: a >= b
        self.min_ordering = lambda a, b: a <= b
    
    def test_add(self):
        for heap_order, heap in zip(self.orders, self.heaps):
            ordering = self.min_ordering if heap_order == 'min' else self.max_ordering
            for i in range(self.CAPACITY):
                self.assertEqual(i, len(heap))
                heap.add(i)
                self.assertTrue(check_heap_ordering(heap, ordering), str(heap))
            self.assertEqual(self.CAPACITY, len(heap), str(heap))

            self.assertRaises(ValueError, lambda: heap.add(1))
    
    
    def test_extract(self):
        for heap_order, heap in zip(self.orders, self.heaps):
            ordering = self.min_ordering if heap_order == 'min' else self.max_ordering

            self.assertRaises(ValueError, heap.extract_root)
            
            for i in range(self.CAPACITY):
                heap.add(i)
            
            for i in range(self.CAPACITY):
                self.assertEqual(len(heap), self.CAPACITY-i)
                root = heap.extract_root()
                expected_root = i if heap_order == 'min' else self.CAPACITY - i - 1

                self.assertEqual(root, expected_root)
                self.assertTrue(check_heap_ordering(heap, ordering))
            
            self.assertRaises(ValueError, heap.extract_root)

    def test_peek(self):
        for heap_order, heap in zip(self.orders, self.heaps):
            self.assertRaises(ValueError, heap.peek)

            for i in range(self.CAPACITY):
                heap.add(i)
                expected_root = 0 if heap_order == 'min' else i
                self.assertEqual(heap.peek(), expected_root)
            
            for i in range(self.CAPACITY):
                expected_root = i if heap_order == 'min' else self.CAPACITY - i - 1
                self.assertEqual(heap.peek(), expected_root)
                heap.extract_root()
            
            self.assertRaises(ValueError, heap.peek)

    def test_heapify(self):
        for heap_order, heap in zip(['max', 'min'], [self.heaps[0], self.heaps[2]]):
            num_items = self.CAPACITY
            heap_class = type(heap)
            items1 = list(range(num_items))
            items2 = list(reversed(range(num_items)))
            heap1 = heap_class.heapify(items1)
            heap2 = heap_class.heapify(items2)

            self.assertEqual(len(heap1), num_items)
            self.assertEqual(len(heap2), num_items)
            self.assertIs(type(heap1), heap_class)
            self.assertIs(type(heap2), heap_class)

            act_items1 = [heap1.extract_root() for _ in range(num_items)]
            act_items2 = [heap2.extract_root() for _ in range(num_items)]
            if heap_order == 'max':
                items1 = items1[::-1]
            self.assertEqual(act_items1, items1)
            self.assertEqual(act_items2, items1)
        
        #Separate ArrayHeap as heapify needs extra parameters
        for heap_order, heap in zip(['max', 'min'], [self.heaps[1], self.heaps[3]]):
            num_items = 10
            heap_class = type(heap)
            items1 = list(range(num_items))
            items2 = list(reversed(range(num_items)))
            heap1 = heap_class.heapify(items1, heap_order)
            heap2 = heap_class.heapify(items2, heap_order)

            self.assertEqual(len(heap1), num_items)
            self.assertEqual(len(heap2), num_items)
            self.assertIs(type(heap1), heap_class)
            self.assertIs(type(heap2), heap_class)

            act_items1 = [heap1.extract_root() for _ in range(num_items)]
            act_items2 = [heap2.extract_root() for _ in range(num_items)]
            if heap_order == 'max':
                items1 = items1[::-1]
            self.assertEqual(act_items1, items1)
            self.assertEqual(act_items2, items1)


        ArrayHeap.heapify([], 'max')

    def test_str(self):
        heap = ArrayHeap(10, 'min')
        empty_str = '<ArrayHeap(min, [])>'
        self.assertEqual(empty_str, str(heap))

        for i in range(6):
            heap.add(i)

        filled_str = '<ArrayHeap(min, [0, 1, 2, 3, 4, 5])>'
        self.assertEqual(filled_str, str(heap))

        heap = ArrayHeap(10, 'max')
        empty_str = '<ArrayHeap(max, [])>'
        self.assertEqual(empty_str, str(heap))

        for i in range(6):
            heap.add(i)

        filled_str = '<ArrayHeap(max, [5, 3, 4, 0, 2, 1])>'
        self.assertEqual(filled_str, str(heap))

class TestLinkedHeap(TestCase):
    def test_init(self):
        linked_heap = MinLinkedHeap()
        self.assertEqual(len(linked_heap), 0)
    
    def test_add(self):
        lh = MinLinkedHeap()
        num = 34
        for i in range(num):
            lh.add(i)
            tree = lh._MinLinkedHeap__root
            rank = tree.key
            for _ in range(rank):
                tree = tree.right
            self.assertIsNone(tree)
        
        self.assertEqual(len(lh), num)

    def test_extract(self):
        lh = MinLinkedHeap()
        items = [1,23,4,23,44,3,5,9,3,2]
        for i in items:
            lh.add(i)
        
        self.assertEqual(lh.peek(), 1)


        extracted_items = [lh.extract_root() for _ in range(len(items))]
        self.assertEqual(extracted_items, [1,2,3,3,4,5,9,23,23,44])
        self.assertEqual(len(lh), 0)

    def test_unbalanced(self):
        lh = MinLinkedHeap()
        for i in range(20, 0, -1):
            lh.add(i)
            self.assertEqual(lh._MinLinkedHeap__root.key, 1)
        
    def test_heapify(self):
        items = list(range(10))
        lh = MinLinkedHeap.heapify(items)
        self.assertEqual(10, len(lh))
        extracted_items = [lh.extract_root() for _ in range(len(items))]
        self.assertEqual(items, extracted_items)       

        items = []
        lh = MinLinkedHeap.heapify(items)
        self.assertEqual(0, len(lh))
        extracted_items = [lh.extract_root() for _ in range(len(items))]
        self.assertEqual(items, extracted_items)       

    def test_str(self):
        heap = MinLinkedHeap()
        empty_str = '<MinLinkedHeap([])>'
        self.assertEqual(empty_str, str(heap))

        for i in range(6):
            heap.add(i)

        filled_str = '<MinLinkedHeap([0, 2, 1, 3, 4, 5])>'
        self.assertEqual(filled_str, str(heap))
