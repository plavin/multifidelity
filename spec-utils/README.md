# Spec + Ariel

This README covers the workflow for woking with SPEC CPU and Ariel. 

1. Instal SPEC

  - SPEC is easy to install. Just copy over the whole directory to where you want it. Then run `./install`. It should just install into the directory it is in. This step might not even be necessary.

  - When working with SPEC, make sure you run `source shrc` to set up your environment. 

2. Create a SPEC config

  - Go into $SPEC/config and copy one of the existing config files. Edit the parts marked `EDIT`.

3. Choose your benchmarks

  - Create a file _in this directory_, such as `song-benchmarks.txt` with the names of the SPEC benchmarks you want to run.

4. Generate configs for Ariel

  - Use the command `./generate.py <config name> <benchmarks file>` to create a file with a dict of configs for Ariel. This dict has two fields: `cmd` and `directory`. The former is the command used to run the benchmark and the latter is the directory the command must be run from. The reason for the directory change is that some of the arguments to the program are relative paths to files. 
  - This can take 10 minutes on flubber8
  - Potential issues:
    - Check to see if there are more then 1 set of build directories for the benchmarks (e.g. are the directories ending in numbers greater than 0000, such as 0001, and 0002?) You may want to delete those and retry. 
      - `runcpu <config-name> -a clean all`
      - `runcpu <config-name> -a realclean all`
      - `runcpu <config-name> -a clobber all`
    - These commands may help as well
      - `rm -Rf $SPEC/benchspec/C*/*/run`
      - `rm -Rf $SPEC/benchspec/C*/*/build`
      - `rm -Rf $SPEC/benchspec/C*/*/exe`
    - You shouldn't need these anymore but I'm leaving this for reference.

5. Use `simulate.py`

  - The last step should have generated a config file like the ones in `../workloads`. There are examples in this directory (`song_pattest_3.py` and `song_pattest_config.py`).
  - For example, run `./simulate.py song_pattest_3.py spec_ariel_test.py 0` to run the first benchmark (index 0)
