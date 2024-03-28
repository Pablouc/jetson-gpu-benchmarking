

console_output = {}

def reset_console():
    global console_output
    console_output = {}


def get_console_logs():
    global console_output
    return console_output


def write_console_log(process, type):
    global console_output

    output_lines=[]
    if type == 'stdout':
        console_output[len(console_output)] = process.stdout

    if type == 'stderr':
        console_output[len(console_output)] = process.stderr

def write_print_toConsole(print_msg):
    global console_output

    console_output[len(console_output)] = print_msg
