### Analysis
The buggy function `table_exists` is supposed to check whether a table exists in a given database and optionally in a specific partition. It makes use of the `run_hive_cmd` function to execute Hive commands. The bug lies in the conditional blocks where it checks the output of the `run_hive_cmd` function. In the first block, it checks if the table name is in the output (`stdout`) which is incorrect. In the second block, it only checks if the output is truthy, but it should compare the output to a string indicating the existence of the partition.

### Bug
The bug is in how the function handles the output of the `run_hive_cmd` function. In the first part, it incorrectly checks for the presence of the table name in the output, while it should check for the exact string `'OK'`. In the second part, it only checks if the output is not empty, instead of checking for the specific existence of the partition pattern.

### Strategy for fixing the bug
1. In the first block, check if the `stdout` contains only the exact string `'OK'`.
2. In the second block, modify the condition to check if the `stdout` contains the specific partition pattern.

### Corrected Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout == 'OK'
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return 'OK' in stdout
```