import sys

out_file = sys.argv[1]
in_file = sys.argv[2]

with open(in_file, 'r', encoding='utf-8') as f_in:
    content = f_in.read()

with open(out_file, 'a', encoding='utf-8') as f_out:
    f_out.write(content + '\n\n')

print(f"Appended to {out_file}")
