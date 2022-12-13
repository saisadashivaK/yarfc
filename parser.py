# Terminals - DOUBLE_COLON, STYLE, LITERAL, SEMICOLON, ARROW, COLON, LIST_BEGIN, LIST_END, NAME, 
#            SECTION, DASH, COMMA, ROW_DELIMITER


from enum import Enum, auto

from copy import deepcopy

import json



class TokenType(Enum):
    DOUBLE_COLON = auto()
    STYLE = auto()
    LITERAL = auto()
    SEMICOLON = auto()
    ARROW = auto()
    COLON = auto()
    LIST_BEGIN = auto()
    LIST_END = auto()
    NAME = auto()
    SECTION = auto()
    DASH = auto()
    COMMA = auto()
    ROW_DELIMITER = auto()
    EMPTY = auto()
    ERROR = auto()

class Token:
    def __init__(self, token_type: TokenType, lexeme: str, line_no: int, col_no: int):
        self.token_type = token_type
        self.lexeme = lexeme
        self.line_no = line_no
        self.col_no = col_no
        
    def __str__(self):
        return f'{self.token_type}'
        

PEEK = 0                    # points to the current character to be seen by lexical analyzer
CURRENT_TOKEN = None        # points to the last read token
CURRENT_LINE_NUMBER = 1
CURRENT_COLUMN_NUMBER = 0
source_string: str = None        # the string holding the source script
SOURCE_STRING_LENGTH: int = 0
error_list: list = []
    
sync_map = {
    "program": [], 
    "style": [ TokenType.SECTION ], 
    "block": [  ], 
    "rowgroup": [ TokenType.SECTION ], 
    "element_list": [ TokenType.SECTION, TokenType.ROW_DELIMITER ], 
    "element": [ TokenType.SEMICOLON, TokenType.DASH ], 
    "key_value_pairs": [ TokenType.SEMICOLON, TokenType.DASH ], 
    "id": [ TokenType.ARROW, TokenType.DASH ], 
    "key": [ TokenType.COLON, TokenType.DASH ], 
    "value": [ TokenType.COMMA, TokenType.DASH ], 
    "option_list": [ TokenType.LIST_END, TokenType.DASH ]
    
}

    
    
    
def print_tokens(inputStr: str):
    global SOURCE_STRING_LENGTH, source_string
    source_string = inputStr
    SOURCE_STRING_LENGTH = len(source_string)
    while True:
        token = get_token()
        if token is None:
            break
        print(token, end=" ")
    
    print()
    
def lexer(test):
    pass

