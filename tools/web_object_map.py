from tools.object_map import ObjectMap
import flask

## LIMITATION - ASSUMES ALL PARAMS ARE INTS

class WebObjectMap(ObjectMap):
    def generate_html(self, font_size=2.5):
        buttons = ""
        for funcname, (f, params) in self.func_dict.items():
            stack = self.name + "." + funcname
            onclick = f'quick_action("{stack}")'
            buttons += f"<button class='nice_button' onclick={onclick}>{funcname}</button>"
            for paramname in params:
                className = 'py_' + stack
                elemID = className + '|' + paramname
                buttons += f"<span class='input_label'>{paramname}</span>"
                buttons += f"<input id='{elemID}' class='{className}' type='number' value='0'>"
            buttons += "<br>"

        var_table = ""
        if len(self.var_list) > 0:
            var_table += "<br><table><thead><tr><th>Variable</th><th>Value</th></thead><body>"
            for varname in self.var_list:
                elemID = 'py_' + self.name + "." + varname
                var_table += f"<tr><td>{varname}</td><td id='{elemID}'>Waiting for update...</td>"
            var_table += "</body></table>"

        subcontent = ""
        for subname, om in self.subobj_dict.items():
            subcontent += om.generate_html(font_size - 0.5) + '\n'

        return (f"""
        <details open>
            <summary style="font-size: {font_size}em">{self.name}</summary>
            {buttons}
            {var_table}
            {subcontent}
        </details>
        """)

    def get_status(self):
        retval = {}
        for var_name in self.var_list:
            retval[self.name + '.' + var_name] = str(getattr(self.obj, var_name))
        for obj in self.subobj_dict.values():
            retval.update(obj.get_status())
        return retval

def create_WebObjectMap_server(flask_app, name, obj, include_private=False):
    wom = WebObjectMap(name, obj, include_private)

    py_control_content = wom.generate_html()

    @flask_app.route('/py_control')
    def py_control():
        return flask.render_template('py_control.html', content=py_control_content)

    @flask_app.route('/py_control/quick_action/<action>')
    def quick_action(action):
        kwargs = {argname: int(arg) for argname, arg in flask.request.args.items()}
        wom.call_function(action, kwargs)
        return "OK"

    @flask_app.route('/py_control/get_status')
    def get_status():
        return wom.get_status()

