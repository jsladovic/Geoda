from os.path import join
from scandir import walk

class CorParser:
    def __init__(self):
        self.output_files = {}

    def parse_files(self, input_path, output_path, first_last_only, n):
        for root, dirs, files in walk(input_path):
            for filename in files:
                if not filename.endswith('.cor'):
                     continue

                print filename
                [antenna_name, output_file] = self.find_output_file(input_path, output_path, filename)
                if output_file == None:
                    print 'Error when finding antenna type for file ' + filename
                    continue

                if first_last_only:
                    self.write_first_and_last_line_to_output(input_path, filename, antenna_name, output_file)
                else:
                    self.write_every_n_lines_to_output(input_path, filename, antenna_name, output_file, n)
                
        self.close_output_files()
    
    def read_lines_from_file(self, path, filename):
        with open(join(path, filename)) as f:
            return f.readlines()

    def format_line(self, line, antenna_name, filename):
        return line[:-1] + '\t' + antenna_name + '\t' + filename + '\n'

    def write_first_and_last_line_to_output(self, path, filename, antenna_name, output_file):   
        lines = self.read_lines_from_file(path, filename)
        if len(lines) < 2:
            return

        first_line = lines[0]
        last_line = lines[-1]
        output_file.write(self.format_line(first_line, antenna_name, filename))
        output_file.write(self.format_line(last_line, antenna_name, filename))
        
    def write_every_n_lines_to_output(self, path, filename, antenna_name, output_file, n):
        lines = self.read_lines_from_file(path, filename)
        every_nth_line = lines[0::n]
        for line in every_nth_line:
            output_file.write(self.format_line(line, antenna_name, filename))

    def find_output_file(self, input_path, output_path, filename):
        rad_filename = filename.replace('.cor', '.rad')
        lines = self.read_lines_from_file(input_path, rad_filename)
        antennas_lines = [line for line in lines if 'ANTENNAS:' in line]
        if len(antennas_lines) == 0:
            return None

        antennas_lines = antennas_lines[0].split(':')
        if len(antennas_lines) < 2:
            return None
        antenna_name = antennas_lines[1].split(' ')[0]
        output_filename = antenna_name + '.txt'
        if (output_filename in self.output_files):
            return antenna_name, self.output_files[output_filename]

        self.output_files[output_filename] = open(join(output_path, output_filename), 'w')
        return antenna_name, self.output_files[output_filename]

    def close_output_files(self):
        for _, output_file in self.output_files.iteritems():
            output_file.close()
