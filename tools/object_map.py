from typing import Self

class ObjectMap:
    def __init__(self, name, obj):
        self.name = name
        self.obj = obj
        self.func_dict: dict[str, tuple] = {} #tuple of function(), args
        self.var_list = [] #list of varnames
        self.subobj_dict: dict[str, Self] = {} #ObjectMap of subobject

        for attr in [x for x in dir(obj) if x[0] != '_']:
            inst = getattr(obj, attr)
            if hasattr(inst, '__call__'):
                self.func_dict[attr] = (inst, inst.__code__.co_varnames[1:]) #ignore self param
            elif isinstance(inst, (int, float, str, bool)):
                self.var_list.append(attr)
            else:
                # noinspection PyTypeChecker
                self.subobj_dict[attr] = self.__class__(self.name + '.' + attr, inst) #this allows superclassing

    def call_function(self, func_trace: str, kwargs):
        func_name = func_trace.removeprefix(self.name + '.')
        if '.' in func_name:
            obj_name = func_name.split('.')[0]
            self.subobj_dict[obj_name].call_function(func_trace, kwargs)
        else:
            self.func_dict[func_name][0](**kwargs)

    def __repr__(self):
        return (f"{self.name} with:"
                f"\nfunctions:\n{self.func_dict}" +
                f"\nvars:\n{self.var_list}"
                f"\nsubobjects: {list(self.subobj_dict.keys())}")


