import re
from abc import ABCMeta
import sys 
import types
import functools
import random

class ProtectAttributesMeta(ABCMeta):
    PREFIX = "Protected" # + hex(id(1))  # Add hex(id(1)) to assignments so students can't deterministically access the remangled name
    PROTECTED_RE = re.compile(r"^_[0-9A-Za-z]")
    
    def hide_caller():
        """ This method hides the key for the lookup inside a local variable of a function, to prevent forging the key """

        caller = [None]

        def method_wrapper(func:types.FunctionType, is_class_method = False, static_class = None):
            """Wraps methods to set the caller to allow access to private/protected attributes of the class."""
            @functools.wraps(func)
            def wrapped(*args, **kwargs):
                old_caller = caller[0]
                caller[0] = ((args[0].__base_class if is_class_method else static_class.__base_class if static_class is not None else args[0].__class__.__base_class))
                print(caller[0].__get__)
                try:
                    res = func(*args, **kwargs)
                except Exception:
                    caller[0] = old_caller
                    raise
                caller[0] = old_caller
                return res
            return wrapped
        class StaticMethod:
            def __init__(self, func):
                self.func = func
                self.memo = None
            def __get__(self, instance, owner):
                self.func = method_wrapper(self.func, False, owner)
                def new_get(self, instance, owner):
                    return self.func
                self.__get__ = new_get
                return self.func
            
        def __new__(cls, name, bases, namespace, **kwargs):
            """ 
            On the construction of the class find all the protected (and private) attributes and methods on the class
            and replace the attributes with relevant properties, and overwrite the methods.
            The attributes are overwritten at the protected location, so need to be stored at another location
            """
            # Can't check for ProtectAttributes in issubclass, when it hasn't been created yet.
            if name != 'ProtectAttributes': 
                def find_abstract_base_name():
                    for cls_ in bases:
                        if issubclass(cls_, ProtectAttributes):
                            break
                    else:
                        return None # This shouldn't happen
                    if cls_ is ProtectAttributes: # We are creating the abstract base class
                        return name 
                    else: # We are creating a class that inherited from the abstract base class
                        base_class = _get_base_class(cls_.mro())
                        return base_class.__name__
                
            
                base_name = find_abstract_base_name()
                mangled_base = f"_{ProtectAttributesMeta.PREFIX}{base_name}_"

                # Once we know the base case to mangle everything to, need to mangle all the class attributes and methods
                # Delete all the old names and replace them with mangled ones, before the class gets created
                new_namespace = {}
                for attr, value in namespace.items():
                    if isinstance(value, (types.FunctionType)):
                        value = method_wrapper(value)
                    elif isinstance(value, classmethod):
                        value = classmethod(method_wrapper(value.__func__, True))
                    elif isinstance(value, staticmethod):
                        value = StaticMethod(value.__func__)
                            
                    if not re.match(r"^_[0-9A-Za-z]", attr) or attr == '_abc_impl': 
                        new_namespace[attr] = value
                    else:

                        new_namespace[mangled_base + attr] = value
                    
            else:
                # This is the __getattr__ and __setattr__ for the ProtectAttributes class
                # Defining them here so they have access to the local caller variable
                # This saves wrapping the methods in a function that passes caller
                # which had a considerable performance boost.
                def __getattr__(self, name:str):
                    if ProtectAttributesMeta.PROTECTED_RE.match(name):
                        # Check that we are in a Protected class
                        caller_class = caller[0]
                        if caller_class is None: 
                            return self.invalid_access(name)
                        # Find the base class of protection 
                        cls = caller_class
                        

                        # Check the mangled name based on abstract base class.
                        mangled_name = f"_{ProtectAttributesMeta.PREFIX}{cls.__name__}_{name}"
                        return object.__getattribute__(self, mangled_name)
                    else: 
                        return object.__getattribute__(self, name)
                    

                def __setattr__(self, name:str, value):
                    if ProtectAttributesMeta.PROTECTED_RE.match(name):
                        #check for an abstract class in the mro
                        caller_class = caller[0]
                        if caller_class is None:
                            return self.invalid_access(name)

                        cls = caller_class
                        if cls is None:
                            return self.invalid_access(name)
                        
                        # Check the mangled name based on abstract base class.
                        mangled_name = f"_{ProtectAttributesMeta.PREFIX}{cls.__name__}_{name}"
                        return object.__setattr__(self, mangled_name, value)
                    else:
                        return object.__setattr__(self, name, value)

                new_namespace = namespace
                new_namespace['__getattr__'] = __getattr__
                new_namespace['__setattr__'] = __setattr__
            
            # Class gets initialised with the mangled names for the attributes and methods
            klass = super().__new__(cls, name, bases, new_namespace, **kwargs)
            if name != 'ProtectAttributes' and ProtectAttributes in bases:
                def get_class(self):
                    return klass
                klass.__base_class = property(get_class)

            return klass
        return __new__
    __new__ = hide_caller()


    
class ProtectAttributes(metaclass=ProtectAttributesMeta):
    def invalid_access(self, name):
        """
        If you are reading this due to an AttributeError, you have tried to access an internal attribute 
        or call an internal method of a data class which is prohibited and prone to errors.
        Use another approach that does not rely on the attribute / method you were trying to use.
        There will be another approach.
        """
        # Obscure the traceback, this makes the bottom line be the 
        # File "/directory/script.py", line 55, in function
        #   illegal_access = foo._bar
        #                    ^^^^^^^
        # Instead of the raise AttributeError in this file, 
        # which should reduce the number of students that look at this file,
        # and thus the number of internal accesses

        frame = sys._getframe(2) #invalid access, ProtectAttributes.getattr
        tb = types.TracebackType(None, frame, frame.f_lasti, frame.f_lineno)

        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'").with_traceback(tb)

def _get_base_class(mro):
    # Traverse up the mro to find the earliest class that directly inherited Protected Attributes
    for cls in mro:
        if ProtectAttributes in cls.__bases__:
            return cls