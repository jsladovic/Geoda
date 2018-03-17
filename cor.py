from os.path import isfile, join
from scandir import walk

def read_lines_from_file(path, filename):
    with open(join(path, filename)) as f:
        return f.readlines()

def format_line(line, antenna_name, filename):
    return line[:-1] + '\t' + antenna_name + '\t' + filename + '\n'

def write_first_and_last_line_to_output(path, filename, antenna_name, output_file):   
    lines = read_lines_from_file(path, filename)
    if len(lines) < 2:
        return

    first_line = lines[0]
    last_line = lines[-1]
    output_file.write(format_line(first_line, antenna_name, filename))
    output_file.write(format_line(last_line, antenna_name, filename))
    
def write_every_n_lines_to_output(path, filename, antenna_name, output_file, n):
    lines = read_lines_from_file(path, filename)
    every_nth_line = lines[0::n]
    for line in every_nth_line:
        output_file.write(format_line(line, antenna_name, filename))

def find_output_file(path, filename, output_files):
    rad_filename = filename.replace('.cor', '.rad')
    lines = read_lines_from_file(path, rad_filename)
    antennas_lines = [line for line in lines if 'ANTENNAS:' in line]
    if len(antennas_lines) == 0:
        return None

    antennas_lines = antennas_lines[0].split(':')
    if len(antennas_lines) < 2:
        return None
    antenna_name = antennas_lines[1].split(' ')[0]
    output_filename = antenna_name + '.txt'
    if (output_filename in output_files):
        return antenna_name, output_files[output_filename]

    output_files[output_filename] = open(join(path, output_filename), 'w')
    return antenna_name, output_files[output_filename]

path = r'Z:\V1\!maxtor\MALA\ASCII'
#path = r'C:\Users\janko\Documents\work\geoda\files'

output_files = {}

for root, dirs, files in walk(path):
    for filename in files:
        if not filename.endswith('.cor'):
            continue

        [antenna_name, output_file] = find_output_file(path, filename, output_files)
        if output_file == None:
            print 'Error when finding antenna type for file ' + filename
            continue
        
        print filename
        #write_first_and_last_line_to_output(path, filename, antenna_name, output_file)
        write_every_n_lines_to_output(path, filename, antenna_name, output_file, 10)

for _, output_file in output_files.iteritems():
    output_file.close()
