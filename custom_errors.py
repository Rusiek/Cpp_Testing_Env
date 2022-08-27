from datetime import datetime


LOG_PATH = "log.txt"


def reset_log():
    log_file = open(LOG_PATH, "w")
    log_file.close()

def make_log(txt):
    output = ""
    log_file = open(LOG_PATH, "a")
    now = datetime.now()
    dt_string = now.strftime("[%H:%M:%S] ")
    log_file.write(dt_string + txt + "\n")
    output += dt_string + txt + "\n"
    log_file.close()
    return output

class ProgError(Exception):
    @staticmethod
    def print_msg():
        msg = make_log("Program Status:                   FAIL")
        return msg

class ArgError(Exception):
    @staticmethod
    def print_msg():
        msg = make_log("Invalid Type or Number of Arguments!!!")
        msg += ProgError.print_msg()
        return msg

class CmpFail(Exception):
    @staticmethod
    def print_msg():
        make_log("Compilation Status:               FAIL")
        ProgError.print_msg()

class CmpError(Exception):
    @staticmethod
    def print_msg():
        make_log("Compilation Error!!!")
        CmpFail.print_msg()

class CmpTimeout(Exception):
    @staticmethod
    def print_msg():
        make_log("Compilation Stopped")
        make_log("Process killed")
        CmpFail.print_msg()
