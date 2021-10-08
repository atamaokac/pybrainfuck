#!/usr/bin/env python3
import sys
commands = set('><+-.,[]')
source_filename = sys.argv[1]
memory = [0]
pointer = 0
source = []
stdin_line = []
with open(source_filename) as f:
    while line := f.readline():
        for s in line:
            if s in commands:
                source.append(s)
here = 0
while here < len(source):
    s = source[here]
    if s == '>':
        if pointer == len(memory) - 1:
            memory.append(0)
        pointer += 1
    elif s == '<':
        if pointer == 0:
            print('Error: Pointer moved to illegal region.', file=sys.stderr)
            exit()
        else:
            pointer -= 1
    elif s == '+':
        memory[pointer] += 1
        memory[pointer] %= 256
    elif s == '-':
        memory[pointer] -= 1
        memory[pointer] %= 256
    elif s == '.':
        print(chr(memory[pointer]), end='')
    elif s == ',':
        if not stdin_line:
            try:
                stdin_line = list(input().encode())[::-1]
            except:
                print('Error: Unexpected EOF in the input.', file=sys.stderr)
                exit()
        memory[pointer] = stdin_line.pop()
    elif s == '[':
        if memory[pointer] == 0:
            while here < len(source) and source[here] != ']':
                here += 1
            if here >= len(source):
                print('Error: Encountered [ without ].', file=sys.stderr)
                exit()
            continue
    elif s == ']':
        if memory[pointer] != 0:
            while here >= 0 and source[here] != '[':
                here -= 1
            if here < 0:
                print('Error: Encountered ] without [.', file=sys.stderr)
                exit()
            continue
    here += 1
