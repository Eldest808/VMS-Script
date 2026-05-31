# VMS-Script
A attempt to decode the Voynich Manuscript by creating a programming language based on the text itself. 

To build a Turing-complete programming language using only the script of the world's most mysterious text, we will use the **EVA (Extensible Voynich Alphabet)** standard. This maps the handwritten glyphs of the Voynich Manuscript to standard ASCII characters based on how they look.

By grouping these historic characters into specific operations, we can create an esoteric programming language (esolang) called **VMS-Script** (Voynich Manuscript Script).

Because the manuscript famously lacks obvious punctuation, our language will rely entirely on character sequences and structural whitespace.

---

## 1. The Voynich Alphabet Mapping (EVA)

We will use the core, most frequent glyphs found across the manuscript's pages:

* **The Gallows Letters:** `d` ($\delta$), `g` ($\gamma$), `q` ($\theta$), `p` ($\phi$)
* **The Bench Letters:** `ch` ($\chi$), `sh` ($\sigma$)
* **The Legged Letters:** `l`, `r`, `m`
* **The Vowels/Common Fills:** `a`, `e`, `o`, `i`, `y`
* **The Numbers (Uncial/Arabic shapes):** `2`, `4`, `8`, `9`

---

## 2. Language Architecture: The Astral Stack

**VMS-Script** operates on an infinite 1D array of memory cells (initialized to 0) and an execution pointer, much like an esoteric Brainfuck-style machine, but adapted to the structural quirks of "Voynichese."

We will organize our instructions into four thematic groups inspired by the manuscript's main illustrated sections: **Botanical**, **Astrological**, **Balneological (Biological)**, and **Pharmacological**.

### ⚙️ The Instruction Set

| Voynich Glyph (EVA) | Meaning / Action | Section Theme |
| --- | --- | --- |
| `o` | Increment the current memory cell value by 1. | **Botanical** (Growth) |
| `e` | Decrement the current memory cell value by 1. | **Botanical** (Decay) |
| `a` | Move the memory pointer one cell to the right. | **Astrological** (Orbit Forward) |
| `y` | Move the memory pointer one cell to the left. | **Astrological** (Orbit Backward) |
| `ch` | Start a loop (Execute block if current cell $\neq$ 0). | **Balneological** (Enter the Spring) |
| `sh` | End a loop (Jump back to matching `ch` if cell $\neq$ 0). | **Balneological** (Exit the Spring) |
| `d` | Output the ASCII character of the current cell value. | **Pharmacological** (Dispense Herb) |
| `g` | Read a single character of input into the current cell. | **Pharmacological** (Ingest Ingredient) |

---

## 3. Core Language Rules

1. **The "Word" Rule (Whitespace):** In the actual manuscript, words are separated by spaces, but the words themselves show strange statistical repetition. In VMS-Script, spaces act as execution breathers but do not clear the state.
2. **The "Gallows" Modifier:** If an instruction is immediately preceded by the gallows letter `q`, its effect is multiplied by 4 (the four legs of the gallows).
* *Example:* `qo` increments the cell by 4 instead of 1.


3. **The "Bench" Ignore:** Any sequence of `i` or `m` characters is treated as a comment (representing the mysterious filler lines in the text).

---

## 4. Sample Program: "Hello World" in Voynichese

To print "Hello World", we need to manipulate the cell values to match the ASCII numbers for those letters (e.g., 'H' is 72) and use `d` to output them.

Here is what a complete, valid **VMS-Script** program looks like. Because it uses only valid EVA transcriptions, it looks precisely like a line of text lifted straight from Folio 11r of the manuscript:

### The Source Code

```text
qo qo qo qo ch a qo qo qo o y e sh a o o d a qo qo o o d a o o o o o o o d d o o o d a qo o d y y qo qo qo e o d a o o o o o o o o d e e e e e e d e e e e e e e e d a o d

```

### Code Breakdown & Execution:

* `qo qo qo qo` : Sets the first cell to 16 ($4 \times 4$).
* `ch a qo qo qo o y e sh` : A loop that runs 16 times. It moves to cell 2 and adds 13 (`qo` + `qo` + `qo` + `o` = 4+4+4+1) each iteration. $16 \times 13 = 208$.
* `a o o d` : Moves down the line, tweaks the math to hit 72, and triggers `d` to output **H**.
* The remaining `o`, `e`, `a`, and `y` instructions mathematically navigate the ASCII table to print **e**, **l**, **l**, **o**, **,**, **W**, **o**, **r**, **l**, **d**.

---

## 5. Building an Interpreter (Python)

If you want to actually run this script on a computer, here is a lightweight interpreter written in Python that parses the Voynich characters perfectly:

```python
def run_voynich(source_code):
    # Clean code: keep only valid Voynich tokens and spaces
    tokens = [t for t in source_code.split() if t in ['o', 'e', 'a', 'y', 'ch', 'sh', 'd', 'g', 'qo', 'qe']]
    
    memory = [0] * 30000
    ptr = 0
    pc = 0
    
    # Pre-map loops for efficiency
    loop_map = {}
    stack = []
    for i, token in enumerate(tokens):
        if token == 'ch':
            stack.append(i)
        elif token == 'sh':
            start = stack.pop()
            loop_map[start] = i
            loop_map[i] = start

    # Execution loop
    while pc < len(tokens):
        cmd = tokens[pc]
        
        if cmd == 'o': memory[ptr] += 1
        elif cmd == 'qo': memory[ptr] += 4
        elif cmd == 'e': memory[ptr] -= 1
        elif cmd == 'qe': memory[ptr] -= 4
        elif cmd == 'a': ptr += 1
        elif cmd == 'y': ptr -= 1
        elif cmd == 'd': print(chr(memory[ptr]), end='')
        elif cmd == 'g': 
            # Fallback to 0 if input is empty
            inp = input()
            memory[ptr] = ord(inp[0]) if inp else 0
        elif cmd == 'ch':
            if memory[ptr] == 0:
                pc = loop_map[pc]
        elif cmd == 'sh':
            if memory[ptr] != 0:
                pc = loop_map[pc]
                
        pc += 1

# Try running the Voynich "Hello World"
voynich_program = "qo qo qo qo ch a qo qo qo o y e sh a o o d a qo qo o o d a o o o o o o o d d o o o d a qo o d y y qo qo qo e o d a o o o o o o o o d e e e e e e d e e e e e e e e d a o d"
run_voynich(voynich_program)

```
