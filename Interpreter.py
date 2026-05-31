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
