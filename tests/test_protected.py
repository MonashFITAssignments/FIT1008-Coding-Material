from unittest import TestCase
from data_structures.hash_table_linear_probing import LinearProbeTable
from data_structures.hash_table_quadratic_probing import QuadraticProbeTable
from data_structures.hash_table_double_hashing import DoubleHashingTable
from data_structures.dunder_protected import DunderProtected

class Parent(DunderProtected, private="a,b"):
    def __init__(self):
        self.__a = 1
        self.__b = 10
    def get_a(self):
        return self.__a
    def get_b(self):
        return self.__b
    def set_a(self, a):
        self.__a = a
    def set_b(self, b):
        self.__b = b
    def __a_method(self, a):
        return a
    def __b_method(self, b):
        return (b, b)
    def call_a(self, a):
        return self.__a_method(a)
    def call_b(self, b):
        return self.__b_method(b)

class ChildOverwrite(Parent, private="a,b"):
    def __init__(self):
        super().__init__()
        self.__b = 100
    def get_b(self):
        return self.__b
    def __b_method(self, b):
        return (b, b, b)
    def call_b(self, b):
        return self.__b_method(b)
    def set_b(self, b):
        self.__b = b

class Child2(Parent, private="b"):
    def set_b(self, b):
        self.__b = b
    def __b_method(self, b):
        return (b, b, b)
    def get_a(self):
        return self.__a

class TestProtected(TestCase):
    def setUp(self):
       
        self.probe_tables = [
            LinearProbeTable(),
            DoubleHashingTable(),
            QuadraticProbeTable(),
        ]

    def test_private(self):
        for table in self.probe_tables:
            # Check that private attributes cannot be accessed outside of the mro
            self.assertRaises(AttributeError, lambda: table.__array)
            # Check that a private attribute can be set outside of the mro
            table.__array = 1
            # Check that a new private attribute set outside of the mro can still be retrieved
            self.assertEqual(table.__array, 1)

            # Check that the children are calling their version of private attributes if they exist
            calls = 0
            probing_func_name = f"_LinearProbeTable__handle_probing" #Because setitem is in LinearProbeTable it looks up _LinearProbeTable__handle_probing
            old_func = getattr(table, probing_func_name)
            def new_probing_func(*args, **kwargs):
                nonlocal calls
                calls += 1
                return old_func(*args, **kwargs)
            
            setattr(table, probing_func_name, new_probing_func)

            table["key"] = 'value'
            self.assertEqual(len(table), 1)

            self.assertEqual(calls, 1)


        
        
    def test_parent_get(self):
        p = Parent()
        self.assertEqual(p.get_a(), 1)
        self.assertEqual(p.get_b(), 10)
    def test_parent_set(self):
        p = Parent()
        p.set_a(2)
        p.set_b(20)
        self.assertEqual(p.get_a(), 2)
        self.assertEqual(p.get_b(), 20)
    def test_parent_call(self):
        p = Parent()
        self.assertEqual(p.call_a(1), 1)
        self.assertEqual(p.call_b(1), (1,1))
    
    def test_child_inherit_get(self):
        c = ChildOverwrite()
        self.assertEqual(c.get_a(), 1)
    def test_child_overwrite_get(self):
        c = ChildOverwrite()
        self.assertEqual(c.get_b(), 100)
    def test_child_inherit_set(self):
        c = ChildOverwrite()
        c.set_a(2)
        self.assertEqual(c.get_a(), 2)
    def test_child_overwrite_set(self):
        c = ChildOverwrite()
        c.set_b(20)
        self.assertEqual(c.get_b(), 20)
    def test_child_inherit_call(self):
        c = ChildOverwrite()
        self.assertEqual(c.call_a(10), 10)
    def test_child_overwrite_call(self):
        c = ChildOverwrite()
        self.assertEqual(c.call_b(20), (20, 20, 20))
    
    def test_parent_get_child_set(self):
        c = Child2()
        c.set_b(30)
        self.assertEqual(c.get_b(), 30)
    def test_parent_call_child_method(self):
        c = Child2()
        self.assertEqual(c.call_b(15), (15, 15, 15))

    def test_outside_access(self):
        for obj in [Parent(), ChildOverwrite()]:
            for attr in ['__a', '__b', '__a_method', '__b_method']:
                with self.assertRaises(AttributeError):
                    getattr(obj, attr)
        with self.assertRaises(AttributeError):
            Parent().__a
    def test_mangled_access(self):
        for attr in ['__a', '__b', '__a_method', '__b_method']:
            getattr(Parent(), '_Parent' + attr)
            getattr(ChildOverwrite(), '_Parent' + attr)
            getattr(ChildOverwrite(), '_ChildOverwrite' + attr)
    
    def test_incorrect_private_kwarg(self):
        with self.assertRaises(AttributeError):
            Child2().get_a() # This test may be removed if inheriting private attribtues is added to DunderProtected.