def get_token(lookahead=1, check=False, recovery=False):
    global PEEK, CURRENT_LINE_NUMBER, CURRENT_COLUMN_NUMBER
    
    line_no = deepcopy(CURRENT_LINE_NUMBER)
    column_no = deepcopy(CURRENT_COLUMN_NUMBER)
    PEEK_COPY = deepcopy(PEEK)
    lexeme = ""
    token = None
    for i in range(lookahead):
        while PEEK_COPY < SOURCE_STRING_LENGTH and source_string[PEEK_COPY].isspace():
            if source_string[PEEK_COPY] == '\n':
                line_no += 1
                column_no = 0
            elif source_string[PEEK_COPY] == " ":
                column_no += 1
                # print(f"sp {column_no} ", end="")
            PEEK_COPY += 1
        
        if PEEK_COPY >= SOURCE_STRING_LENGTH:
            token = Token(TokenType.EMPTY, "", line_no, column_no)
        elif source_string[PEEK_COPY].isalnum():
            while PEEK_COPY < SOURCE_STRING_LENGTH and (source_string[PEEK_COPY].isalnum() or source_string[PEEK_COPY] in ['_', '.']) and not source_string[PEEK_COPY].isspace():
                lexeme += source_string[PEEK_COPY]
                PEEK_COPY += 1
                
            
            if lexeme == "style":
                token = Token(TokenType.STYLE, lexeme, line_no, column_no)
            elif lexeme == "section":
                token = Token(TokenType.SECTION, lexeme, line_no, column_no)
            else:
                token = Token(TokenType.NAME, lexeme, line_no, column_no)
            
            
        elif source_string[PEEK_COPY] == ":":
            if (PEEK_COPY + 1) < SOURCE_STRING_LENGTH and source_string[PEEK_COPY + 1] == ":":
                PEEK_COPY += 2
                lexeme = "::"
                token = Token(TokenType.DOUBLE_COLON, lexeme, line_no, column_no)
            else:
                PEEK_COPY += 1
                lexeme = ":"
                token = Token(TokenType.COLON, lexeme, line_no, column_no)
        elif source_string[PEEK_COPY] == '"':
            PEEK_COPY += 1
            while PEEK_COPY < SOURCE_STRING_LENGTH and source_string[PEEK_COPY] != '"':
                lexeme += source_string[PEEK_COPY]
                PEEK_COPY += 1
                
            if source_string[PEEK_COPY] == '"':    
                PEEK_COPY += 1
                token = Token(TokenType.LITERAL, lexeme, line_no, column_no)
                column_no += 2
            else:
                if recovery is False:
                    error_list.append({"message": "Invalid literal", "loc": (line_no, column_no)})
                token = Token(TokenType.ERROR, lexeme, line_no, column_no)
            
        elif source_string[PEEK_COPY] == ';':
            lexeme = ';'
            PEEK_COPY += 1
            token = Token(TokenType.SEMICOLON, lexeme, line_no, column_no)
        elif source_string[PEEK_COPY] == '[':
            lexeme = '['
            PEEK_COPY += 1
            token = Token(TokenType.LIST_BEGIN, lexeme, line_no, column_no)
        elif source_string[PEEK_COPY] == ']':
            lexeme = ']'
            PEEK_COPY += 1
            token = Token(TokenType.LIST_END, lexeme, line_no, column_no)
        elif source_string[PEEK_COPY] == ',':
            lexeme = ','
            PEEK_COPY += 1
            token = Token(TokenType.COMMA, lexeme, line_no, column_no)
        elif source_string[PEEK_COPY] == '-':
            PEEK_COPY += 1
        
            if PEEK_COPY < SOURCE_STRING_LENGTH and source_string[PEEK_COPY] == '>':
                lexeme = "->"
                PEEK_COPY += 1
                token = Token(TokenType.ARROW, lexeme, line_no, column_no)
            elif PEEK_COPY + 1 < SOURCE_STRING_LENGTH and source_string[PEEK_COPY] == '-' and source_string[PEEK_COPY + 1] == '-':
                lexeme = '---'
                PEEK_COPY += 2
                token = Token(TokenType.ROW_DELIMITER, lexeme, line_no, column_no)
            else:
                token = Token(TokenType.DASH, lexeme, line_no, column_no)
        else:
            if recovery is False:
                error_list.append({"message": "Does not form any valid token", "loc": (line_no, column_no)})
            lexeme = source_string[PEEK_COPY]
            PEEK_COPY += 1
            token = Token(TokenType.ERROR, lexeme, line_no, column_no)
    if check is False:
        PEEK = PEEK_COPY
        column_no += len(lexeme) # required because of the white space
        CURRENT_COLUMN_NUMBER = column_no
        CURRENT_LINE_NUMBER = line_no
        
    # print(token.lexeme, token.line_no, token.col_no)
    return token
    

    
    
    

        
def match_token(token_type: TokenType):
    token = get_token(check=False)
    if token_type != token.token_type:
        error_list.append({"type": "matching", "message": f"Expected {token_type} but got {token.token_type} instead.", "loc": (token.line_no, token.col_no)})
    # print(token.token_type, end=" ")
    
def top_token(_recovery=False, _lookahead=1):
    return get_token(check=True, recovery=_recovery, lookahead=_lookahead)


def synchronize(non_terminal: str):
    while PEEK < SOURCE_STRING_LENGTH:
        top = top_token(_recovery=True)
        print(top.token_type)
        if top.token_type not in sync_map[non_terminal]:
            get_token(recovery=True)
        else:
            break
        
