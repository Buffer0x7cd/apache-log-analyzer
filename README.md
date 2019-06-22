## Invokation of the command ##
### Supported Runttime: Python3+ ###
. To invoke the program run the file with a starting timestamp and ending timestamp and a list of files for processing    
Example:   
    ``` python main.py "20/Jun/2019:21:26:36 +0530" "21/Jun/2019:00:46:26 +0530" logs ```

Sample  Output:   
    ```
Between time 2019-06-20 21:26:36+05:30 and time 2019-06-21 00:46:26+05:30
32.23.210.7 got 1.3514% 5XX errors
69.14.123.112 got 1.3514% 5XX errors
228.176.133.39 got 1.3514% 5XX errors
68.15.160.51 got 1.3514% 5XX errors
211.128.180.109 got 1.3514% 5XX errors
    ```

External dependencies:   
    The Program is only dependent on the python standard library, this allow the program to be run in any enviornment without any kind of extra installation. Due to this capability this program serves well as the first level of analysis when a suddent need occures.

Assumptions:   
    The Primary assumtion of the programs is that the logs files should by thier timestamp values.