from unittest import TestCase
from data_structures.hash_table_linear_probing import LinearProbeTable
from data_structures.hash_table_quadratic_probing import QuadraticProbeTable
from data_structures.hash_table_double_hashing import DoubleHashingTable
from data_structures.dunder_protected import protected_names, ProtectAttributes

class ProtectedParent(protected_names("_protected_call", "_a")):
    def __init__(self):
        self._a = 1
        self.calls = 0
        # protect_attributes(self)
        
    def _protected_call(self):
        self.calls += 1
    def public_call(self):
        self._protected_call()

class ProtectedChild(ProtectedParent):
    def _protected_call(self):
        self.calls += 2
    def get_a(self):
        return self._a

class TestProtected(TestCase):
    def test_private(self):
        parent = ProtectedParent()
        child = ProtectedChild()
        #Check accessing protected attributes raises attribute error
        # print(parent._a)
        self.assertRaises(AttributeError, lambda: parent._a)
        self.assertRaises(AttributeError, lambda: child._a)

        #Check that child can access protected attribute
        self.assertEqual(1, child.get_a())

        def set_a(obj):
            obj._a = 2
        
        #Check that protected attributes cannot be set
        self.assertRaises(AttributeError, set_a, parent)
        self.assertRaises(AttributeError, set_a, child)

        parent.public_call()
        child.public_call()

        #Check that children can overwrite protected methods
        self.assertEqual(parent.calls, 1)
        self.assertEqual(child.calls, 2)

        #Check that protected calls cannot be called
        self.assertRaises(AttributeError, parent._protected_call)
        self.assertRaises(AttributeError, child._protected_call)


    # def setUp(self):
       
    #     self.probe_tables = [
    #         LinearProbeTable(),
    #         DoubleHashingTable(),
    #         QuadraticProbeTable(),
    #     ]

    # def test_private(self):
    #     for table in self.probe_tables:
    #         # Check that private attributes cannot be accessed outside of the mro
    #         # print(table.__array)
    #         self.assertRaises(AttributeError, lambda: table._array)
    #         # Check that a protected attribute cannot be set outside of the mro
    #         def f():
    #             table._array = 1
    #         self.assertRaises(AttributeError, f)
            
    #         table["key"] = 'value'
    #         self.assertEqual(len(table), 1)
