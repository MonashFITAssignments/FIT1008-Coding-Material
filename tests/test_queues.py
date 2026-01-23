from unittest import TestCase

from data_structures.linked_queue import LinkedQueue
from data_structures.circular_queue import CircularQueue

class TestCircularQueue(TestCase):
    EMPTY = 0
    ROOMY = 5
    LARGE = 10
    CAPACITY = 20

    def setUp(self) -> None:
        self._lengths = [self.EMPTY, self.ROOMY, self.LARGE, self.ROOMY, self.LARGE]
        self._queues = [CircularQueue(self.CAPACITY) for i in range(len(self._lengths))]
        for queue, length in zip(self._queues, self._lengths):
            for i in range(length):
                queue.append(i)
        self._empty_queue = self._queues[0]
        self._roomy_queue = self._queues[1]
        self._large_queue = self._queues[2]
        #we build empty queues from clear.
        #this is an indirect way of testing if clear works!
        #(perhaps not the best)
        self._clear_queue = self._queues[3]
        self._clear_queue.clear()
        self._lengths[3] = 0
        self._queues[4].clear()
        self._lengths[4] = 0

    def tearDown(self) -> None:
        for s in self._queues:
            s.clear()

    def test_init(self) -> None:
        self.assertTrue(self._empty_queue.is_empty())
        self.assertEqual(len(self._empty_queue), 0)

    def test_len(self) -> None:
        """ Tests the length of all queues created during setup."""
        for queue, length in zip(self._queues, self._lengths):
            self.assertEqual(len(queue), length)

    def test_is_empty_add(self) -> None:
        """ Tests queues that have been created empty/non-empty."""
        self.assertTrue(self._empty_queue.is_empty())
        self.assertFalse(self._roomy_queue.is_empty())
        self.assertFalse(self._large_queue.is_empty())

    def test_is_empty_clear(self) -> None:
        """ Tests queues that have been cleared."""
        for queue in self._queues:
            queue.clear()
            self.assertTrue(queue.is_empty())

    def test_is_empty_serve(self) -> None:
        """ Tests queues that have been served completely."""
        for queue in self._queues:
            #we empty the queue
            try:
                while True:
                    was_empty = queue.is_empty()
                    queue.serve()
                    #if we have served without raising an assertion,
                    #then the queue was not empty.
                    self.assertFalse(was_empty)
            except:
                self.assertTrue(queue.is_empty())

    def test_is_full_add(self) -> None:
        """ Tests queues that have been created not full."""
        self.assertFalse(self._empty_queue.is_full())
        self.assertFalse(self._roomy_queue.is_full())
        self.assertFalse(self._large_queue.is_full())

    def test_append_and_serve(self) -> None:
        for queue in self._queues:
            nitems = self.ROOMY
            for i in range(nitems):
                queue.append(i)
            for i in range(nitems):
                self.assertEqual(queue.serve(), i)

    def test_clear(self) -> None:
        for queue in self._queues:
            queue.clear()
            self.assertEqual(len(queue), 0)
            self.assertTrue(queue.is_empty())

    def test_str(self) -> None:
        empty_str = '<CircularQueue []>'
        self.assertEqual(empty_str, str(self._empty_queue))

        roomy_str = '<CircularQueue [0, 1, 2, 3, 4]>'
        self.assertEqual(roomy_str, str(self._roomy_queue))
        for _ in range(3):
            self._roomy_queue.append(self._roomy_queue.serve())
        roomy_str = '<CircularQueue [3, 4, 0, 1, 2]>'
        self.assertEqual(roomy_str, str(self._roomy_queue))

        #make sure the modulus code works
        for _ in range(self.CAPACITY - self.ROOMY):
            self._roomy_queue.append(self._roomy_queue.serve())
        roomy_str = '<CircularQueue [3, 4, 0, 1, 2]>'
        self.assertEqual(roomy_str, str(self._roomy_queue))


class TestLinkedQueue(TestCase):
    def setUp(self):
        self._queue = LinkedQueue()
    
    def test_append(self):
        self._queue.append(1)
        self.assertEqual(self._queue.peek(), 1)
        self._queue.append(2)
        self.assertEqual(self._queue.peek(), 1)
    
    def test_len(self):
        self._queue.append(1)
        self.assertEqual(len(self._queue), 1)
        self._queue.append(2)
        self.assertEqual(len(self._queue), 2)
        self._queue.serve()
        self.assertEqual(len(self._queue), 1)
        self._queue.peek()
        self.assertEqual(len(self._queue), 1)

    def test_serve(self):
        self._queue.append(1)
        self._queue.append(2)
        self._queue.append(3)
        self.assertEqual(self._queue.serve(), 1)
        self.assertEqual(self._queue.peek(), 2)
        self.assertEqual(self._queue.serve(), 2)
        self.assertEqual(self._queue.peek(), 3)
        self.assertEqual(self._queue.serve(), 3)
        self.assertTrue(self._queue.is_empty())
    
    def test_peek(self):
        for i in range(10):
            self._queue.append(i + 1)
        self.assertEqual(self._queue.peek(), 1)
        for i in range(10):
            self._queue.serve()
            if i < 9:
                self.assertEqual(self._queue.peek(), i + 2)
        self.assertTrue(self._queue.is_empty())

    def test_peek_node(self):
        self._queue.append(1)
        self.assertEqual(self._queue.peek_node()._item, 1)
        self._queue.append(2)
        self.assertEqual(self._queue.peek_node()._item, 1)
        self._queue.serve()
        self.assertEqual(self._queue.peek_node()._item, 2)
        self.assertEqual(self._queue.peek_node()._link, None)
    
    def test_is_empty(self):
        self.assertTrue(self._queue.is_empty())
        self._queue.append(1)
        self.assertFalse(self._queue.is_empty())
    
    def test_clear(self):
        self._queue.append(1)
        self._queue.append(2)
        self._queue.clear()
        self.assertTrue(self._queue.is_empty())
        self.assertEqual(len(self._queue), 0)
        self.assertRaises(Exception, self._queue.serve)
        self.assertRaises(Exception, self._queue.peek)

    def test_str(self):
        empty_str = '<LinkedQueue []>'
        self.assertEqual(empty_str, str(self._queue))

        self._queue.append(0)
        self._queue.append(1)
        self._queue.append(2)
        self._queue.append(3)
        self._queue.append(4)

        roomy_str = '<LinkedQueue [0, 1, 2, 3, 4]>'
        self.assertEqual(roomy_str, str(self._queue))
        for _ in range(3):
            self._queue.append(self._queue.serve())
        roomy_str = '<LinkedQueue [3, 4, 0, 1, 2]>'
        self.assertEqual(roomy_str, str(self._queue))

        #make sure the modulus code works
        for _ in range(len(self._queue)):
            self._queue.append(self._queue.serve())
        roomy_str = '<LinkedQueue [3, 4, 0, 1, 2]>'
        self.assertEqual(roomy_str, str(self._queue))
