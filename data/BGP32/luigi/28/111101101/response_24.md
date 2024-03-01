### Bug Explanation
The bug arises because the `table_exists` function checks for the presence of the table name in the output of `run_hive_cmd`, but it does not handle the case where the table name is part of another word in the output. For example, in the second case where the table name is 'MyTable', the function incorrectly returns True because 'mytable' is found within the output 'OK\nmytable'.

### Bug Fix Strategy
To fix the bug, we need to modify the check for table existence to ensure that the table name is a standalone word in the output. One way to achieve this is by splitting the output into lines and checking each line for an exact match with the table name.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and any(line.strip() == table for line in stdout.split('\n'))
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                    (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
``` 

By using the `any()` function to iterate over the lines in the output and checking for an exact match with the table name, we ensure that the function only returns True if the table name is a standalone match in the output. The corrected version should now pass the failing tests and satisfy the expected input/output values.