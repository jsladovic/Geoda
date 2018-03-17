from os.path import isfile, join
from scandir import walk

def read_lines_from_file(path, filename):
    with open(join(path, filename)) as f:
        return f.readlines()

def write_first_and_last_line_to_output(path, filename, output_file):   
    lines = read_lines_from_file(path, filename)
    if len(lines) < 2:
        return

    first_line = lines[0]
    last_line = lines[-1]
    output_file.write(first_line[:-1] + '\t' + filename + '\n')
    output_file.write(last_line[:-1] + '\t' + filename + '\n')
    
def write_every_n_lines_to_output(path, filename, output_file, n):
    lines = read_lines_from_file(path, filename)
    every_nth_line = lines[0::n]
    for line in every_nth_line:
        output_file.write(line[:-1] + '\t' + filename + '\n')    

path = r'Z:\V1\!maxtor\MALA\ASCII'
#path = r'C:\Users\janko\Documents\work\geoda\files'

output_filename = 'output.txt'
output_file = open(join(path, output_filename), 'w')

for root, dirs, files in walk(path):
    for filename in files:
        if not filename.endswith('.cor'):
            continue
        #write_first_and_last_line_to_output(path, filename, output_file)
        write_every_n_lines_to_output(path, filename, output_file, 10)
    
output_file.close()
