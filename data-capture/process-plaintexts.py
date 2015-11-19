#!/usr/bin/env python

with open('./data/plaintexts.txt', 'r') as f:
    plaintext_bytes = []
    for line in [l.strip() for l in f.readlines()]:
        plaintext_bytes.append([int(s, 16) for s in line.split(" ")])

num_lines = len(plaintext_bytes)
assert len(plaintext_bytes[0]) == 16
assert num_lines > 0 and num_lines < 1000

num_lines_str = 'const uint8_t N_PLAINTEXTS = ' + str(num_lines) + ';\n'
data_init_str = 'byte plaintext[N_PLAINTEXTS][N_BLOCK] =\n'
data_str = '{\n\t' + ',\n\t'.join(['{' + str(arr)[1:-1] + '}'  for arr in plaintext_bytes]) + '\n};'
total_data_str = data_init_str + data_str

with open('./arduino-code/sketch.unprocessed.ino', 'r') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        if '@1' in line:
            lines[i] = num_lines_str
        elif '@2' in line:
            lines[i] = total_data_str

    total_lines = ''.join(lines)


with open('./arduino-code/src/sketch.ino', 'w') as f:
    f.write(total_lines)


