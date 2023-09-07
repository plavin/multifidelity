# ------------------------------------------------
# This is a simple config file used for testing.
# ------------------------------------------------
# Notes:
#  - If you use an input smaller that 15, then you
#    may not see parallel behavior on 4 threads.

{
    'sp-01' : { 'cmd': 'spatter -pUNIFORM:8:1:NR --runs=1 --count=500000',  'directory': '../spatter/build_omp_gnu', 'ariel_markers':True},
    'sp-02' : { 'cmd': 'spatter -pUNIFORM:8:2:NR --runs=1 --count=500000',  'directory': '../spatter/build_omp_gnu', 'ariel_markers':True},
    'sp-03' : { 'cmd': 'spatter -pUNIFORM:8:3:NR --runs=1 --count=500000',  'directory': '../spatter/build_omp_gnu', 'ariel_markers':True},
    'sp-04' : { 'cmd': 'spatter -pUNIFORM:8:4:NR --runs=1 --count=500000',  'directory': '../spatter/build_omp_gnu', 'ariel_markers':True},
    'sp-05' : { 'cmd': 'spatter -pUNIFORM:8:5:NR --runs=1 --count=500000',  'directory': '../spatter/build_omp_gnu', 'ariel_markers':True},
    'sp-06' : { 'cmd': 'spatter -pUNIFORM:8:6:NR --runs=1 --count=500000',  'directory': '../spatter/build_omp_gnu', 'ariel_markers':True},
    'sp-07' : { 'cmd': 'spatter -pUNIFORM:8:7:NR --runs=1 --count=500000',  'directory': '../spatter/build_omp_gnu', 'ariel_markers':True},
    'sp-08' : { 'cmd': 'spatter -pUNIFORM:8:8:NR --runs=1 --count=500000',  'directory': '../spatter/build_omp_gnu', 'ariel_markers':True},
}
