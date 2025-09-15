import re
# import inspect

# class DunderProtected:
#     """
#     Allow subclass code to override/access base-class __dunder attributes/methods
#     by remapping _Owner__name across the MRO to the most-derived definition.
#     """
#     _DU_PTN = re.compile(r"^_([A-Za-z_]\w*)__([A-Za-z_]\w*)$")
#     ENABLED = True

#     def __getattribute__(self, name:str):
#         if (m:= DunderProtected._DU_PTN.match(name)):
#             caller = inspect.currentframe().f_back.f_locals.get('self', None)
#             # print(type(caller), inspect.currentframe())
#             if not isinstance(caller, object.__getattribute__(self, '__class__')) and not issubclass(type(caller), object.__getattribute__(self, '__class__')):
#                 return object.__getattribute__(self, name)

#                 # raise AttributeError(f"type object '{object.__getattribute__(self, '__class__').__name__}' has no attribute '{name}'")
#             attr = m.group(2)
#             for cls in type(self).mro():
#                 try:
#                     return object.__getattribute__(self, f"_{cls.__name__}__{attr}")
#                 except AttributeError:
#                     pass

#         # Normal lookup (also handles non-mangled names)
#         return object.__getattribute__(self, name)

#     def __setattr__(self, name, value):
        
#         if DunderProtected.ENABLED and (m := DunderProtected._DU_PTN.match(name)) and m.group(1) in (cls.__name__ for cls in type(self).mro()):
#             attr = m.group(2)
#             # print('setting', name)
#             # Prefer writing into the first existing slot across MRO
#             objdict = object.__getattribute__(self, "__dict__")
#             for cls in type(self).mro():
#                 mangled = f"_{cls.__name__}__{attr}"
#                 if mangled in objdict:
#                     objdict[mangled] = value
#                     return
#             # Otherwise default behavior (creates attribute under provided name)
#         object.__setattr__(self, name, value)


import inspect
from functools import wraps

def _protected_property(name):
    private_name = f'_DunderProtected_{name}'

    def getter(self):
        caller = inspect.currentframe().f_back.f_locals.get('self', None)
        if not isinstance(caller, self.__class__) and not isinstance(self, type(caller)):
            raise AttributeError(f"AttributeError '{type(self).__name__}' object has no attribute '{name}'")
        return getattr(self, private_name)

    def setter(self, value):
        caller = inspect.currentframe().f_back.f_locals.get('self', None)
        if not isinstance(caller, self.__class__) and not isinstance(self, type(caller)):
            raise AttributeError(f"AttributeError '{type(self).__name__}' object has protected attribute '{name}'")
        setattr(self, private_name, value)

    def deleter(self):
        caller = inspect.currentframe().f_back.f_locals.get('self', None)
        if not isinstance(caller, self.__class__) and not isinstance(self, type(caller)):
            raise AttributeError(f"AttributeError '{type(self).__name__}' object has no attribute '{name}'")
        delattr(self, private_name)

    prop =  property(getter, setter, deleter)
    return prop

def _protected_method(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        caller = inspect.currentframe().f_back.f_locals.get('self', None)
        if not isinstance(caller, self.__class__) and not isinstance(self, type(caller)):
            raise AttributeError(f"Protected method '{method.__name__}' cannot be called from outside the class or its subclasses.")
        return method(self, *args, **kwargs)
    return wrapper

# def protected_attributes(*attr_names:str):
#     def decorator(cls):
#         for name in attr_names:
#             if not name.startswith("_"): raise ValueError("Improper protected attribute: " + name)
#             setattr(cls, name, _protected_property(name))
#         return cls
#     return decorator



def protected_names(*protected):
    """Returns a class that protects all attributes given as strings"""
    class Protect():
        def __new__(cls, *args, **kwargs):
            klass = super().__new__(cls)
            for attr in protected:
                try:
                    method = getattr(cls, attr)
                    if callable(method):
                        setattr(cls, attr, _protected_method(method))
                    else:
                        setattr(cls, attr, _protected_property(attr))
                except AttributeError:
                    setattr(cls, attr, _protected_property(attr))
            return klass

    return Protect

def protect_attributes(obj):
    for attr, val in list(obj.__dict__.items()):
        if re.match(r"^_[0-9A-Za-z]", attr):
            setattr(obj, attr, _protected_property(attr))
            
class ProtectAttributesMeta(type):
    def __call__(self, *args, **kwds):
        obj = super().__call__(*args, **kwds)
        protect_attributes(obj)
        return obj
    
class ProtectAttributes(metaclass = ProtectAttributesMeta):
    pass
        
