### Bug Explanation
The bug in the `table_exists` function lies in the conditional check for the presence of the table name in the stdout. The function incorrectly checks for the full match of the table name in the stdout, leading to incorrect results. The bug causes the function to return False when the table name is contained within the stdout, and True when there is an exact match with the table name.

### Bug Fix Strategy
To fix the bug, we need to modify the conditional check to correctly verify if the table name exists within the stdout, irrespective of its exact position. We can achieve this by using the `in` operator to check for the presence of the table name.

### Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
```

In the corrected version of the function, we use the `in` operator to check if the table name exists within the stdout. Additionally, we simplify the conditional return statement for the partition case by directly converting the `stdout` value to a boolean using the `bool` function.