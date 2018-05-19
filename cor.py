import os
from scandir import walk
from shutil import copy2
import time

from xml.etree.ElementTree import Element, SubElement, tostring

class CorParser:
    def __init__(self):
        self.output_files = {}

    def convert_to_gpgga(self, input_path, output_path, step):
        print '\nConverting .cor files to .gps started'
        files = self.get_all_files_in_path(input_path)
        for filename in files:
            if not filename.endswith('.cor'):
                continue

            output_filename = filename.split('.')[0] + '.gps'
            output_file = open(os.path.join(output_path, output_filename), 'w')
            self.output_files[output_filename] = output_file

            self.convert_input_file(input_path, filename, output_file, step)

        self.close_output_files()

    def backup_files(self, input_path, output_path):
        print '\nFile backup started'
        sorted_files = self.sort_files_into_dictionary(self.get_all_files_in_path(input_path))
        for group in sorted_files:
            cor_filename = group + '.cor'
            if cor_filename not in sorted_files[group]:
                continue
            
            first_line = self.read_lines_from_file(input_path, cor_filename, True).split()
            if len(first_line) < 2:
                print 'Invalid file ' + cor_filename
                continue
            
            folder_name =  first_line[1] + '/'
            for filename in sorted_files[group]:
                path = os.path.join(output_path, folder_name)
                if not os.path.exists(path):
                    os.makedirs(path)
                copy2(os.path.join(input_path, filename), path)

    def parse_files(self, input_path, output_path, first_last_only, n, create_kml = False):
        print '\nFile parsing started'
        files = self.get_all_files_in_path(input_path)

        if create_kml:
            kml_data = []
        for filename in files:
            if not filename.endswith('.cor'):
                continue

            print filename
            [antenna_name, output_file] = self.find_output_file(input_path, output_path, filename)
            if output_file == None:
                print 'Error when finding antenna type for file ' + filename
                continue

            if first_last_only:
                lines = self.write_first_and_last_line_to_output(input_path, filename, antenna_name, output_file)
            else:
                lines = self.write_every_n_lines_to_output(input_path, filename, antenna_name, output_file, n)

            if create_kml:
                kml_data.append([filename.split('.')[0], lines])
                
        self.close_output_files()
        if create_kml:
            self.create_kml_file(output_path, kml_data)

    def create_kml_file(self, output_path, kml_data):
        if len(kml_data) == 0:
            return
        elif len(kml_data) == 1:
            filename = kml_data[0][0] + '.kml'
        else:
            filename = kml_data[0][0] + '-' + kml_data[-1][0]
        
        kml = Element('kml')
        document = SubElement(kml, 'Document')
        folder = SubElement(document, 'Folder')

        name = SubElement(folder, 'name')
        name.text = filename

        for element in kml_data:
            placemark = SubElement(folder, 'Placemark')

            description = SubElement(placemark, 'name')
            description.text = element[0]
            
            line_string = SubElement(placemark, 'LineString')
            coordinates = SubElement(line_string, 'coordinates')

            for line in element[1]:
                line = self.transform_coordinates(line)
                if coordinates.text is None:
                    coordinates.text = line
                else:
                    coordinates.text += ' ' + line + ' '

        output_file = open(os.path.join(output_path, filename + '.kml'), 'w')
        output_file.write(tostring(kml))
        output_file.close()

    def transform_coordinates(self, line):
        elements = line.split()
        return elements[5] + ',' + elements[3]

    def get_all_files_in_path(self, path):
        files = []
        for root, dirs, filenames in walk(path):
            for filename in filenames:
                if root != path:
                    continue
                files.append(filename)

        return files

    def sort_files_into_dictionary(self, files):
        dictionary = {}
        for filename in files:
            main_part = filename.split('.')[0]
            if main_part not in dictionary:
                dictionary[main_part] = []
            dictionary[main_part].append(filename)

        return dictionary
    
    def read_lines_from_file(self, path, filename, only_first_line = False):
        with open(os.path.join(path, filename)) as f:
            if only_first_line:
                return f.readline()
            return f.readlines()

    def format_line(self, line, antenna_name, filename):
        return line[:-1] + '\t' + antenna_name + '\t' + filename + '\n'

    def convert_input_file(self, path, filename, output_file, step):
        lines = self.read_lines_from_file(path, filename)
        for line in lines:
            output_file.write(self.line_cor_to_gpgga(line, step))

    def write_first_and_last_line_to_output(self, path, filename, antenna_name, output_file):   
        lines = self.read_lines_from_file(path, filename)
        if len(lines) < 2:
            return

        output_file.write(self.format_line(lines[0], antenna_name, filename))
        output_file.write(self.format_line(lines[-1], antenna_name, filename))

        return [lines[0], lines[-1]]
        
    def write_every_n_lines_to_output(self, path, filename, antenna_name, output_file, n):
        lines = self.read_lines_from_file(path, filename)
        every_nth_line = lines[0::n]
        if (len(lines) % n) != 1:
            every_nth_line.append(lines[-1])
        
        for line in every_nth_line:
            output_file.write(self.format_line(line, antenna_name, filename))

        return every_nth_line

    def line_cor_to_gpgga(self, line, step):
        elements = line.split()
        # broj traga index 0, vrijeme index 2
        trace_number = int(elements[0])
        trace_time = self.time_to_gpgga_time(elements[2])
        # x koordinata index 3, 4
        x_coordinate = self.coordinate_to_minutes(elements[3])
        x_additional = elements[4]
        # y koordinata index 5, 6
        y_coordinate = self.coordinate_to_minutes(elements[5])
        y_additional = elements[6]
        return 'Trace #{0} at position {1}\n$GPGGA,{2},{3},{4},{5},{6},2,09,1.2,110.2,M,-35.1,M,,138*68\n'.format(
            trace_number, trace_number * step, trace_time, x_coordinate, x_additional, y_coordinate, y_additional)

    def coordinate_to_minutes(self, coordinate):
        temp = coordinate.split('.')
        return temp[0] + str(round((float(coordinate) - float(temp[0])) * 60, 4))

    def time_to_gpgga_time(self, cor_time):
        time_temp = time.strptime(cor_time, '%H:%M:%S:%f')
        return time.strftime('%H%M%S', time_temp)

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

        self.output_files[output_filename] = open(os.path.join(output_path, output_filename), 'w')
        return antenna_name, self.output_files[output_filename]

    def close_output_files(self):
        for _, output_file in self.output_files.iteritems():
            output_file.close()
