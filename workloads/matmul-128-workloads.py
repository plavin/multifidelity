# ------------------------------------------------
# Blocked Tests
# ------------------------------------------------
# Notes:
#  - If you use an input smaller that 15, then you
#    may not see parallel behavior on 4 threads.

{
    'mm-1'  : { 'cmd': 'mm 128 1', 'directory': './', 'ariel_markers': True},
    'mm-2'  : { 'cmd': 'mm 128 2', 'directory': './', 'ariel_markers': True},
    'mm-4'  : { 'cmd': 'mm 128 4', 'directory': './', 'ariel_markers': True},
    'mm-8'  : { 'cmd': 'mm 128 8', 'directory': './', 'ariel_markers': True},
    'mm-16'  : { 'cmd': 'mm 128 16', 'directory': './', 'ariel_markers': True},
    'mm-32'  : { 'cmd': 'mm 128 32', 'directory': './', 'ariel_markers': True},
    'mm-64'  : { 'cmd': 'mm 128 64', 'directory': './', 'ariel_markers': True},
    'mm-128'  : { 'cmd': 'mm 128 128', 'directory': './', 'ariel_markers': True},
}
