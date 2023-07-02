# Author: Ayelet Zadock
# Last modified: Jul 02 2023

# Imports:
import csv
from Globals import *
import math
import numpy as np

class CSVfile:
    '''
    CSVfile is a class for making calculations on a given CSV file.
    '''
    def __init__(self, filename):
        '''
        Constructor of CSVfile class
        :param filename: a csv filename to read
        '''
        self.file = open(filename)
        self.csvfile = csv.reader(self.file, delimiter=';')

    def csv_to_list(self):
        '''
        A function to convert the CSV file into list
        :return: a list of the rows in CSV file
        '''
        list_file = list(self.csvfile)
        self.file.seek(0)  # return to the top of the file
        return list_file

    def get_len(self):
        '''
        A function to get the amount of rows of the file
        :return: amount of rows of the file
        '''
        return len(self.csv_to_list())

    def get_line_by_index(self, index):
        '''
        A function to get line in CSV file by index
        :param index: index in file
        :return: data of file in the given index
        '''
        if index > self.get_len():
            return ERROR_TYPE
        line_data = self.csv_to_list()[index]
        return line_data

    def get_type_by_index(self, index):
        '''
        A function to get type of line by index
        :param index: index in file
        :return: type of line
        '''
        if index > self.get_len():
            return ERROR_TYPE
        line_type = self.get_line_by_index(index)
        return self.get_type_of_line(line_type)

    def get_type_of_line(self, line):
        '''
        A function to get type of line
        :param line: line in file
        :return: type of line
        '''
        line_type = line[0]
        if line_type == str(POLYLINE_TYPE) or line_type == str(POLYGON_TYPE):
            return int(line_type)
        return ERROR_TYPE

    def close_session(self):
        '''
        A function to close session
        :return: None
        '''
        self.file.close()

    def calculate_area_by_index(self, index):
        '''
        A function to calculate area of shape by index in file
        :param index: index in file
        :return: area of the shape
        '''
        line_data = self.get_line_by_index(index)
        if line_data == ERROR_TYPE:
            return ERROR_TYPE

        line_data = line_data[1:]
        return self.calculate_area_by_line(line_data)

    def calculate_area_by_line(self, line):
        '''
        A function to calculate area of given shape
        :param line: a list of coordinates
        :return: area of the shape
        '''
        line_data = line[1:]
        coordinates = [self.convert_strpoint_to_floatpoint(p) for p in line_data if self.convert_strpoint_to_floatpoint(p) != ERROR_TYPE]
        # get x and y in vectors
        x = [point[0] for point in coordinates]
        y = [point[1] for point in coordinates]
        # shift coordinates
        x_ = x - np.mean(x)
        y_ = y - np.mean(y)
        # calculate area
        correction = x_[-1] * y_[0] - y_[-1] * x_[0]
        main_area = np.dot(x_[:-1], y_[1:]) - np.dot(y_[:-1], x_[1:])
        return 0.5 * np.abs(main_area + correction)

    def get_max_area(self, shape_type):
        '''
        A function to get the maximum value of area for a given type of shape
        :param shape_type: type of shape
        :return: maximum value, error if there is no such type of shape
        '''
        if shape_type == POLYLINE_TYPE:
            shapes = self.get_all_polylines()
        elif shape_type == POLYGON_TYPE:
            shapes = self.get_all_polygons()
        else:
            return ERROR_TYPE
        max_area = max([self.calculate_area_by_line(shapes[i]) for i in range(len(shapes))])
        return max_area

    def calculate_length_by_index(self, index):
        '''
        A function to calculate length of given shape by index in file
        :param index: index in file
        :return: length of the shape
        '''
        line_data = self.get_line_by_index(index)
        if line_data == ERROR_TYPE:
            return ERROR_TYPE

        line_data = line_data[1:]
        return self.calculate_length_by_line(line_data)

    def calculate_length_by_line(self, line):
        '''
        A function to calculate length of given shape
        :param line: a list of coordinates
        :return: length of the shape
        '''
        line_data = line[1:]
        length = 0
        for i in range(len(line_data) - 1):
            p1, p2 = line_data[i], line_data[i+1]
            p1 = self.convert_strpoint_to_floatpoint(p1)
            p2 = self.convert_strpoint_to_floatpoint(p2)
            if p1 != ERROR_TYPE and p2 != ERROR_TYPE:
                length += math.dist(p1, p2)
        return length

    def get_max_length(self, shape_type):
        '''
        A function to calculate maximum length of a given shape
        :param shape_type: type of shape
        :return: maximum length, error if there is no such type of shape
        '''
        if shape_type == POLYLINE_TYPE:
            shapes = self.get_all_polylines()
        elif shape_type == POLYGON_TYPE:
            shapes = self.get_all_polygons()
        else:
            return ERROR_TYPE
        max_length = max([self.calculate_length_by_line(shapes[i]) for i in range(len(shapes))])
        return max_length

    def get_all_polylines(self):
        '''
        A function to get all polylines in file
        :return: a list of polylines
        '''
        polylines = [x for x in self.csv_to_list() if self.get_type_of_line(x) == POLYLINE_TYPE]
        return polylines

    def get_all_polygons(self):
        '''
        A function to get all polygons in file
        :return: a list of polygons
        '''
        polygons = [x for x in self.csv_to_list() if self.get_type_of_line(x) == POLYGON_TYPE]
        return polygons

    def convert_strpoint_to_floatpoint(self, p):
        '''
        A function to convert string point into float point
        :param p: a string of x,y values
        :return: a list of float x,y values
        '''
        try:
            x, y = p.split(',')
            x = float(x)
            y = float(y)
            p = [x, y]
            return p
        except:
            return ERROR_TYPE
