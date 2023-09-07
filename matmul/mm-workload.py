# ------------------------------------------------
# This is a simple config file used for testing.
# ------------------------------------------------
# Notes:
#  - If you use an input smaller that 15, then you
#    may not see parallel behavior on 4 threads.
# Format:
#   { '[NAME]' : {'cmd': '[PROGRAM AND ARGS]', 'directory': '[DIRECTORY TO RUN COMMAND IN]', ...}
# The NAME should be a unique identifier for each invocation of your program
# The simulator will execute the program from the directory specified
# Input and output redirection is allowed in the command
# 

{
    'mm' : { 'cmd': 'mm 15  5', 'directory': './'},
    'mm2' : { 'cmd': 'mm 20  5', 'directory': './'},
 }
