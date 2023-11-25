from typing import Self

class ObjectMap:
    def __init__(self, obj):
        self.func_dict: dict[str, tuple] = {} #tuple of function(), args
        self.var_dict: dict[str, tuple] = {} #tuple of baseobject, varname
        self.subobj_dict: dict[str, Self] = {} #ObjectMap of subobject

        for name in [x for x in dir(obj) if x[0] != '_']:
            inst = getattr(obj, name)
            if hasattr(inst, '__call__'):
                self.func_dict[name] = (inst, inst.__code__.co_varnames)
            elif isinstance(inst, (int, float, str, bool)):
                self.var_dict[name] = (obj, name)
            else:
                # noinspection PyTypeChecker
                self.subobj_dict[name] = self.__class__(inst) #this allows superclassing

    def call_function(self, func_trace, kwargs):
        obj_name = func_trace[0]
        func_trace = func_trace[1:]
        if len(func_trace) == 0:
            self.func_dict[obj_name][0](**kwargs)
        else:
            self.subobj_dict[obj_name].call_function(func_trace, kwargs)

    def __repr__(self):
        return (f"Object with:"
                f"\nfunctions:\n{self.func_dict}" +
                f"\nvars:\n{self.var_dict}"
                f"\nsubobjects: {list(self.subobj_dict.keys())}")


