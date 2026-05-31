Building a compiler from scratch is one of the most rewarding projects in computer science. A compiler is essentially a translator: it takes a high-level source program (like Python or C) and transforms it into a lower-level target language (like Assembly or Machine Code) without changing the meaning of the program.

To make this practical and achievable, we are going to build a compiler for a simple arithmetic language (let's call it **NumLang**) that translates code into running **Python bytecode** or basic instructions.

A traditional compiler runs in a series of pipeline stages:

```
Source Code ──> [ Lexer ] ──> Tokens ──> [ Parser ] ──> AST ──> [ Code Generator ] ──> Target Code

```

---

## The 3 Core Stages of Our Compiler

1. **The Lexer (Lexical Analyzer):** Breaks raw text strings into labeled pieces called **Tokens** (numbers, operators, keywords).
2. **The Parser (Syntactic Analyzer):** Takes the stream of tokens and builds a hierarchical tree structure called an **Abstract Syntax Tree (AST)** based on grammar rules.
3. **The Code Generator:** Walks through the AST and translates those nodes into target code.

---

## Step 1: The Lexer (Tokenizing)

Our language will handle integers, `+`, `-`, `*`, `/`, and parentheses. First, we define what a token is and write a function to scan through the source string.

```python
import re

# Token Types
TOKEN_INT   = 'INT'
TOKEN_PLUS  = 'PLUS'
TOKEN_MINUS = 'MINUS'
TOKEN_MUL   = 'MUL'
TOKEN_DIV   = 'DIV'
TOKEN_LPAREN = 'LPAREN'
TOKEN_RPAREN = 'RPAREN'
TOKEN_EOF   = 'EOF'

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})" if self.value is not None else f"Token({self.type})"

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[0] if text else None

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return Token(TOKEN_INT, int(result))

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isdigit():
                return self.integer()
            if self.current_char == '+':
                self.advance()
                return Token(TOKEN_PLUS)
            if self.current_char == '-':
                self.advance()
                return Token(TOKEN_MINUS)
            if self.current_char == '*':
                self.advance()
                return Token(TOKEN_MUL)
            if self.current_char == '/':
                self.advance()
                return Token(TOKEN_DIV)
            if self.current_char == '(':
                self.advance()
                return Token(TOKEN_LPAREN)
            if self.current_char == ')':
                self.advance()
                return Token(TOKEN_RPAREN)
            
            raise SyntaxError(f"Invalid character: '{self.current_char}'")
        
        return Token(TOKEN_EOF)

```

---

## Step 2: The Parser (Building the AST)

Next, we map out the hierarchy. Operations like multiplication and division have higher **precedence** than addition and subtraction. We define AST nodes as simple Python classes.

```python
# AST Node Structures
class ASTNode: pass

class NumberNode(ASTNode):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class BinOpNode(ASTNode):
    def __init__(self, left, op_token, right):
        self.left = left
        self.op_token = op_token
        self.right = right

# The Parser
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token}, expected {token_type}")

    def factor(self):
        """factor : INT | LPAREN expr RPAREN"""
        token = self.current_token
        if token.type == TOKEN_INT:
            self.eat(TOKEN_INT)
            return NumberNode(token)
        elif token.type == TOKEN_LPAREN:
            self.eat(TOKEN_LPAREN)
            node = self.expr()
            self.eat(TOKEN_RPAREN)
            return node

    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        node = self.factor()
        while self.current_token.type in (TOKEN_MUL, TOKEN_DIV):
            op_token = self.current_token
            if op_token.type == TOKEN_MUL:
                self.eat(TOKEN_MUL)
            elif op_token.type == TOKEN_DIV:
                self.eat(TOKEN_DIV)
            node = BinOpNode(left=node, op_token=op_token, right=self.factor())
        return node

    def expr(self):
        """expr : term ((PLUS | MINUS) term)*"""
        node = self.term()
        while self.current_token.type in (TOKEN_PLUS, TOKEN_MINUS):
            op_token = self.current_token
            if op_token.type == TOKEN_PLUS:
                self.eat(TOKEN_PLUS)
            elif op_token.type == TOKEN_MINUS:
                self.eat(TOKEN_MINUS)
            node = BinOpNode(left=node, op_token=op_token, right=self.term())
        return node

    def parse(self):
        return self.expr()

```

---

## Step 3: The Code Generator (Targeting a Virtual Machine)

Instead of outputting raw standard binary file machinery (which is heavily OS-dependent), our compiler will target an **Assembly-like Stack Machine architecture**. Stack machines are how modern platforms like Java (JVM) and Python work under the hood.

* `PUSH [value]`: Puts a number on the stack.
* `ADD`, `SUB`, `MUL`, `DIV`: Pops the top two numbers, performs the operation, and pushes the result back.

```python
class CodeGenerator:
    def __init__(self):
        self.instructions = []

    def generate(self, node):
        if isinstance(node, NumberNode):
            self.instructions.append(f"PUSH {node.value}")
        
        elif isinstance(node, BinOpNode):
            # Compile the left side, then the right side (Post-order traversal)
            self.generate(node.left)
            self.generate(node.right)
            
            if node.op_token.type == TOKEN_PLUS:
                self.instructions.append("ADD")
            elif node.op_token.type == TOKEN_MINUS:
                self.instructions.append("SUB")
            elif node.op_token.type == TOKEN_MUL:
                self.instructions.append("MUL")
            elif node.op_token.type == TOKEN_DIV:
                self.instructions.append("DIV")
                
        return "\n".join(self.instructions)

```

---

## Running the Complete Pipeline

Let’s tie everything together into a driver function and compile an expression like `(14 + 2) * 3`.

```python
def compile_code(source_code):
    print(f"Source Code: {source_code}")
    
    # 1. Lexical Analysis
    lexer = Lexer(source_code)
    
    # 2. Syntax Analysis (Parsing)
    parser = Parser(lexer)
    ast = parser.parse()
    
    # 3. Code Generation
    codegen = CodeGenerator()
    compiled_assembly = codegen.generate(ast)
    
    return compiled_assembly

# Execution
source = "(14 + 2) * 3"
compiled_program = compile_code(source)

print("\n--- Compiled Target Assembly ---")
print(compiled_program)

```

### Output:

```text
Source Code: (14 + 2) * 3

--- Compiled Target Assembly ---
PUSH 14
PUSH 2
ADD
PUSH 3
MUL

```

---

## 🚀 Next Steps to Expand Your Compiler

If you want to grow this basic compiler into a feature-rich language engine, try implementing these modules in order:

* **Add a Symbol Table:** Create a dictionary structure to store and track named variables (e.g., `x = 5`).
* **Implement an Interpreter:** Build a tiny virtual machine stack wrapper loop in Python that loops over your generated `PUSH`, `ADD`, `MUL` instructions and physically evaluates them to output an execution result.
* **Type Checking:** Create a semantic analysis phase that throws errors if an engineer tries to perform illegal operations (like adding a string to an integer).
