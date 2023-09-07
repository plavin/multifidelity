# ------------------------------------------------
# Blocked Tests
# ------------------------------------------------
# Notes:
#  - If you use an input smaller that 15, then you
#    may not see parallel behavior on 4 threads.

{
    'mm-1'  : { 'cmd': 'mm-nosimd 180 1', 'directory': './', 'ariel_markers': True},
    'mm-2'  : { 'cmd': 'mm-nosimd 180 2', 'directory': './', 'ariel_markers': True},
    'mm-3'  : { 'cmd': 'mm-nosimd 180 3', 'directory': './', 'ariel_markers': True},
    'mm-4'  : { 'cmd': 'mm-nosimd 180 4', 'directory': './', 'ariel_markers': True},
    'mm-5'  : { 'cmd': 'mm-nosimd 180 5', 'directory': './', 'ariel_markers': True},
    'mm-6'  : { 'cmd': 'mm-nosimd 180 6', 'directory': './', 'ariel_markers': True},
    'mm-9'  : { 'cmd': 'mm-nosimd 180 9', 'directory': './', 'ariel_markers': True},
    'mm-10' : { 'cmd': 'mm-nosimd 180 10', 'directory': './', 'ariel_markers': True},
    'mm-12' : { 'cmd': 'mm-nosimd 180 12', 'directory': './', 'ariel_markers': True},
    'mm-15' : { 'cmd': 'mm-nosimd 180 15', 'directory': './', 'ariel_markers': True},
    'mm-18' : { 'cmd': 'mm-nosimd 180 18', 'directory': './', 'ariel_markers': True},
    'mm-20' : { 'cmd': 'mm-nosimd 180 20', 'directory': './', 'ariel_markers': True},
    'mm-30' : { 'cmd': 'mm-nosimd 180 30', 'directory': './', 'ariel_markers': True},
    'mm-36' : { 'cmd': 'mm-nosimd 180 36', 'directory': './', 'ariel_markers': True},
    'mm-45' : { 'cmd': 'mm-nosimd 180 45', 'directory': './', 'ariel_markers': True},
    'mm-60' : { 'cmd': 'mm-nosimd 180 60', 'directory': './', 'ariel_markers': True},
    'mm-90' : { 'cmd': 'mm-nosimd 180 90', 'directory': './', 'ariel_markers': True},
}