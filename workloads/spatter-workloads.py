# ------------------------------------------------
# This is a simple config file used for testing.
# ------------------------------------------------
# Notes:
#  - If you use an input smaller that 15, then you
#    may not see parallel behavior on 4 threads.

{
    'sp01' : { 'cmd': 'spatter -pFILE=bwcurve.json',  'directory': '../spatter/build_omp_gnu', 'ariel_markers':True},
    'sp02' : { 'cmd': 'spatter -pFILE=bwcurve2.json', 'directory': '../spatter/build_omp_gnu', 'ariel_markers':True},
}
