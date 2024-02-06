The function takes no input parameters and returns a string in the format of "Fish Shell {version}". 

Within the function, it uses the Popen function from the subprocess module to execute a command in a subshell and retrieves the output. The command being executed is `fish -c 'echo $FISH_VERSION'`, which retrieves the version of the current shell. 

The output of this command is read and decoded from bytes to a string, which is then stripped of any whitespace.

The function then returns a string in the format of "Fish Shell {version}".

The expected return value for the test case provided is "Fish Shell fish, version 3.5.9".