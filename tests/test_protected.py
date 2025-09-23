from unittest import TestCase
from data_structures.array_heap import ArrayHeap
from data_structures.array_list import ArrayList
from data_structures.array_set import ArraySet
from data_structures.array_sorted_list import ArraySortedList
from data_structures.array_sorted_set import ArraySortedSet
from data_structures.array_stack import ArrayStack
from data_structures.binary_search_tree import BinarySearchTree
from data_structures.bit_vector_set import BitVectorSet
from data_structures.circular_queue import CircularQueue
from data_structures.sunder_protected import ProtectAttributes
from data_structures.hash_table_double_hashing import DoubleHashingTable
from data_structures.hash_table_linear_probing import LinearProbeTable
from data_structures.hash_table_quadratic_probing import QuadraticProbeTable
from data_structures.hash_table_separate_chaining import SeparateChainingTable
from data_structures.linked_heap import MinLinkedHeap
from data_structures.linked_list import LinkedList
from data_structures.linked_queue import LinkedQueue
from data_structures.linked_stack import LinkedStack
from data_structures.max_array_heap import MaxArrayHeap
from data_structures.min_array_heap import MinArrayHeap

def global_function_attr(obj):
    obj._a
def global_function_class(obj):
    obj._protected_class_attr
def global_function_method(obj):
    obj._protected_call

class ProtectedParent(ProtectAttributes):
    _protected_class_attr = 10
    __private_class_attr = 12

    _to_overide = 20
    __to_overide = 30
    def __init__(self):
        self._a = 1
        self.calls = 0
        
    def _protected_call(self):
        self.calls += 1
    def __private_call(self):
        self.calls -= 1
    def public_call(self):
        self._protected_call()

    def get_protected_class(self):
        return self._protected_class_attr
    def set_protected_class(self, x):
        self._protected_class_attr = x

    def get_private_class(self):
        return self.__private_class_attr
    def set_private_class(self, x):
        self.__private_class_attr = x
    
    def get_protected_overide(self):
        return self._to_overide
    
    def get_private_overide(self):
        return self.__to_overide

class ProtectedChild(ProtectedParent):
    def _protected_call(self):
        self.calls += 2
    def get_a(self):
        return self._a
    def public_call2(self):
        self._protected_call()

class ProtectedChild2(ProtectedParent):
    _to_overide = 21
    __to_overide = 31
    def get_protected_class(self):
        return self._protected_class_attr
    def set_protected_class(self, x):
        self._protected_class_attr = x

    def get_private_class(self):
        return self.__private_class_attr
    def set_private_class(self, x):
        self.__private_class_attr = x

    def get_private_overide(self):
        return self.__to_overide

class Foo:
    pass
class Bar:
    pass
class A(ProtectAttributes, Foo, Bar):
    def __init__(self):
        self._a = None
class B(Foo, ProtectAttributes, Bar):
    def __init__(self):
        self._a = None
class C(Foo, Bar, ProtectAttributes):
    def __init__(self):
        self._a = None
    

