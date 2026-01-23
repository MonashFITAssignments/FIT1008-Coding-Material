from unittest import TestCase

from data_structures.array_stack import ArrayStack
from data_structures.linked_stack import LinkedStack

class TestStack(TestCase):
    EMPTY = 0
    ROOMY = 5
    LARGE = 10
    CAPACITY = 20

    def setUp(self) -> None:
        self._lengths = [self.EMPTY, self.ROOMY, self.LARGE, self.ROOMY, self.LARGE]
        self._stacks = [ArrayStack(self.CAPACITY) for i in range(len(self._lengths))]
        for stack, length in zip(self._stacks, self._lengths):
            for i in range(length):
                stack.push(i)
        self._empty_stack = self._stacks[0]
        self._roomy_stack = self._stacks[1]
        self._large_stack = self._stacks[2]
        #we build empty stacks from clear.
        #this is an indirect way of testing if clear works!
        #(perhaps not the best)
        self._clear_stack = self._stacks[3]
        self._clear_stack.clear()
        self._lengths[3] = 0
        self._stacks[4].clear()
        self._lengths[4] = 0

    def tearDown(self) -> None:
        for s in self._stacks:
            s.clear()

    def test_init(self) -> None:
        self.assertTrue(self._empty_stack.is_empty())
        self.assertEqual(len(self._empty_stack), 0)

    def test_len(self) -> None:
        """ Tests the length of all stacks created during setup."""
        for stack, length in zip(self._stacks, self._lengths):
            self.assertEqual(len(stack), length)

    def test_is_empty_add(self) -> None:
        """ Tests stacks that have been created empty/non-empty."""
        self.assertTrue(self._empty_stack.is_empty())
        self.assertFalse(self._roomy_stack.is_empty())
        self.assertFalse(self._large_stack.is_empty())

    def test_is_empty_clear(self) -> None:
        """ Tests stacks that have been cleared."""
        for stack in self._stacks:
            stack.clear()
            self.assertTrue(stack.is_empty())

    def test_is_empty_pop(self) -> None:
        """ Tests stacks that have been popped completely."""
        for stack in self._stacks:
            #we empty the stack
            try:
                while True:
                    was_empty = stack.is_empty()
                    stack.pop()
                    #if we have popped without raising an assertion,
                    #then the stack was not empty.
                    self.assertFalse(was_empty)
            except:
                self.assertTrue(stack.is_empty())

    def test_is_full_add(self) -> None:
        """ Tests stacks that have been created not full."""
        self.assertFalse(self._empty_stack.is_full())
        self.assertFalse(self._roomy_stack.is_full())
        self.assertFalse(self._large_stack.is_full())

    def test_push_and_pop(self) -> None:
        for stack in self._stacks:
            nitems = self.ROOMY
            for i in range(nitems):
                stack.push(i)
            for i in range(nitems-1, -1, -1):
                self.assertEqual(stack.pop(), i)

    def test_clear(self) -> None:
        for stack in self._stacks:
            stack.clear()
            self.assertEqual(len(stack), 0)
            self.assertTrue(stack.is_empty())

    def test_str(self) -> None:
        for stack in self._stacks:
            self.assertEqual(str(stack), f'<ArrayStack [{", ".join(str(i) for i in range(len(stack)))}]>')
    
        for _ in range(2):
            self._roomy_stack.pop()
        roomy_str = '<ArrayStack [0, 1, 2]>'
        self.assertEqual(roomy_str, str(self._roomy_stack))


class TestLinkedStack(TestCase):
    
    def setUp(self):
        self._stack = LinkedStack()

    def test_push(self):
        self._stack.push(1)
        self.assertEqual(self._stack.peek(), 1)
        self._stack.push(2)
        self.assertEqual(self._stack.peek(), 2)
    
    def test_len(self):
        self._stack.push(1)
        self.assertEqual(len(self._stack), 1)
        self._stack.push(2)
        self.assertEqual(len(self._stack), 2)
        self._stack.pop()
        self.assertEqual(len(self._stack), 1)

    def test_pop(self):
        self._stack.push(1)
        self._stack.push(2)
        self._stack.push(3)
        self.assertEqual(self._stack.pop(), 3)
        self.assertEqual(self._stack.peek(), 2)
        self.assertEqual(self._stack.pop(), 2)
        self.assertEqual(self._stack.peek(), 1)
        self.assertEqual(self._stack.pop(), 1)
        self.assertTrue(self._stack.is_empty())

    def test_peek(self):
        # Push 1 to 10 to the stack
        for i in range(10):
            self._stack.push(i + 1)
        self.assertEqual(self._stack.peek(), 10)

    def test_is_empty(self):
        self.assertTrue(self._stack.is_empty())
        self._stack.push(1)
        self.assertFalse(self._stack.is_empty())

    def test_clear(self):
        self._stack.push(1)
        self._stack.push(2)
        self._stack.clear()
        self.assertTrue(self._stack.is_empty())
        self.assertEqual(len(self._stack), 0)
        self.assertRaises(Exception, self._stack.pop)
        self.assertRaises(Exception, self._stack.peek)

    def test_str(self):
        empty_str = '<LinkedStack []>'
        self.assertEqual(empty_str, str(self._stack))

        self._stack.push(0)
        self._stack.push(1)
        self._stack.push(2)
        self._stack.push(3)
        self._stack.push(4)

        roomy_str = '<LinkedStack [0, 1, 2, 3, 4]>'
        self.assertEqual(roomy_str, str(self._stack))
        for _ in range(2):
            self._stack.pop()
        roomy_str = '<LinkedStack [0, 1, 2]>'
        self.assertEqual(roomy_str, str(self._stack))
