# Optimize

This directory contains a tool to help you choose your phase detection and stability detection parameters.

After collected a set of normal runs, you can use the tool `optimize` to sweep over a large set of configurations. It will output two scores for each configuration, an accuracy estimate and a speedup estimate. 

You can then use these data to do further analysis to choose your configuration. 

See the `*.out` files for examples of the output.

## Running
```
./optimize JUL-19-2 > out-jul-19-2.txt
```
