import re
from abc import ABCMeta
import sys 
import types
# from functools import wraps



class ProtectAttributesMeta(ABCMeta):
    PREFIX = "Protected" # + hex(id(1))
    
    def __new__(cls, name, bases, namespace, **kwargs):
        """ 
        On the construction of the class find all the protected (and private) attributes and methods on the class
        and replace the attributes with relevant properties, and overwrite the methods.
        The attributes are overwritten at the protected location, so need to be stored at another location
        """

        #check for an abstract class in the mro
        
        if name != 'ProtectAttributes':      
            def find_abstract_base_name():
                for cls_ in bases:
                    if issubclass(cls_, ProtectAttributes):
                        break
                else:
                    return None # This shouldn't happen
                if cls_ is ProtectAttributes: # We are creating the abstract base class
                    return name 
                else:
                    mro = cls_.mro()
                    
                    for i in range(len(mro)):
                        if mro[i] is ProtectAttributes:
                            for j in range(i-1, -1, -1):
                                if issubclass(mro[j] , ProtectAttributes):
                                    return mro[j].__name__
        
            base_name = find_abstract_base_name()
            
            mangled_base = f"_{ProtectAttributesMeta.PREFIX}{base_name}_"
            for attr, value in list(namespace.items()):
                if not re.match(r"^_[0-9A-Za-z]", attr) or attr == '_abc_impl': continue
                
                namespace[mangled_base + attr] = value
                del namespace[attr]
        
        klass = super().__new__(cls, name, bases, namespace, **kwargs)

        return klass

    
class ProtectAttributes(metaclass=ProtectAttributesMeta):
    __protected_properties__ = False

    def __get_caller(self):
        frame = sys._getframe(2)
        callername = frame.f_code.co_qualname.split(".", 1)[0]
        caller = frame.f_globals[callername]
        return caller
    
    def __get_base_class(self, mro):
        for i in range(len(mro)):
            if mro[i] is ProtectAttributes:
                for j in range(i-1, -1, -1):
                    if issubclass(mro[j] , ProtectAttributes):
                        return mro[j]

    def __invalid_access(self, name):
        """
        If you are reading this due to an AttributeError, you have tried to access an internal attribute 
        or call an internal method of a data class which is prohibited and prone to errors.
        Use another approach that does not rely on the attribute / method you were trying to use.
        There will be another approach.
        """
        frame = sys._getframe(2)
        tb = types.TracebackType(None, frame, frame.f_lasti, frame.f_lineno)

        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'").with_traceback(tb)

    def __getattr__(self, name:str):
        if name.startswith("_") and not name.startswith("__"):
            # print(name)
            caller = self.__get_caller()
            
            #check for an abstract class in the mro
            if type(self) is ProtectAttributes or type(caller).__name__ == 'function': 
                return self.__invalid_access(name)
            
            mro = caller.mro()
            cls = self.__get_base_class(mro)
            if cls is None:
                return self.__invalid_access(name)
            

            # Check the mangled name based on abstract class.
            mangled = f"_{ProtectAttributesMeta.PREFIX}{cls.__name__}_{name}"
            return object.__getattribute__(self, mangled)
        else: 
            return object.__getattribute__(self, name)
        #
        # caller = frame.f_globals[className]

        # return caller
    def __setattr__(self, name, value):
        if name.startswith("_") and not name.startswith("__"):
            frame = sys._getframe(1)

            # print(frame.f_locals.keys())
            callername = frame.f_code.co_qualname.split(".", 1)[0]
            caller = frame.f_globals[callername]
            #check for an abstract class in the mro
            if type(self) is ProtectAttributes: 
                return self.__invalid_access(name)

            cls = self.__get_base_class(caller.mro())
            if cls is None:
                return self.__invalid_access(name)
            # Check the mangled name based on abstract class.
            mangled = f"_{ProtectAttributesMeta.PREFIX}{cls.__name__}_{name}"
            return object.__setattr__(self, mangled, value)
        else:
            return object.__setattr__(self, name, value)
