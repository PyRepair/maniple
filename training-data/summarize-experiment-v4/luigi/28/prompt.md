Please fix the buggy function provided below and output a corrected version.


Your output should follow these steps:
1. Analyze the buggy function and its relationship with the buggy class, related functions, test code, corresponding error message, the actual input/output variable information, the expected input/output variable information, the github issue.
2. Identify a potential error location within the buggy function.
3. Elucidate the bug's cause using:
   (a) The buggy function, 
   (b) The buggy class docs, 
   (c) The related functions, 
   (d) The failing test, 
   (e) The corresponding error message, 
   (f) The actual input/output variable values, 
   (g) The expected input/output variable values, 
   (h) The GitHub Issue information

4. Suggest approaches for fixing the bug.
5. Present the corrected code for the buggy function such that it satisfied the following:
   (a) the program passes the failing test, 
   (b) the function satisfies the expected input/output variable information provided, 
   (c) successfully resolves the issue posted in GitHub




## The source code of the buggy function

The buggy function is under file: `/home/ubuntu/Desktop/bgp_envs_local/repos/luigi_28/luigi/contrib/hive.py`

Here is the buggy function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False

```


## Summary of Related Functions

Class docstring: The `HiveCommandClient` class uses `hive` invocations to find information.

`def run_hive_cmd(hivecmd, check_return_code=True)`: This function is called within the `table_exists` function to execute a Hive command and check the return code.

`def partition_spec(self, partition)`: This function is also called within the `table_exists` function to format the partition specification before running the Hive command.

`def table_exists(self, table, database='default', partition=None)`: This function checks whether a table exists in a given database. It calls `run_hive_cmd` to execute Hive commands and uses `partition_spec` to format partition specifications, depending on whether a partition is provided as an argument or not.


## Summary of the test cases and error messages

Based on the error messages from test_table_exists and test_apacheclient_table_exists, we can see that in both failing test cases, the error occurs when the function table_exists returns False. More specifically, the AssertionError appears in both test cases when the test case insensitivity failed but the returned value still indicated False.


## Summary of Runtime Variables and Types in the Buggy Function

The relevant input/output values are:
- Input parameters: database (value: 'default', type: str), table (value: 'MyTable', type: str)
- Output: stdout (value: 'OK\nmytable', type: str)
Rational: The function is not correctly handling the case when the table name contains uppercase letters, leading to a mismatch in comparison and thus failing to return the expected result.


## Summary of Expected Parameters and Return Values in the Buggy Function

Case 1: Given the input parameters `database='default'` and `table='mytable'`, the function should return `stdout='OK'`, indicating that the table exists in the specified database.

Case 2: Given the input parameters `database='default'` and `table='MyTable'`, the function should return `stdout='OK\nmytable'`, also indicating that the table exists in the specified database.

Case 3: Given the input parameters `database='default'` and `table='mytable'`, the function should return `stdout='OK'`, indicating that the table exists in the specified database.

Case 4: Given the input parameters `database='default'` and `table='MyTable'`, the function should return `stdout='OK\nmytable'`, indicating that the table exists in the specified database.

In summary, the function should return the expected output values for the given input parameters, indicating whether the specified table exists in the specified database.


## A GitHub issue for this bug

The issue's title:
```text
hive table_exists should be case insensitive?
```

The issue's detailed description:
```text
Any thoughts on this one?\n\nIn https://github.com/spotify/luigi/blob/master/luigi/contrib/hive.py#L141\n(possibly here too, but we're not on CDH: https://github.com/spotify/luigi/blob/master/luigi/contrib/hive.py#L192)\n\nSometimes we have tables that are defined as capitalized, rather than lower case underscored names. These are easier to read in code if left capitalized, though hive is case insensitive, and will return them as lower case.\n\nE.g. when checking for an existing table table = 'FooBar', stdout will return with foobar and the test will fail\n\nThis wasn't an issue in older versions, which just checked for string \"does not exist\" or \"Table not found\" in stdout.\n\nWould be easy to fix using return stdout and table.lower() in stdout or return stdout and table.lower() in stdout.lower()\n\nLet me know your thoughts on this. I can supply a pull request if necessary.\n\nThanks,\nLin.
```

## A GitHub issue for this bug

The issue's title:
```text
Fix #896: make table_exists case insensitive
```

The issue's detailed description:
```text
Check stdout against table.lower() to avoid case issues
```

