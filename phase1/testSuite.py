import unittest
import subprocess
import time

def match(input, output):
    input = open(input, "r")
    output = open(output, "r")
    status = True

    for input_line in input:
        for output_line in output:
            if input_line.strip("\n") == output_line.strip("\n"):
                status = True
                break
            else:
                print("Expected Output: " + output_line)
                print("Received Output: " + input_line)
                status = False
    output.close()
    input.close()
    return status


def instructor_test_phase1():
    test_file_name = "test/instructor_samples/input/prog"


    for i in range(0, 6):
        input_file_name = "test/instructor_samples/input/prog" + str(i) + ".j"
        output_file_name = "test/instructor_samples/output/prog" + str(i) + ".out"
        f = open("test.out", "w")
        subprocess.call(["python3", "jott.py", input_file_name], stdout=f)

        if match("test.out", output_file_name):
            print("PASSED + " + input_file_name)









instructor_test_phase1()