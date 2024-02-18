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

`def run_hive_cmd(hivecmd, check_return_code=True)`: This function is called within the `table_exists` function to execute a Hive command and return the standard output.

`def partition_spec(self, partition)`: This function is also called within the `table_exists` function to format the partition specification before running the Hive command.

`def table_exists(self, table, database='default', partition=None)`: This function checks whether a table exists in a given database. It calls `run_hive_cmd` to execute Hive commands and uses `partition_spec` to format partition specifications, if provided.


## Summary of the test cases and error messages

Based on the failing test cases and the error messages, the issue is likely within the table_exists function of the luigi.contrib.hive module. Specifically, the failing assertion of table_exists in both test cases cause an AssertionError due to the value not returning as expected. The problem seems to be due to case insensitivity, as evidenced by the issue #896 test case insensitivity check. This inconsistency leads to the failure of the table_exists function. Therefore, this function should be examined for potential issues when dealing with matching and comparing table names.


## Summary of Runtime Variables and Types in the Buggy Function

The relevant input/output values are:

### For Case 1 and Case 4
- Input parameters: table (value: 'mytable', type: str)
- Input parameters: database (value: 'default', type: str)
- Output: stdout (value: 'OK', type: str)

### For Case 2 and Case 5
- Input parameters: table (value: 'MyTable', type: str)
- Input parameters: database (value: 'default', type: str)
- Output: stdout (value: 'OK\nmytable', type: str)

Rational: The bug in the function may be related to how it handles the comparison of the table names. The function seems to be case-sensitive with table names, which might be leading to inconsistent results when checking for table existence.


## Summary of Expected Parameters and Return Values in the Buggy Function

In the buggy function table_exists, there are discrepancies in the expected outputs for the given test cases. In cases 1 and 3, the expected value of stdout is 'OK', but the function is currently returning True or False based on the presence of a table, indicating that the function is not working properly. Additionally, in cases 2 and 4, the expected values of stdout are 'OK\nmytable', but the function is currently returning True or False based on the presence of partitions, which also indicates an issue.


# A GitHub issue for this bug

The issue's title:
```text
hive table_exists should be case insensitive?
```

The issue's detailed description:
```text
Any thoughts on this one?\n\nIn https://github.com/spotify/luigi/blob/master/luigi/contrib/hive.py#L141\n(possibly here too, but we're not on CDH: https://github.com/spotify/luigi/blob/master/luigi/contrib/hive.py#L192)\n\nSometimes we have tables that are defined as capitalized, rather than lower case underscored names. These are easier to read in code if left capitalized, though hive is case insensitive, and will return them as lower case.\n\nE.g. when checking for an existing table table = 'FooBar', stdout will return with foobar and the test will fail\n\nThis wasn't an issue in older versions, which just checked for string \"does not exist\" or \"Table not found\" in stdout.\n\nWould be easy to fix using return stdout and table.lower() in stdout or return stdout and table.lower() in stdout.lower()\n\nLet me know your thoughts on this. I can supply a pull request if necessary.\n\nThanks,\nLin.
```

# A GitHub issue for this bug

The issue's title:
```text
Fix #896: make table_exists case insensitive
```

The issue's detailed description:
```text
Check stdout against table.lower() to avoid case issues
```

