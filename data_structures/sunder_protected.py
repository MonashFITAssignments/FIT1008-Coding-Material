import re
from abc import ABCMeta
import sys 
from functools import wraps



class ProtectAttributesMeta(ABCMeta):
    
    PROTECTION_PREFIX = "Protected" #+ hex(id(1))

    def __new__(cls, name, bases, namespace, **kwargs):
        """ 
        On the construction of the class find all the protected (and private) attributes and methods on the class
        and replace the attributes with relevant properties, and overwrite the methods.
        The attributes are overwritten at the protected location, so need to be stored at another location
        """
        properties = []
        for attr, value in namespace.items():
            if not re.match(r"^_[0-9A-Za-z]", attr) or attr == '_abc_impl': continue
            
            if callable(value):
                namespace[attr] = ProtectAttributesMeta.__protected_method(value)
            else:
                namespace[attr] = ProtectAttributesMeta.__protected_property(attr)
                private_name = f'_{ProtectAttributesMeta.PROTECTION_PREFIX}_{attr}'
                properties.append((private_name, value))
        
        klass = super().__new__(cls, name, bases, namespace, **kwargs)

        for prop in properties:
            setattr(klass, *prop)
        return klass


    def __call__(cls, *args, **kwds):
        """ 
        Meta class that redefines the Class() method
        After the first construction of a class, it finds all protected (and private) attributes set during __init__
        and adds those protected properties on the **Class**, then regenerates the object with protected propeties.
        Once the class has the protected properties, it doesn't need to be reprotected on each call.
        """
        obj = super().__call__(*args, **kwds)
        
        if not cls.__protected_properties__:
            for attr in obj.__dict__:
                #Check for a protected attribute, starts with _ and not __
                if re.match(r"^_[0-9A-Za-z]", attr):
                    setattr(type(obj), attr, ProtectAttributesMeta.__protected_property(attr)) #Setting this on the object type (class), means that it has the correct property function for all init calls after the first
            cls.__protected_properties__ = True
            obj = super().__call__(*args, **kwds)
        return obj
    
    @staticmethod
    def __protected_property(name):
        private_name = f'_{ProtectAttributesMeta.PROTECTION_PREFIX}_{name}'
        def get_caller():
            frame = sys._getframe(2)
            className = frame.f_code.co_qualname.split(".", 1)[0]
            caller = frame.f_globals[className]
            return caller
        def getter(self):
            caller = get_caller()
            if not isinstance(self, caller):
                # You are doing something dumb, please use a different approach that does not rely on this attribute
                # If you still get around the protection, we will change ProtectAttributesMeta.PROTECTION_PREFIX in marking, 
                # and your code will break
                raise AttributeError(f"cannot access protected attribute '{name}' on object '{type(self).__name__}'")
            
            return getattr(self, private_name)

        def setter(self, value):
            caller = get_caller()
            if not isinstance(self, caller) and not (caller is ProtectAttributesMeta or type(caller) is ProtectAttributesMeta):
                raise AttributeError(f"cannot set protected attribute '{name}' on object '{type(self).__name__}'")
            setattr(self, private_name, value)

        def deleter(self):
            caller = get_caller()
            if not isinstance(self, caller):
                raise AttributeError(f"cannot delete protected attribute '{name}' on object '{type(self).__name__}'")
            delattr(self, private_name)

        prop =  property(getter, setter, deleter)
        return prop
    
    @staticmethod
    def __protected_method(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            frame = sys._getframe(1)
            caller = frame.f_globals[frame.f_code.co_qualname.split(".", 1)[0]]
            if not caller is ProtectAttributesMeta.__protected_method and not isinstance(self, caller):
                raise AttributeError(f"cannot call protected method '{method.__name__}'")
            return method(self, *args, **kwargs)
        return wrapper

    
class ProtectAttributes(metaclass = ProtectAttributesMeta):
    __protected_properties__ = False
