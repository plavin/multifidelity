# Spec + Ariel

This README covers the workflow for woking with SPEC CPU and Ariel. 

1. Instal SPEC

  - SPEC is easy to install. Just copy over the whole directory to where you want it. Then run `./install`. It should just install into the directory it is in. This step might not even be necessary.

  - When working with SPEC, make sure you run `source shrc` to set up your environment. 

2. Create a SPEC config

  - Go into $SPEC/config and copy one of the existing config files. Edit the parts marked `EDIT`.

3. Choose your benchmarks

  - Create a file, such as `song-benchmarks.txt` with the names of the SPEC benchmarks you want to run.

4. Generate configs for Ariel

  - Use the command `./generate.py <config name> <benchmarks file>` to create a file with a dict of configs for Ariel. This dict has two fields: `cmd` and `directory`. The former is the command used to run the benchmark and the latter is the directory the command must be run from. The reason for the directory change is that some of the arguments to the program are relative paths to files. 

5. Run Ariel

  - You can run `sst --stop-at 25ms spec_ariel_test.py` to try out the benchmarks in SST on a simple architecture.

