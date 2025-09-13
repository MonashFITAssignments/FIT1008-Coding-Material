from unittest import TestCase
from data_structures.hash_table_linear_probing import LinearProbeTable
from data_structures.hash_table_quadratic_probing import QuadraticProbeTable
from data_structures.hash_table_double_hashing import DoubleHashingTable

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
            probing_func_name = f"_{type(table).__name__}__handle_probing"
            old_func = getattr(table, probing_func_name)
            def new_probing_func(*args, **kwargs):
                nonlocal calls
                calls += 1
                return old_func(*args, **kwargs)
            
            setattr(table, probing_func_name, new_probing_func)

            table["key"] = 'value'
            self.assertEqual(len(table), 1)

            self.assertEqual(calls, 1)


        
        

        
    