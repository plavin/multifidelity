# ------------------------------------------------
# This is a simple config file used for testing.
# ------------------------------------------------
# Notes:
#  - If you use an input smaller that 15, then you
#    may not see parallel behavior on 4 threads.

{
    'sp-01' : { 'cmd': 'spatter -pUNIFORM:8:1:NR --runs=10 --count=25000',  'directory': '../spatter/build_omp_gnu', 'ariel_markers':True},
    'sp-02' : { 'cmd': 'spatter -pUNIFORM:8:2:NR --runs=10 --count=25000',  'directory': '../spatter/build_omp_gnu', 'ariel_markers':True},
    'sp-03' : { 'cmd': 'spatter -pUNIFORM:8:3:NR --runs=10 --count=25000',  'directory': '../spatter/build_omp_gnu', 'ariel_markers':True},
    'sp-04' : { 'cmd': 'spatter -pUNIFORM:8:4:NR --runs=10 --count=25000',  'directory': '../spatter/build_omp_gnu', 'ariel_markers':True},
    'sp-05' : { 'cmd': 'spatter -pUNIFORM:8:5:NR --runs=10 --count=25000',  'directory': '../spatter/build_omp_gnu', 'ariel_markers':True},
    'sp-06' : { 'cmd': 'spatter -pUNIFORM:8:6:NR --runs=10 --count=25000',  'directory': '../spatter/build_omp_gnu', 'ariel_markers':True},
    'sp-07' : { 'cmd': 'spatter -pUNIFORM:8:7:NR --runs=10 --count=25000',  'directory': '../spatter/build_omp_gnu', 'ariel_markers':True},
    'sp-08' : { 'cmd': 'spatter -pUNIFORM:8:8:NR --runs=10 --count=25000',  'directory': '../spatter/build_omp_gnu', 'ariel_markers':True},
    'sp-09' : { 'cmd': 'spatter -pUNIFORM:8:9:NR --runs=10 --count=25000',  'directory': '../spatter/build_omp_gnu', 'ariel_markers':True},
    'sp-10' : { 'cmd': 'spatter -pUNIFORM:8:10:NR --runs=10 --count=25000',  'directory': '../spatter/build_omp_gnu', 'ariel_markers':True},
    'sp-11' : { 'cmd': 'spatter -pUNIFORM:8:11:NR --runs=10 --count=25000',  'directory': '../spatter/build_omp_gnu', 'ariel_markers':True},
    'sp-12' : { 'cmd': 'spatter -pUNIFORM:8:12:NR --runs=10 --count=25000',  'directory': '../spatter/build_omp_gnu', 'ariel_markers':True},
    'sp-13' : { 'cmd': 'spatter -pUNIFORM:8:13:NR --runs=10 --count=25000',  'directory': '../spatter/build_omp_gnu', 'ariel_markers':True},
    'sp-14' : { 'cmd': 'spatter -pUNIFORM:8:14:NR --runs=10 --count=25000',  'directory': '../spatter/build_omp_gnu', 'ariel_markers':True},
    'sp-15' : { 'cmd': 'spatter -pUNIFORM:8:15:NR --runs=10 --count=25000',  'directory': '../spatter/build_omp_gnu', 'ariel_markers':True},
    'sp-16' : { 'cmd': 'spatter -pUNIFORM:8:16:NR --runs=10 --count=25000',  'directory': '../spatter/build_omp_gnu', 'ariel_markers':True},
}
