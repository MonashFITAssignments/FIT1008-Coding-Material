from unittest import TestCase

from data_structures.linked_queue import LinkedQueue
from data_structures.circular_queue import CircularQueue

class TestCircularQueue(TestCase):
    EMPTY = 0
    ROOMY = 5
    LARGE = 10
    CAPACITY = 20

    def setUp(self) -> None:
        self.lengths = [self.EMPTY, self.ROOMY, self.LARGE, self.ROOMY, self.LARGE]
        self.queues = [CircularQueue(self.CAPACITY) for i in range(len(self.lengths))]
        for queue, length in zip(self.queues, self.lengths):
            for i in range(length):
                queue.append(i)
        self.empty_queue = self.queues[0]
        self.roomy_queue = self.queues[1]
        self.large_queue = self.queues[2]
        #we build empty queues from clear.
        #this is an indirect way of testing if clear works!
        #(perhaps not the best)
        self.clear_queue = self.queues[3]
        self.clear_queue.clear()
        self.lengths[3] = 0
        self.queues[4].clear()
        self.lengths[4] = 0

    def tearDown(self) -> None:
        for s in self.queues:
            s.clear()

    def test_init(self) -> None:
        self.assertTrue(self.empty_queue.is_empty())
        self.assertEqual(len(self.empty_queue), 0)

    def test_len(self) -> None:
        """ Tests the length of all queues created during setup."""
        for queue, length in zip(self.queues, self.lengths):
            self.assertEqual(len(queue), length)

    def test_is_empty_add(self) -> None:
        """ Tests queues that have been created empty/non-empty."""
        self.assertTrue(self.empty_queue.is_empty())
        self.assertFalse(self.roomy_queue.is_empty())
        self.assertFalse(self.large_queue.is_empty())

    def test_is_empty_clear(self) -> None:
        """ Tests queues that have been cleared."""
        for queue in self.queues:
            queue.clear()
            self.assertTrue(queue.is_empty())

    def test_is_empty_serve(self) -> None:
        """ Tests queues that have been served completely."""
        for queue in self.queues:
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
        self.assertFalse(self.empty_queue.is_full())
        self.assertFalse(self.roomy_queue.is_full())
        self.assertFalse(self.large_queue.is_full())

    def test_append_and_serve(self) -> None:
        for queue in self.queues:
            nitems = self.ROOMY
            for i in range(nitems):
                queue.append(i)
            for i in range(nitems):
                self.assertEqual(queue.serve(), i)

    def test_clear(self) -> None:
        for queue in self.queues:
            queue.clear()
            self.assertEqual(len(queue), 0)
            self.assertTrue(queue.is_empty())

    def test_str(self) -> None:
        empty_str = '<CircularQueue []>'
        self.assertEqual(empty_str, str(self.empty_queue))

        roomy_str = '<CircularQueue [0, 1, 2, 3, 4]>'
        self.assertEqual(roomy_str, str(self.roomy_queue))
        for _ in range(3):
            self.roomy_queue.append(self.roomy_queue.serve())
        roomy_str = '<CircularQueue [3, 4, 0, 1, 2]>'
        self.assertEqual(roomy_str, str(self.roomy_queue))

        #make sure the modulus code works
        for _ in range(self.CAPACITY - self.ROOMY):
            self.roomy_queue.append(self.roomy_queue.serve())
        roomy_str = '<CircularQueue [3, 4, 0, 1, 2]>'
        self.assertEqual(roomy_str, str(self.roomy_queue))


class TestLinkedQueue(TestCase):
    def setUp(self):
        self.queue = LinkedQueue()
    
    def test_append(self):
        self.queue.append(1)
        self.assertEqual(self.queue.peek(), 1)
        self.queue.append(2)
        self.assertEqual(self.queue.peek(), 1)
    
    def test_len(self):
        self.queue.append(1)
        self.assertEqual(len(self.queue), 1)
        self.queue.append(2)
        self.assertEqual(len(self.queue), 2)
        self.queue.serve()
        self.assertEqual(len(self.queue), 1)
        self.queue.peek()
        self.assertEqual(len(self.queue), 1)

    def test_serve(self):
        self.queue.append(1)
        self.queue.append(2)
        self.queue.append(3)
        self.assertEqual(self.queue.serve(), 1)
        self.assertEqual(self.queue.peek(), 2)
        self.assertEqual(self.queue.serve(), 2)
        self.assertEqual(self.queue.peek(), 3)
        self.assertEqual(self.queue.serve(), 3)
        self.assertTrue(self.queue.is_empty())
    
    def test_peek(self):
        for i in range(10):
            self.queue.append(i + 1)
        self.assertEqual(self.queue.peek(), 1)
        for i in range(10):
            self.queue.serve()
            if i < 9:
                self.assertEqual(self.queue.peek(), i + 2)
        self.assertTrue(self.queue.is_empty())
    
    def test_is_empty(self):
        self.assertTrue(self.queue.is_empty())
        self.queue.append(1)
        self.assertFalse(self.queue.is_empty())
    
    def test_clear(self):
        self.queue.append(1)
        self.queue.append(2)
        self.queue.clear()
        self.assertTrue(self.queue.is_empty())
        self.assertEqual(len(self.queue), 0)
        self.assertRaises(Exception, self.queue.serve)
        self.assertRaises(Exception, self.queue.peek)

    def test_str(self):
        empty_str = '<LinkedQueue []>'
        self.assertEqual(empty_str, str(self.queue))

        self.queue.append(0)
        self.queue.append(1)
        self.queue.append(2)
        self.queue.append(3)
        self.queue.append(4)

        roomy_str = '<LinkedQueue [0, 1, 2, 3, 4]>'
        self.assertEqual(roomy_str, str(self.queue))
        for _ in range(3):
            self.queue.append(self.queue.serve())
        roomy_str = '<LinkedQueue [3, 4, 0, 1, 2]>'
        self.assertEqual(roomy_str, str(self.queue))

        #make sure the modulus code works
        for _ in range(len(self.queue)):
            self.queue.append(self.queue.serve())
        roomy_str = '<LinkedQueue [3, 4, 0, 1, 2]>'
        self.assertEqual(roomy_str, str(self.queue))
