from tools.object_map import ObjectMap
import flask

## LIMITATION - ASSUMES ALL PARAMS ARE INTS

class WebObjectMap(ObjectMap):
    def generate_html(self, name, font_size=2.5):
        subcontent = ""
        for subname, om in self.subobj_dict.items():
            subcontent += om.generate_html(name + '.' + subname, font_size - 0.25) + '\n'

        buttons = ""
        for funcname, (f, params) in self.func_dict.items():
            onclick = f'quick_action("{name + "." + funcname}")'
            buttons += f"<button class='nice_button' onclick={onclick}>{funcname}</button>"
            for paramname in params:
                className = 'py_' + name + '.' + funcname
                elemID = 'py_' + name + '.' + funcname + '|' + paramname
                buttons += f"<span class='input_label'>{paramname}</span>"
                buttons += f"<input id='{elemID}' class='{className}' type='number' value='0'>"
            buttons += "<br><br>"

        return (f"""
        <details open>
            <summary style="font-size: {font_size}em">{name}</summary>
            {buttons}
            {subcontent}
        </details>
        """)

    def get_status(self):
        update = {}
        for name, (baseobject, attrname) in self.var_dict.items():
            update[name] = getattr(baseobject, attrname)
        for name, obj in self.subobj_dict.items():
            for sub_name, ref in obj.get_status().items():
                update[name + '.' + sub_name] = ref
        return update

def create_WebObjectMap_server(flask_app, name, obj):
    wom = WebObjectMap(obj)

    py_control_content = wom.generate_html(name)

    @flask_app.route('/py_control')
    def py_control():
        return flask.render_template('py_control.html', content=py_control_content)

    @flask_app.route('/quick_action/<action>')
    def quick_action(action: str):
        kwargs = {argname: int(arg) for argname, arg in flask.request.args.items()}
        wom.call_function(action.removeprefix(name + '.').split('.'), kwargs)
        return "OK"


