import json
import re
import parser
import sys



class Renderable:
    def render():
        ...
        
class FormElement(Renderable):
    def __init__(self, type: str, name: str, label: str, formStateHandler: str, id: str=None, state_name: str=None, placeholder: str="", validation: bool=True, validation_message: str="", distinct_state: bool=False):
        self.indent = 0
        self.type = type
        self.name = name
        self.label = label
        self.id = id
        self.state_name = state_name
        self.validation = validation
        self.placeholder = placeholder
        self.distinct_state = distinct_state

            
        if self.distinct_state is True:
            name = "".join(list(map(lambda x: x.capitalize(), self.name.split())))
            temp = name
            self.formStateHandler = f'handle{temp}Change'
        else:
            self.formStateHandler = formStateHandler
        if self.id is None:
            self.id = self.name
        
        if self.state_name is None:
            self.state_name = "_".join(list(map(lambda x: x.lower(), self.name.split())))
        else:
            self.state_name = "_".join(list(map(lambda x: x.lower(), state_name.split())))
        
        if self.type not in ["submit", "button"]:
            
            htmlLabel = f'\t<label for="{self.name}">{self.label}</label>'
            if self.type in [ "text", "search", "url", "tel", "email"]:
                
                htmlInput = f'\t<input type="{self.type}" name="{self.name}" id="{self.id}" placeholder="{self.placeholder}" value=' + "{$formState." + self.state_name + "} onChange={" + self.formStateHandler + "} />"
            else:
                htmlInput = f'\t<input type="{self.type}" name="{self.name}" id="{self.id}" value=' + "{$formState." + self.state_name + "} onChange={" + self.formStateHandler + "} />"

            self.htmlLines = [ htmlLabel, htmlInput ]
        
        if self.validation is True:
            self.htmlLines.insert(0, '<div className="input-group">')
            self.htmlLines.append(r'{ !$formValidState.' + self.state_name + ' ? (<p className="error">' + validation_message + '</p>): (<p></p>)}')
            self.htmlLines.append('</div>')
        
    
    def increase_indent(self):
        self.indent += 1
        
    def __str__(self):
        return "\n".join(self.htmlLines)
    
    def render(self):
        indent_tabs = '\t' * self.indent
        lines = list(map(lambda el: f'{indent_tabs}{el}\n', self.htmlLines))
        htmlRendered = "".join(lines)
        return htmlRendered
            
    
class ContainerElement(Renderable):
    def __init__(self):
        self.indent = 0
        
    def increase_indent(self):
        self.indent += 1
    
    def add_indent(self, element: Renderable):
        lines = element.render().splitlines()
        indent_tabs = '\t' * self.indent
        indented_lines = list(map(lambda line: f'{indent_tabs}{line}\n', lines))
        return "".join(indented_lines)  
        
    
class Row(ContainerElement):
    def __init__(self):
        super().__init__()
        self.element_list = []
        
        
    def add_element(self, element: FormElement):
        element.increase_indent()
        self.element_list.append(element)
             
        
    def render(self):
        indent_tabs = '\t' * self.indent
        htmlRendered = f'{indent_tabs}<div className="form-row">\n'
        lines = []
        for element in self.element_list:
            
            # print(r_element)
            lines.append(self.add_indent(element))
        
        htmlRendered += "".join(lines)
            
        
        
        htmlRendered += f'{indent_tabs}</div>\n'
        return htmlRendered
            
        
        
        
class Section(ContainerElement):
    def __init__(self):
        super().__init__()
        self.row_list = []
    
 
    def add_row(self, row: Row):
        row.increase_indent()
        self.row_list.append(row)
        
    
    def render(self):
        indent_tabs = '\t' * self.indent
        htmlRendered = f'{indent_tabs}<div className="form-container">\n'
        lines = []
        for row in self.row_list:
            # print(r_element)
            lines.append(self.add_indent(row))
        
        htmlRendered += "".join(lines)
            
        
        
        htmlRendered += f'{indent_tabs}</div>\n'
        return htmlRendered
    
class Component(ContainerElement):
    def __init__(self):
        super().__init__()
        self.jsx = []
        
        self.component = r'''
        import React, { useState } from 'react';


        function Component(props)
        {
            const [$formState, $setFormState] = useState($defaultState);
            const [$formValidState, $setFormValidState] = useState($defaultValidityState);
            
            const $formStateHandler = (stateName) => (e) => {
                const value = e.target.type === "checkbox" ? e.target.checked : e.target.value;
                $setFormState({
                    ...$formState,
                    [stateName]: value
                });
            };
            
            
            return (
              $jsx  
            );
            
            
            
        }
        '''
    def add_section(self, section: Section):
        self.jsx.append(section)
    
    def add_state(self, defaultState: dict, formState: str='formState', setFormState: str='setFormState', formValidState: str='formValidState', setFormValidState: str='setFormValidState', formStateHandler: str='formStateHandler'):
        self.defaultState = defaultState
        self.formState = formState
        self.setFormState = setFormState
        self.formValidState = formValidState
        self.setFormValidState = setFormValidState
        self.formStateHandler = formStateHandler
        self.defaultValidityState = {key: True for key, _ in self.defaultState.items()}
        
    def render(self):
        jsx = "\n".join(list(map(lambda x: x.render(), self.jsx)))
        
        # print(self.component)
        self.component = re.sub(r'\$jsx', jsx, self.component)
        print(self.component)
        self.component = re.sub(r'\$defaultState', json.dumps(self.defaultState), self.component)
        self.component = re.sub(r'\$defaultValidityState', json.dumps(self.defaultValidityState), self.component)
        self.component = re.sub(r'\$formState', self.formState, self.component)
        self.component = re.sub(r'\$setFormState', self.setFormState, self.component)
        self.component = re.sub(r'\$formValidState', self.formValidState, self.component)
        self.component = re.sub(r'\$setFormValidState', self.setFormValidState, self.component)
        self.component = re.sub(r'\$formStateHandler', self.formStateHandler, self.component)                
        return self.component
        
        
        

def convert_to_component(config: dict):
    
    component = Component()
    formState = {}
    for section in config['sections']:
        _section = Section()
        for row in section['rows']:
            _row = Row()
            for element in row:
                props = element['properties']
                ds = False
                if props.get('distinct_state') is not None and props['distinct_state']['value'] == 'true':
                    ds = True
                
                vmessage = ""
                if props.get('validation_message') is not None and props['validation_message']['value'] is not None:
                    vmessage = props['validation_message']['value']
                
                _validation = True
                if props.get('validation') is not None and props['validation']['value'] == 'false':
                    _validation = False
                
                _element = FormElement(type=props['type']['value'], name=element['id'], label=props['label']['value'], formStateHandler='formStateHandler', distinct_state=ds, validation_message=vmessage, validation=_validation)
                if props['type']['value'] in ['text', 'date', "url", "tel", "email"]:
                    formState[_element.state_name] = ""
                elif props['type']['value'] == 'checkbox':
                    formState[_element.state_name] = False
                _row.add_element(_element)
            
            _section.add_row(_row)
        component.add_section(_section)
    # print(formState)
    component.add_state(formState)
    return component.render()

def create_form(filename: str, target_file_name: str):
    source_script = ''
    component_string = ''
    with open(filename, "r") as f:
        source_script = f.read()
        parser.set_source_string(source_script)
        config = parser._program()
        component_string = convert_to_component(config)
    
    with open(target_file_name, "w") as f:
        f.write(component_string)
    
    
    
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Incorrect number of arguments")
    
    create_form(sys.argv[1], sys.argv[2])
    
        
        