class TestProtected(TestCase):
    def setUp(self):
        self.parent = ProtectedParent()
        self.child = ProtectedChild()
        #Check that creating a second instance of the class doesn't break things
        self.parent2 = ProtectedParent()
        self.child2 = ProtectedChild2()
        #Check accessing protected attributes raises attribute error

    def test_inherintance_order(self):
        #Check that the order of inheritance does not affect the name of protection.
        a = A()
        b = B()
        c = C()
        a._ProtectedA__a
        b._ProtectedB__a
        c._ProtectedC__a

    def test_attributes(self):
        # print(self.child.__dict__)
        # print(ProtectedChild.__dict__)
        self.assertRaises(AttributeError, lambda: self.parent._a)
        self.assertRaises(AttributeError, lambda: self.parent2._a)
        self.assertRaises(AttributeError, lambda: self.child._a)
        self.assertRaises(AttributeError, lambda: self.child2._a)
        self.assertEqual(self.parent2._ProtectedProtectedParent__a, 1)
        self.assertEqual(self.child2._ProtectedProtectedParent__a, 1)

        #Check that child can access protected attribute
        self.assertEqual(1, self.child.get_a())

        def set_a(obj):
            obj._a = 2
        
        #Check that protected attributes cannot be set
        self.assertRaises(AttributeError, set_a, self.parent)
        self.assertRaises(AttributeError, set_a, self.child)
        self.assertRaises(AttributeError, set_a, self.parent2)


        self.parent.public_call()
        self.child.public_call()

        #Check that children can overwrite protected methods
        self.assertEqual(self.parent.calls, 1)
        self.assertEqual(self.child.calls, 2)

    def test_methods(self):
        #Check that protected calls cannot be called
        self.assertRaises(AttributeError, lambda: self.parent._protected_call())
        self.assertRaises(AttributeError, lambda: self.child._protected_call())

        self.child.public_call2()
        self.assertEqual(self.child.calls, 2)
    
    def test_class_attrs(self):
        #Getting class attributes from methods works
        self.assertEqual(self.parent.get_protected_class(), 10)
        self.assertEqual(self.parent.get_private_class(), 12)
        self.assertEqual(self.child.get_protected_class(), 10)
        self.assertEqual(self.child.get_private_class(), 12)
        self.assertEqual(self.child2.get_protected_class(), 10)
        self.assertRaises(AttributeError, self.child2.get_private_class)

        #Setting class attributes from methods works
        self.parent.set_protected_class(11)
        self.assertEqual(self.parent.get_protected_class(), 11)
        self.parent.set_private_class(13)
        self.assertEqual(self.parent.get_private_class(), 13)
        self.assertEqual(self.parent2.get_protected_class(), 10)
        self.assertEqual(self.parent2.get_private_class(), 12)

        self.child.set_protected_class(110)
        self.assertEqual(self.child.get_protected_class(), 110)
        self.child.set_private_class(130)
        self.assertEqual(self.child.get_private_class(), 130)

        self.child2.set_private_class(120)
        self.assertEqual(self.child2.get_private_class(), 120) #This adds a new attribute which won't be protected, but won't raise error anymore

        #Check that children properly inheritted attributes
        self.assertEqual(self.child._ProtectedProtectedParent__to_overide, 20)
        self.assertEqual(self.child._ProtectedProtectedParent__ProtectedParent__to_overide, 30)

        #Check that children overide inheritted attributes
        self.assertEqual(self.child2._ProtectedProtectedParent__to_overide, 21)
        self.assertEqual(self.child2._ProtectedProtectedParent__ProtectedChild2__to_overide, 31)

    def test_global_funcs(self):
        self.assertRaises

    def test_adt_attrs(self):
        array_attr = [
            ArrayHeap(10, "min"),
            ArrayList(10),
            ArraySet(10),
            ArraySortedList(10),
            ArraySortedSet(10),
            ArrayStack(10),
            CircularQueue(10),
            DoubleHashingTable(),
            QuadraticProbeTable(),
            LinearProbeTable(),
            MaxArrayHeap(10),
            MinArrayHeap(10),
        ]
        
        for adt in array_attr:
            for attr in adt.__dict__:
                if '_array' in attr: 
                    break
            else: 
                self.fail(f"Array class '{type(adt).__name__}' does not have an array attribute")
            self.assertRaises(AttributeError, lambda: adt._array)
        
        length_attr = array_attr[:]
        bst = BinarySearchTree(); length_attr.append(bst)
        self.assertRaises(AttributeError, lambda: bst.__root)
        self.assertRaises(AttributeError, lambda: bst.__get_max_node(None))

        bsv = BitVectorSet()
        self.assertRaises(AttributeError, lambda: bsv._elems)
        
        htsc = SeparateChainingTable(); length_attr.append(htsc)
        self.assertRaises(AttributeError, lambda: htsc._table)

        mlh = MinLinkedHeap()
        self.assertRaises(AttributeError, lambda: mlh._root)
        self.assertRaises(AttributeError, lambda: mlh.__merge(None, None))

        ll = LinkedList(); length_attr.append(ll)
        self.assertRaises(AttributeError, lambda: ll._head)
        self.assertRaises(AttributeError, lambda: ll._rear)
        self.assertRaises(AttributeError, lambda: ll.__get_node_at_index(2))

        lq = LinkedQueue(); length_attr.append(lq)
        self.assertRaises(AttributeError, lambda: lq._front)
        self.assertRaises(AttributeError, lambda: lq._rear)

        ls = LinkedStack(); length_attr.append(ls)
        self.assertRaises(AttributeError, lambda: ls._top)
        
        for ht in array_attr[7:10]:
            self.assertRaises(AttributeError, lambda: ht._TABLE_SIZES)
        
        
        for adt in length_attr:
            for attr in adt.__dict__:
                if '_length' in attr:
                    break
            else:
                self.fail(f"Length class '{type(adt).__name__}' does not have a length attribute")
            self.assertRaises(AttributeError, lambda: adt._length)
