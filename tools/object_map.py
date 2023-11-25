class ObjectMap:
    def __init__(self, obj):
        self.func_dict: dict[str, tuple] = {} #tuple of function(), args
        self.var_dict: dict[str, tuple] = {} #tuple of baseobject, varname
        self.subobj_dict: dict[str, ObjectMap] = {} #ObjectMap of subobject

        for name in [x for x in dir(obj) if x[0] != '_']:
            inst = getattr(obj, name)
            if hasattr(inst, '__call__'):
                self.func_dict[name] = (inst, inst.__code__.co_varnames)
            elif isinstance(inst, (int, float, str, bool)):
                self.var_dict[name] = (obj, name)
            else:
                self.subobj_dict[name] = ObjectMap(inst)

    def get_status(self):
        update = {}
        for name, (baseobject, attrname) in self.var_dict.items():
            update[name] = getattr(baseobject, attrname)
        for name, obj in self.subobj_dict.items():
            for sub_name, ref in obj.get_status().items():
                update[name + '.' + sub_name] = ref
        return update


    def call_function(self, func_trace, kwargs):
        obj_name = func_trace[0]
        func_trace = func_trace[1:]
        if len(func_trace) == 0:
            self.func_dict[obj_name][0](**kwargs)
        else:
            self.subobj_dict[obj_name].call_function(func_trace, kwargs)

    def generate_html(self, name, font_size = 2.5):
        subcontent = ""
        for subname, om in self.subobj_dict.items():
            subcontent += om.generate_html(name + '.' + subname, font_size-0.25) + '\n'

        buttons = ""
        for funcname, params in self.func_dict.items():
            onclick = f'quick_action("{name + "." + funcname}")'
            buttons += f"<button class='nice_button' onclick={onclick}>{funcname}</button><br><br>"

        return (f"""
        <details open>
            <summary style="font-size: {font_size}em">{name}</summary>
            {buttons}
            {subcontent}
        </details>
        """)

    def __repr__(self):
        return (f"Object with:"
                f"\nfunctions:\n{self.func_dict}" +
                f"\nvars:\n{self.var_dict}"
                f"\nsubobjects: {list(self.subobj_dict.keys())}")


