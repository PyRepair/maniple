### Bug Explanation:
The bug in the `table_exists` function lies in the condition check when `partition` is `None`. The function incorrectly checks if `table` is in the output of the `run_hive_cmd` function, which can cause unexpected behavior for certain inputs.

1. In Cases 1 and 3, the function returns `True` because the `stdout` value is `'OK'`, which causes `table in stdout` to evaluate to `True`, even though the table name does not match exactly.

2. In Cases 2 and 4, the function correctly identifies the table in the `stdout`, but due to case sensitivity, the function returns incorrectly (should return `True` when the table name is found in the `stdout`).

### Fix Strategy:
To fix the bug, we need to update the condition check so that it is case-insensitive. We should compare the table names by converting both sides to lowercase or uppercase before comparing them.

### Corrected Version:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        
        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
``` 

By converting both the `table` and `stdout` values to lowercase or uppercase in the comparison, we can ensure a case-insensitive match, fixing the bug.