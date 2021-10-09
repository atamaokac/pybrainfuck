#!/usr/bin/env python3
# version 1.1 - Bugfix for nested loops.
import sys
commands = set('><+-.,[]?')
source_filename = sys.argv[1]
memory = [0]
pointer = 0
source = []
stdin_line = []
loop_stack = []
loop_pair = dict()
here = 0
with open(source_filename) as f:
    while line := f.readline():
        for s in line:
            if s in commands:
                source.append(s)
                if s == '[':
                    loop_stack.append(here)
                elif s == ']':
                    if loop_stack:
                        there = loop_stack.pop()
                        loop_pair[here] = there
                        loop_pair[there] = here
                    else:
                        print('Error: Error: Encountered ] without [.', file=sys.stderr)
                        exit()
                here += 1
    if loop_stack:
        print('Error: Error: Encountered [ without ].', file=sys.stderr)
        exit()

here = 0
while here < len(source):
    s = source[here]
    if s == '>':
        if pointer == len(memory) - 1:
            memory.append(0)
        pointer += 1
    elif s == '<':
        if pointer == 0:
            print('Error: Pointer moved to illegal region, at {}-th command.'.format(here), file=sys.stderr)
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
            here = loop_pair[here]
            continue
    elif s == ']':
        if memory[pointer] != 0:
            here = loop_pair[here]
            continue
    elif s == '?':
        print(memory, ', pointer:{}'.format(pointer), ', command:{}'.format(here), file=sys.stderr)
    here += 1
