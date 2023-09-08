# -----------------------------------------------
# SPEC home is:		/nethome/plavin3/spec/cpu/2017
# Config file:		$SPEC/config/patrick-test.cfg
# Benchmark file:	song-benchmarks.txt
# -----------------------------------------------
# Generating configs for: 641.leela_s 605.mcf_s 623.xalancbmk_s 607.cactuBSSN_s 621.wrf_s 654.roms_s
# -----------------------------------------------
# Step 1: Execute fake run to set up directories
# 641.leela_s: success
# 605.mcf_s: success
# 623.xalancbmk_s: success
# 607.cactuBSSN_s: success
# 621.wrf_s: success
# 654.roms_s: success
# -----------------------------------------------
# Step 2: Parse logs from step 1 to determine how to invoke benchmark
# 641.leela_s: success
# 605.mcf_s: success
# 623.xalancbmk_s: success
# 607.cactuBSSN_s: success
# 621.wrf_s: success
# 654.roms_s: success
# -----------------------------------------------
# Done. Printing configs. Call eval() on the output of this program to get the configs.
# -----------------------------------------------

{ '605.mcf_s': { 'cmd': '../run_base_test_pattest-m64.0003/mcf_s_base.pattest-m64 '
                        'inp.in  > inp.out 2>> inp.err',
                 'directory': '/nethome/plavin3/spec/cpu/2017/benchspec/CPU/605.mcf_s/run/run_base_test_pattest-m64.0003'},
  '607.cactuBSSN_s': { 'cmd': '../run_base_test_pattest-m64.0001/cactuBSSN_s_base.pattest-m64 '
                              'spec_test.par   > spec_test.out 2>> '
                              'spec_test.err',
                       'directory': '/nethome/plavin3/spec/cpu/2017/benchspec/CPU/607.cactuBSSN_s/run/run_base_test_pattest-m64.0001'},
  '621.wrf_s': { 'cmd': '../run_base_test_pattest-m64.0002/wrf_s_base.pattest-m64 '
                        '> rsl.out.0000 2>> wrf.err',
                 'directory': '/nethome/plavin3/spec/cpu/2017/benchspec/CPU/621.wrf_s/run/run_base_test_pattest-m64.0002'},
  '623.xalancbmk_s': { 'cmd': '../run_base_test_pattest-m64.0001/xalancbmk_s_base.pattest-m64 '
                              '-v test.xml xalanc.xsl > test-test.out 2>> '
                              'test-test.err',
                       'directory': '/nethome/plavin3/spec/cpu/2017/benchspec/CPU/623.xalancbmk_s/run/run_base_test_pattest-m64.0001'},
  '641.leela_s': { 'cmd': '../run_base_test_pattest-m64.0000/leela_s_base.pattest-m64 '
                          'test.sgf > test.out 2>> test.err',
                   'directory': '/nethome/plavin3/spec/cpu/2017/benchspec/CPU/641.leela_s/run/run_base_test_pattest-m64.0000'},
  '654.roms_s': { 'cmd': '../run_base_test_pattest-m64.0001/sroms_base.pattest-m64 '
                         '< ocean_benchmark0.in > ocean_benchmark0.log 2>> '
                         'ocean_benchmark0.err',
                  'directory': '/nethome/plavin3/spec/cpu/2017/benchspec/CPU/654.roms_s/run/run_base_test_pattest-m64.0001'}}
