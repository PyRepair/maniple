### Bug Analysis:
The buggy function `table_exists` has an issue in the conditional statements determining whether a table exists in a given database. In the first case, the function incorrectly checks for the presence of the entire table name in the output, leading to incorrect results. The second case also shows a similar problem due to the way the function compares the table name in the output.

### Bug Fix Strategy:
To fix the bug, we need to correct the condition for checking table existence based on the expected output from the `run_hive_cmd` function. Instead of checking if the entire table name is in the output, we should check if the table name is present as a separate entity in the output.

### Corrected Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return table in stdout.split('\n')  # Check if table exists in the list of tables
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)  # If stdout is not empty, return True, else False
``` 

This corrected version addresses the issue by splitting the `stdout` string at newline characters and checking if the table name exists in the list. Additionally, in the else part, it directly returns the boolean result of checking if `stdout` is empty or not.