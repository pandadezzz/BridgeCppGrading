import subprocess
import os
import sys

'''
We want to compile the programs by question
'''
class BridgeBatchCompiler:
    '''
    directory: String
        String representation of the directory where homework files are stored

    questions: List[Int]
        Range of questions for a given assignment
    '''
    def __init__(self, directory, subdirectory='Submission attachment(s)'):
        self.subdirectory = subdirectory

        if os.path.isdir(directory):
            self.directory = directory
        else:
            raise Exception("Invalid directory")

    def __run_file(self, filepath):
        compile_file = subprocess.call([
            "g++",
            "-o output",
            filepath
        ])

        # still not totally sure what this does
        run_executable = subprocess.Popen(
            "./output",
            shell=True,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        try:
            # we should allow the user to read through test cases
            # automate this portion rather than having a million executables
            output = run_executable.communicate()


    def __preprocess_file(self, abs_path):
        encoding = ['utf-8', 'utf-16le']
        # try opening the file first
        try:
            f = open(abs_path, 'r').read()
        except Exception:
            sys.exit(1)

        for enc in encoding:
            try:
                f = f.replace('#include "stdafx.h"', '')
                data = f.decode(enc)
            except Exception:
                if enc == encoding[-1]:
                    sys.exit(1)
                continue
            finally:
                break

        f = open(abs_path, 'w')
        try:
            f.write(data.encode('utf-8'))
        except Exception as e:
            print(e)
        finally:
            f.close()


    def __get_results(self, question):

        for student_file in os.listdir(self.directory):
            # Assume here that the directory has a forward-slash
            filepath = "{}{}/{}/".format(self.directory,
                                 student_file,
                                 self.subdirectory)
            for cpp_file in os.listdir(filepath):
                if cpp_file.endswith("{}.cpp".format(question)):
                    abs_path = os.path.join(filepath, cpp_file)
                    self.__preprocess_file(abs_path)


    def run(self, question):
        self.__get_results(question)

if __name__ == '__main__':
    BridgeBatchCompiler(
        directory='../../cs-bridge/summer-extended-2018/hw4/homework #4/').run(1)

