import re

class DunderProtected:
    __classes = {}
    __private_keys = set()
    def __init_subclass__(cls, private = ""):
        """
        Adds aliases for private methods and private attributes so that all children
        can inherit them like normal attributes.

        Class attributes are not supported.
        
        :param private: 
            A comma separated string of all the private instance attributes of the class, passed as a keyword argument to the class definition.
            
            The attributes should **not** contain the leading '__'.
            Private methods are automatically detected, and should not be included.

            Children need to redefine all private attributes for now.

            >>> class ArrayList(DunderProtected, private='array,length'):
                    def __init__(self):
                        self.__array = ArrayR(1)
                        self.__length = 0
                    def __shuffle_left(self, index):
                        pass
                class ArrayList2(ArrayList, private='array,length'):
                    pass
            
        """
        super().__init_subclass__()
        DunderProtected.__classes[cls.__name__] = {}
        classes = [c for c in cls.mro() if c.__name__ in DunderProtected.__classes]
        attrs = [attr for attr in private.split(",") if attr != ""]
        
        # Add instance attributes as custom setters to a very mangled name
        # All of '_Parent__attr', '_Child__attr', '_GrandChild__attr' have setters and getters to f'_{hex(id(DunderProtected))}__attr'
        def g(attr):
            #The setters and getters need their own scope aparently
            key = f"_{hex(id(DunderProtected))}__{attr}"
            def getter(self):
                return getattr(self, key)
            return getter
        def s(attr):
            key = f"_{hex(id(DunderProtected))}__{attr}"
            def setter(self, value):
                setattr(self, key, value)
            return setter
        for attr, cls_base in [(attr, cls) for cls in classes for attr in attrs]:
            DunderProtected.__add_private(cls, f"_{cls_base.__name__}__{attr}", property(g(attr), s(attr)))
        
        #add private methods
        private_methods = set()
        for cls_base in classes:
            # Go through and overwrite the private method for each class in the MRO
            for key, value in list(cls_base.__dict__.items()):
                if key.startswith(f"_{cls_base.__name__}__") and callable(value):
                    unmangled = key[len(f"_{cls_base.__name__}"):]
                    # If this method has already been overwritten then don't overwrite it.
                    # This means that the parents won't overwrite the methods that children are trying to overwrite.
                    if unmangled in private_methods: continue
                    private_methods.add(unmangled)
                    for c in classes:
                        DunderProtected.__add_private(cls, f"_{c.__name__}{unmangled}", value)
    @staticmethod
    def __add_private(cls, key, value):
        setattr(cls, key, value)
        DunderProtected.__private_keys.add(key)  

    @staticmethod
    def find_private_access(code:str, exclude:set[str] = None):
        """
        Checks if the code contains any mangled attributes or functions.
        """
        if exclude is None:
            exclude = set()
        pattern = "|".join(DunderProtected.__private_keys - exclude)
        return re.finditer(pattern, code)
