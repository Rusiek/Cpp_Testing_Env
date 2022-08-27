#g++ -std=c++17 -O3 main.cpp -lm
import sys
import os
from os.path import isfile, join
from custom_errors import *
from time import time, sleep
import subprocess
from check import compare

SLEEP_TIME = 1
LOG_PATH = "log.txt"
CMP_COMMAND = "g++ -std=c++17 -O3 main.cpp -lm"

class Raport():
    OK = 0
    ERROR = 0
    TIMEOUT = 0
    SYSFAULT = 0
    TIME = 0

    ERROR_LIST = []
    TIMEOUT_LIST = []
    SYSFAULT_LIST = []

def summary():
    file = open(LOG_PATH, "r")
    for line in file:
        print(line, end="")
    file.close()

def read_argv(argv):
    if len(argv) != 2:
        raise ArgError

    if argv[0][:2] == "./":
        argv[0] = argv[0][2:]
    argv[0] = argv[0].replace("/", "\\")

    dirpath = os.getcwd() + "\\" + argv[0]
    if not os.path.isdir(dirpath):
        raise ArgError
    try:
        max_time = int(argv[1])
        make_log(f"Test Directory:                   {dirpath}")
        make_log(f"UT Max Time:                      {max_time}s")
        make_log("Reading Arguments:                SUCCESS")
        return dirpath, max_time
    except:
        raise ArgError

def compile_cpp(max_time=60):
    cpp_path = os.getcwd() + "\\main.cpp" 
    make_log(f"Compiled File:                    {cpp_path}")
    make_log(f"Compilation Command:              {CMP_COMMAND}")
    make_log(f"Max Compilation Time:             {max_time}s")
    
    s_time = time()
    compile_process = subprocess.Popen(CMP_COMMAND.rsplit(" "))
    while time() - s_time < max_time and compile_process.poll() is None: pass
    if compile_process.poll() is None:
        compile_process.kill()
        raise CmpTimeout
    
    return_code = compile_process.returncode
    if return_code:
        raise CmpError.print_msg()
    make_log(f"Compilation Time:                 {round(time() - s_time, 3)}s")
    make_log("Compilation:                      SUCCESS")

def get_in_files(path):
    output = [
        path + "\\" + file for 
        file in os.listdir(path) if 
        isfile(join(path, file)) and file[-3:] == ".in"]
    output.sort()
    return output

def get_out_files(path):
    output = [
        path + "\\" + file for 
        file in os.listdir(path) if 
        isfile(join(path, file)) and file[-4:] == ".out"]
    output.sort()
    return output

def check_in_out(in_files, out_files):
    remove_list = []

    i, j = 0, 0
    while i < len(in_files) and j < len(out_files):
        if in_files[i][:-3] < out_files[j][:-4]:
            remove_list.append(in_files[i])
            in_files.pop(i)
        elif in_files[i][:-3] > out_files[j][:-4]:
            remove_list.append(out_files[j])
            out_files.pop(j)
        else:
            i += 1
            j += 1
    
    remove_list += in_files[i:]
    remove_list += out_files[j:]
    remove_list.sort()

    in_files = in_files[:i]
    out_files = out_files[:j]
    
def check_stdout(files_in, files_out, max_time):
    output = Raport()
    test_num = len(files_in)
    make_log("Collecting Tests:                 SUCCESS")
    make_log(f"Number of Tests:                  {test_num}")
    make_log("Testing Phase:                    STARTED\n")
    for i in range(test_num):
        make_log(f"Run Test:                         {files_in[i][:-3]}")
        file_in = open(files_in[i], 'r')
        file_out = open(files_out[i], 'r')
        buffor = open(f"{files_out[i][:-4]}_output.out", "w+")
        prog = subprocess.Popen(["./a"], stdin=file_in, stdout=buffor)
        s_time = time()
        while time() - s_time < max_time and prog.poll() is None: pass
        if prog.poll() is None:
            prog.kill()
            output.TIMEOUT += 1
            make_log("Test Result:                      TIMEOUT\n")
            buffor.close()
        elif prog.returncode:
            output.SYSFAULT += 1
            make_log("Test Result:                      SYSFAULT\n")
            buffor.close()
        else:
            buffor.close()
            run_time = time() - s_time
            make_log(f"Execution Time:                   {round(run_time, 3)}s")
            output.TIME += run_time
            buffor = open(f"{files_out[i][:-4]}_output.out", "r")
            res = compare(file_in, file_out, buffor)
            buffor.close()
            if res:
                output.OK += 1
                make_log("Test Result:                      OK\n")
            else:
                output.ERROR += 1
                make_log("Test Result:                      ERROR\n")
        file_out.close()
        file_in.close()
    return output

def print_raport(raport):
    make_log("Testing Phase:                    FINISHED")
    all_tests = raport.OK + raport.ERROR + raport.TIMEOUT + raport.SYSFAULT
    make_log(f"INI_OK:                           {raport.OK}/{all_tests}")
    make_log(f"INI_ERROR:                        {raport.ERROR}/{all_tests}")
    make_log(f"TIMEOUT:                          {raport.TIMEOUT}/{all_tests}")
    make_log(f"SYSFAULT:                         {raport.SYSFAULT}/{all_tests}")
    if raport.OK + raport.ERROR:
        avg_time = raport.TIME / (raport.OK + raport.ERROR)
        make_log(f"AVG TIME:                         {round(avg_time, 3)}s")

if __name__ == "__main__":
    try:
        reset_log()
        dirpath, max_time = read_argv(sys.argv[1:])
        compile_cpp()
        files_in = get_in_files(dirpath)
        files_out = get_out_files(dirpath)
        check_in_out(files_in, files_out)
        raport = check_stdout(files_in, files_out, max_time)
        print_raport(raport)
        summary()
    except ArgError:
        make_log(ArgError.print_msg())
    except CmpError:
        make_log(CmpError.print_msg())
    except CmpTimeout:
        make_log(CmpTimeout.print_msg())
