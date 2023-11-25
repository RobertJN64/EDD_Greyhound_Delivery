def recursive_expose(obj):
    func_dict = {}
    var_dict = {}
    subobj_dict = {}

    for search_order in ['func', 'var', 'obj']:
        for item in [x for x in dir(obj) if x[0] != '_']:
            inst = getattr(obj, item)

            if hasattr(inst, '__call__'):
                if search_order == 'func':
                    func_dict[item] = (inst, inst.__code__.co_varnames)
            elif isinstance(inst, int) or isinstance(inst, float) or isinstance(inst, str) or isinstance(inst, bool):
                if search_order == 'var':
                    var_dict[item] = inst
            else:
                if search_order == 'obj':
                    subobj_dict[item] = recursive_expose(inst)

    return {"functions": func_dict, "vars": var_dict, "subobjects": subobj_dict}