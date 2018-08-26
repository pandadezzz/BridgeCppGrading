from collections import defaultdict
import subprocess
import os
import sys
import re

class BridgeBatchCompiler:
    def __init__(self, directory, program_input, subdirectory='Submission attachment(s)'):
        self.subdirectory = subdirectory
        self.program_input = program_input

        if os.path.isdir(directory):
            self.directory = directory
        else:
            raise Exception("Invalid directory")

    def __run_file(self, filepath):
        try:
            compile_file = subprocess.call([
                "g++",
                filepath
            ])
        except Exception as e:
            raise Exception("Compilation failed")


        # still not totally sure what this does
        run_executable = subprocess.Popen(
            "./a.out",
            shell=True,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        try:
            print('Running: {}'.format(filepath))
            output = run_executable.communicate(timeout=2, input=self.program_input)
        except subprocess.TimeoutExpired:
            print("Timeout happened\n")
            output = [[], [], ["Timeout"]]
            run_executable.kill()
        except Exception as e:
            print("{} contains error: {}".format(filepath, e))
            output = [[], [], ["Timeout"]]
            run_executable.kill()

        return [compile_file, run_executable, output]


    def __preprocess_file(self, abs_path):

        try:
            data = open(abs_path, newline='', encoding='utf16').read()
        except:
            data = open(abs_path, newline='').read()

        parsed_data = re.sub('#include "stdafx.h"', '', data)

        try:
            f = open(abs_path, 'w')
            f.write(parsed_data)
        except Exception as e:
            print(e)
        finally:
            f.close()


    def __get_results(self, question):
        result = defaultdict(list)
        for student_file in os.listdir(self.directory):
            # Assume here that the directory has a forward-slash
            filepath = "{}{}/{}/".format(self.directory,
                                 student_file,
                                 self.subdirectory)
            for cpp_file in os.listdir(filepath):
                if cpp_file.endswith("{}.cpp".format(question)):
                    abs_path = os.path.join(filepath, cpp_file)
                    self.__preprocess_file(abs_path)
                    try:
                        output = self.__run_file(abs_path)
                        if output[0] == 0:
                            result["result"].append({
                                "student_id": abs_path,
                                "output": output[2][0]
                            })
                    except Exception as e:
                        print(e)
                        print("Error on: {}".format(abs_path))
        return result

    def run(self, question):
        return self.__get_results(question)

if __name__ == '__main__':
    q1_test_case = input('Enter a test case for q1: ')
    q1_results = BridgeBatchCompiler(
        directory='../../cs-bridge/summer-extended-2018/hw4/homework #4/',
        program_input=b'4\n4\n').run(1)

    print("Done running...")

    for res in q1_results["result"]:
        print('{}: {}'.format(res['student_id'], res['output']))