def syntax_error(received: Token, nonterminal: str, expected=[]):
    if len(expected) == 0:
        error_list.append({"type": "syntax", "message": f"Expected some other token. Received {received.token_type} instead", "loc": (received.line_no, received.col_no)})
    else:
        token_types = ",".join(list(map(lambda t: str(t), expected)))
        error_list.append({"type": "syntax", "message": f"Expected {token_types}. Received {received.token_type} instead", "loc": (received.line_no, received.col_no)})
    synchronize(nonterminal)

def matching_error(received: Token, expected=[]):
    expectation = ','.join(expected)
    error_list.append({"type": "matching", "message": f"Expected {expectation} but got {received.token_type} instead.", "loc": (received.line_no, received.col_no)})
            
def _option_list():
    
    op_list = []
    key = top_token()
    match_token(TokenType.LITERAL)
    match_token(TokenType.COLON)
    value = top_token()
    match_token(TokenType.LITERAL)
    op_list.append({key.lexeme: value.lexeme})
    top = top_token()
    if top.token_type == TokenType.COMMA:
        match_token(TokenType.COMMA)
        l = _option_list()
        op_list.extend(deepcopy(l))
    
    return deepcopy(op_list)
    

def _value():
    value = {}
    top = top_token()
    # print(top.token_type)
    # print("value => ", end=" ")
    # if top is None:
    #     raise Exception("Syntax error while matching value")
    if top.token_type == TokenType.NAME:
        match_token(TokenType.NAME)
        value['type'] = 'NAME'
        value['value'] = deepcopy(top.lexeme)
    elif top.token_type == TokenType.LITERAL:
        match_token(TokenType.LITERAL)
        value['type'] = 'LITERAL'
        value['value'] = deepcopy(top.lexeme)
    elif top.token_type == TokenType.LIST_BEGIN:
        match_token(TokenType.LIST_BEGIN)
        top = top_token()
        # if top is None:
        #     raise Exception("Syntax error for option_list")
        if top.token_type == TokenType.LITERAL:
            l = _option_list()
            # print(l)
            value['type'] = 'LIST'
            value['value'] = deepcopy(l)
            match_token(TokenType.LIST_END)
        
        elif top.token_type == TokenType.LIST_END:
            match_token(TokenType.LIST_END)
            value['type'] = 'LIST'
            value['value'] = []
        else:
            syntax_error(top, 'option_list', expected=[TokenType.LIST_END])
    else:
        matching_error(top, expected=[TokenType.NAME, TokenType.LITERAL, TokenType.LIST_BEGIN])
        
    return deepcopy(value)
    
        

def _key():
    key = None
    top = top_token()
    if top.token_type == TokenType.NAME:
        match_token(TokenType.NAME)
        key = deepcopy(top.lexeme)
    elif top.token_type == TokenType.LITERAL:
        match_token(TokenType.LITERAL)
        key = deepcopy(top.lexeme)
    else:
        matching_error(top, 'key', [TokenType.NAME, TokenType.LITERAL])
    
    return deepcopy(key)

def _id():
    id = None
    top = top_token()
    if top.token_type == TokenType.NAME:
        match_token(TokenType.NAME)
        
        id = deepcopy(top.lexeme)
    elif top.token_type == TokenType.LITERAL:
        match_token(TokenType.LITERAL)
        
        id = deepcopy(top.lexeme)
    else:
        matching_error(top, [TokenType.NAME, TokenType.LITERAL])
    return deepcopy(id)

def _key_value_pairs():
    key_value_pairs = {}
    top = top_token()
    if top.token_type in [ TokenType.NAME, TokenType.LITERAL]:
        key = _key()
        match_token(TokenType.COLON)
        value = _value()
        key_value_pairs[key] = value
        newtop = top_token()
        if newtop.token_type == TokenType.COMMA:
            match_token(TokenType.COMMA)
            kvpairs = _key_value_pairs()
            key_value_pairs = { **key_value_pairs, **kvpairs }
    else:
        syntax_error(top, 'key_value_pairs', [TokenType.NAME, TokenType.LITERAL])

    return deepcopy(key_value_pairs)

