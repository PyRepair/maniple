### Bug Explanation
The bug in the `table_exists` function lies in the conditional check for the existence of the table. In the if condition where `stdout` is checked for the presence of `table`, the function incorrectly returns the result. The issue is that when `stdout` is not `None`, it only checks if `table in stdout`, which can lead to incorrect results as the table name could be part of a larger string.

### Bug Fix Strategy
To fix the bug, we need to ensure that the table name is matched exactly within the `stdout`. We can achieve this by splitting the `stdout` by newline characters and then checking each element for an exact match with the table name.

### Updated Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        
        return stdout and any(t.strip() == table for t in stdout.split('\n'))
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
        
        if stdout:
            return True
        else:
            return False
```

By using `any(t.strip() == table for t in stdout.split('\n'))`, we ensure that we only return `True` if there is an exact match for the table name within the `stdout` output. This should fix the bug and make the function behave correctly according to the expected input/output values.