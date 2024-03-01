## Analysis:
1. The buggy function `table_exists` takes a `table`, `database`, and an optional `partition` parameter.
2. It uses the `run_hive_cmd` function to execute certain Hive commands and checks if the table exists based on the command output.
3. The bug seems to be related to how the function handles the stdout from the `run_hive_cmd` function.
4. The function should return True if the table is found in the output and False otherwise.

## Bug:
The bug is in the logic for checking the existence of the table based on the stdout received from the `run_hive_cmd` function. The function is incorrectly checking for a substring in the stdout as a condition to determine if the table exists or not.

## Strategy for Fixing the Bug:
1. Modify the condition to correctly check if the exact table name is present in the stdout.
2. Ensure that the check returns True only if the exact table name is found in the stdout.

## Corrected Version:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                         (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout and table in stdout:
            return True
        else:
            return False
```