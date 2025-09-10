import re

class DunderProtected:
    """
    Allow subclass code to override/access base-class __dunder attributes/methods
    by remapping _Owner__name across the MRO to the most-derived definition.
    """
    _DU_PTN = re.compile(r"^_([A-Za-z_]\w*)__([A-Za-z_]\w*)$")

    def __getattribute__(self, name):
        m = DunderProtected._DU_PTN.match(name)
        if m:
            # e.g. name == "_Base__do" -> attr="do"
            attr = m.group(2)
            cls_self = type(self)

            # 1) Data descriptors on classes (most-derived first)
            for cls in cls_self.mro():
                mangled = f"_{cls.__name__}__{attr}"
                clsdict = object.__getattribute__(cls, "__dict__")
                val = clsdict.get(mangled)
                if val is not None and (hasattr(val, "__set__") or hasattr(val, "__delete__")):
                    # data descriptor
                    return val.__get__(self, cls_self)

            # 2) Instance dict (most-derived owner slot first)
            objdict = object.__getattribute__(self, "__dict__")
            for cls in cls_self.mro():
                mangled = f"_{cls.__name__}__{attr}"
                if mangled in objdict:
                    return objdict[mangled]

            # 3) Non-data descriptors / class attrs (most-derived first)
            for cls in cls_self.mro():
                mangled = f"_{cls.__name__}__{attr}"
                clsdict = object.__getattribute__(cls, "__dict__")
                val = clsdict.get(mangled)
                if val is not None:
                    # bind if descriptor
                    return val.__get__(self, cls_self) if hasattr(val, "__get__") else val

            # If nothing matched, fall through to normal lookup to raise AttrError

        # Normal lookup (also handles non-mangled names)
        return super().__getattribute__(name)

    def __setattr__(self, name, value):
        m = DunderProtected._DU_PTN.match(name)
        if m:
            attr = m.group(2)
            # Prefer writing into the first existing slot across MRO
            objdict = object.__getattribute__(self, "__dict__")
            for cls in type(self).mro():
                mangled = f"_{cls.__name__}__{attr}"
                if mangled in objdict:
                    objdict[mangled] = value
                    return
            # Otherwise default behavior (creates attribute under provided name)
        super().__setattr__(name, value)