def _element():
    element = {}
    match_token(TokenType.DASH)
    top = top_token()
    if top.token_type in [TokenType.NAME, TokenType.LITERAL]:
        id = _id()
        match_token(TokenType.ARROW)
        newtop = top_token()
        if newtop.token_type in [TokenType.NAME, TokenType.LITERAL]:
            key_value_pairs = _key_value_pairs()
        else:
            syntax_error(newtop, 'key_value_pairs', [TokenType.NAME, TokenType.LITERAL])
        element['id'] = id
        element['properties'] = key_value_pairs
    else:
        syntax_error(top, 'element', [TokenType.NAME, TokenType.LITERAL])
    
    return deepcopy(element)
    

def _element_list():
    element_list = []
    top = top_token()
    if top.token_type in [TokenType.DASH]:
        element = _element()
        
        match_token(TokenType.SEMICOLON)
        element_list.append(element)
        newtop = top_token()
        if newtop.token_type == TokenType.DASH:
            el = _element_list()
            element_list.extend(deepcopy(el))
    else:
        syntax_error(top, 'element_list', [TokenType.DASH])
    
    return deepcopy(element_list)

def _rowgroup():
    match_token(TokenType.ROW_DELIMITER)
    rowgroup = []
    top = top_token()
    if top.token_type == TokenType.DASH:
        element_list = _element_list()
        rowgroup.append(deepcopy(element_list))
        newtop = top_token()
        newtop2 = top_token(_lookahead=2)
        if newtop.token_type == TokenType.ROW_DELIMITER and newtop2.token_type == TokenType.DASH:
            rg = _rowgroup() 
            rowgroup.extend(deepcopy(rg))
        else:
            match_token(TokenType.ROW_DELIMITER)
    else:
        syntax_error(top, 'rowgroup', [TokenType.DASH])
    
    return deepcopy(rowgroup)

def _block():
    block = []
    match_token(TokenType.SECTION)
    section_name = top_token()
    match_token(TokenType.LITERAL)
    match_token(TokenType.DOUBLE_COLON)
    
    top = top_token()
    if top.token_type == TokenType.ROW_DELIMITER:
        rowgroup = _rowgroup()
        block.append({"section_name": section_name.lexeme, "rows": rowgroup})
        newtop = top_token()
        if newtop.token_type == TokenType.SECTION:
            bl = _block()
            block.extend(bl)
    else:
        syntax_error(top, 'block', [TokenType.ROW_DELIMITER]) 
    
    return deepcopy(block)
    

def _style():
    style = {}
    match_token(TokenType.SECTION)
    match_token(TokenType.STYLE)
    match_token(TokenType.DOUBLE_COLON)
    top = top_token()
    if top.token_type == TokenType.DASH:
        element_list = _element_list()
        style["config"] = list(map(lambda el: {el['id']: el['properties']}, element_list))
    else:
        syntax_error(top, 'style', [TokenType.DASH]) 
    
    return deepcopy(style)
    

def _program():
    top = top_token()
    program = {}
    if top.token_type == TokenType.SECTION:
        style = _style()
        program['style'] = style
        newtop = top_token()
        if newtop.token_type == TokenType.SECTION:
            sections = _block()
            program['sections'] = sections
        else:
            syntax_error(newtop, 'block', [TokenType.SECTION])
    else:
        syntax_error(top, 'program', [TokenType.SECTION])
    
    return deepcopy(program)

def set_source_string(_source_string: str):
    global source_string, SOURCE_STRING_LENGTH
    source_string = _source_string
    SOURCE_STRING_LENGTH = len(_source_string)
    
def main():
    # with open("config.txt", "r") as f:
    #     config = f.read()
    #     print_tokens(config)
    source_string_cases = [ '("key1": "value1", "key2": "value2" ]' ]
    source_string_cases_2 = ['"literal example"', '["key1": "value1"), "key2": "value2"]', '[]', '["key1": "value1"]']
    # for ss in source_string_cases:
    #     print(ss)
    #     set_source_string(ss)
    #     _value()
    #     print()
    
    with open("config.txt", "r") as f:
        ss = f.read()
        set_source_string(ss)
        p = _program()
        print()
    
    # print(json.dumps(p))
    with open("config.json", "w") as f1:
        json.dump(p, f1, indent=4)
    
    print(error_list)

if __name__ == '__main__':
    main()