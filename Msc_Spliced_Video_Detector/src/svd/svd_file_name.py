'''
Created on 31 Jul 2019

@author: Niall
'''
#property called upon to store video file name
class FileName:

    def __init__(self,file_name):
        self.__file_name = file_name

    def get_file_name(self):
        return self.__file_name

    def set_file_name(self, file_name):
        self.__file_name = file_name