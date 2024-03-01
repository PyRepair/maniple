## Analysis:
The buggy function `table_exists` is not correctly handling the partition parameter when calling the `run_hive_cmd` function. The issue stems from how the partition information is passed to the `run_hive_cmd` function, causing the test case to fail.

## Bug:
The bug is in the line:
```python
stdout = run_hive_cmd("""use %s; show partitions %s partition
                                (%s)""" % (database, table, self.partition_spec(partition)))
```
The format string is incorrect, leading to an incorrect command being passed to `run_hive_cmd`.

## Fix:
To fix the bug, the partition string should be formatted correctly before being passed to the `run_hive_cmd` function.

## Corrected Version:
```python
def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
            return stdout and table in stdout
        else:
            partition_str = ', '.join(['{}="{}"'.format(k, v) for k, v in partition.items()])
            stdout = run_hive_cmd("""use {0}; show partitions {1} partition ({2})""".format(database, table, partition_str))
    
            if stdout:
                return True
            else:
                return False
```

By formatting the partition string using key-value pairs, the corrected version of the `table_exists` function should now correctly handle partitions and pass the failing test case.