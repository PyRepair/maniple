### Bug Explanation
The bug in the `table_exists` function is caused by incorrect handling of the stdout variable when checking if a table exists in the database. In the first if branch, the condition `return stdout and table in stdout` would evaluate to `True` if `stdout` is not empty, regardless of whether the table actually exists in the output. This leads to incorrect results.

### Fix Strategy
To fix the bug, we need to properly check for the table existence in the stdout. We can split the stdout by newline characters and then check if the table exists in the resulting lines. 

### Corrected Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout.split('\n')
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return any(part in stdout.split('\n') for part in self.partition_spec(partition))
``` 

This corrected version splits the stdout by newline characters and then checks for the existence of the table in each line for the first case and the partitions in the subsequent cases. Now, the function should return the correct results according to the expected input/output values.