from unittest import TestCase

from data_structures.array_stack import ArrayStack
from data_structures.linked_stack import LinkedStack

class TestStack(TestCase):
    EMPTY = 0
    ROOMY = 5
    LARGE = 10
    CAPACITY = 20

    def setUp(self) -> None:
        self.lengths = [self.EMPTY, self.ROOMY, self.LARGE, self.ROOMY, self.LARGE]
        self.stacks = [ArrayStack(self.CAPACITY) for i in range(len(self.lengths))]
        for stack, length in zip(self.stacks, self.lengths):
            for i in range(length):
                stack.push(i)
        self.empty_stack = self.stacks[0]
        self.roomy_stack = self.stacks[1]
        self.large_stack = self.stacks[2]
        #we build empty stacks from clear.
        #this is an indirect way of testing if clear works!
        #(perhaps not the best)
        self.clear_stack = self.stacks[3]
        self.clear_stack.clear()
        self.lengths[3] = 0
        self.stacks[4].clear()
        self.lengths[4] = 0

    def tearDown(self) -> None:
        for s in self.stacks:
            s.clear()

    def test_init(self) -> None:
        self.assertTrue(self.empty_stack.is_empty())
        self.assertEqual(len(self.empty_stack), 0)

    def test_len(self) -> None:
        """ Tests the length of all stacks created during setup."""
        for stack, length in zip(self.stacks, self.lengths):
            self.assertEqual(len(stack), length)

    def test_is_empty_add(self) -> None:
        """ Tests stacks that have been created empty/non-empty."""
        self.assertTrue(self.empty_stack.is_empty())
        self.assertFalse(self.roomy_stack.is_empty())
        self.assertFalse(self.large_stack.is_empty())

    def test_is_empty_clear(self) -> None:
        """ Tests stacks that have been cleared."""
        for stack in self.stacks:
            stack.clear()
            self.assertTrue(stack.is_empty())

    def test_is_empty_pop(self) -> None:
        """ Tests stacks that have been popped completely."""
        for stack in self.stacks:
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
        self.assertFalse(self.empty_stack.is_full())
        self.assertFalse(self.roomy_stack.is_full())
        self.assertFalse(self.large_stack.is_full())

    def test_push_and_pop(self) -> None:
        for stack in self.stacks:
            nitems = self.ROOMY
            for i in range(nitems):
                stack.push(i)
            for i in range(nitems-1, -1, -1):
                self.assertEqual(stack.pop(), i)

    def test_clear(self) -> None:
        for stack in self.stacks:
            stack.clear()
            self.assertEqual(len(stack), 0)
            self.assertTrue(stack.is_empty())

    def test_str(self) -> None:
        for stack in self.stacks:
            self.assertEqual(str(stack), f'<ArrayStack [{", ".join(str(i) for i in range(len(stack)))}]>')
    
        for _ in range(2):
            self.roomy_stack.pop()
        roomy_str = '<ArrayStack [0, 1, 2]>'
        self.assertEqual(roomy_str, str(self.roomy_stack))


class TestLinkedStack(TestCase):
    
    def setUp(self):
        self.stack = LinkedStack()

    def test_push(self):
        self.stack.push(1)
        self.assertEqual(self.stack.peek(), 1)
        self.stack.push(2)
        self.assertEqual(self.stack.peek(), 2)
    
    def test_len(self):
        self.stack.push(1)
        self.assertEqual(len(self.stack), 1)
        self.stack.push(2)
        self.assertEqual(len(self.stack), 2)
        self.stack.pop()
        self.assertEqual(len(self.stack), 1)

    def test_pop(self):
        self.stack.push(1)
        self.stack.push(2)
        self.stack.push(3)
        self.assertEqual(self.stack.pop(), 3)
        self.assertEqual(self.stack.peek(), 2)
        self.assertEqual(self.stack.pop(), 2)
        self.assertEqual(self.stack.peek(), 1)
        self.assertEqual(self.stack.pop(), 1)
        self.assertTrue(self.stack.is_empty())

    def test_peek(self):
        # Push 1 to 10 to the stack
        for i in range(10):
            self.stack.push(i + 1)
        self.assertEqual(self.stack.peek(), 10)

    def test_is_empty(self):
        self.assertTrue(self.stack.is_empty())
        self.stack.push(1)
        self.assertFalse(self.stack.is_empty())

    def test_clear(self):
        self.stack.push(1)
        self.stack.push(2)
        self.stack.clear()
        self.assertTrue(self.stack.is_empty())
        self.assertEqual(len(self.stack), 0)
        self.assertRaises(Exception, self.stack.pop)
        self.assertRaises(Exception, self.stack.peek)

    def test_str(self):
        empty_str = '<LinkedStack []>'
        self.assertEqual(empty_str, str(self.stack))

        self.stack.push(0)
        self.stack.push(1)
        self.stack.push(2)
        self.stack.push(3)
        self.stack.push(4)

        roomy_str = '<LinkedStack [0, 1, 2, 3, 4]>'
        self.assertEqual(roomy_str, str(self.stack))
        for _ in range(2):
            self.stack.pop()
        roomy_str = '<LinkedStack [0, 1, 2]>'
        self.assertEqual(roomy_str, str(self.stack))
