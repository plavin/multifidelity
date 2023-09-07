# -----------------------------------------------
# SPEC home is:		/nethome/plavin3/spec/cpu/2017
# Config file:		$SPEC/config/patrick-test.cfg
# Benchmark file:	memsys-spec-benchmarks.txt
# -----------------------------------------------
# Generating configs for: 625.x264_s 648.exchange2_s
# -----------------------------------------------
# Step 1: Execute fake run to set up directories
# 625.x264_s: success
# 648.exchange2_s: success
# -----------------------------------------------
# Step 2: Parse logs from step 1 to determine how to invoke benchmark
# 625.x264_s: success
# 648.exchange2_s: success
# -----------------------------------------------
# Done. Printing configs. Call eval() on the output of this program to get the configs.
# -----------------------------------------------

# Old binaries
#{ '625.x264_s': { 'cmd': '../run_base_test_pattest-m64.0000/x264_s_base.pattest-m64 '
#                         '--dumpyuv 50 --frames 156 -o BuckBunny_New.264 '
#                         'BuckBunny.yuv 1280x720 > '
#                         'run_000-156_x264_s_base.pattest-m64_x264.out 2>> '
#                         'run_000-156_x264_s_base.pattest-m64_x264.err',
#                  'directory': '/nethome/plavin3/spec/cpu/2017/benchspec/CPU/625.x264_s/run/run_base_test_pattest-m64.0000'},
#  '648.exchange2_s': { 'cmd': '../run_base_test_pattest-m64.0000/exchange2_s_base.pattest-m64 '
#                              '0 > exchange2.txt 2>> exchange2.err',
#                       'directory': '/nethome/plavin3/spec/cpu/2017/benchspec/CPU/648.exchange2_s/run/run_base_test_pattest-m64.0000'}}

{ '625.x264_s': { 'ariel_markers': True,
                 'cmd': '../run_base_test_pattest-m64.0000/x264_s '
                         '--dumpyuv 50 --frames 156 -o BuckBunny_New.264 '
                         'BuckBunny.yuv 1280x720 > '
                         'run_000-156_x264_s_base.pattest-m64_x264.out 2>> '
                         'run_000-156_x264_s_base.pattest-m64_x264.err',
                  'directory': '/nethome/plavin3/spec/cpu/2017/benchspec/CPU/625.x264_s/run/run_base_test_pattest-m64.0000'},
 '648.exchange2_s': {'ariel_markers': True,
                     'cmd': '../run_base_test_pattest-m64.0000/exchange2_s '
                              '0 > exchange2.txt 2>> exchange2.err',
                       'directory': '/nethome/plavin3/spec/cpu/2017/benchspec/CPU/648.exchange2_s/run/run_base_test_pattest-m64.0000'}}
