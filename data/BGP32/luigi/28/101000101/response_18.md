### Analysis:
- The function `table_exists` in the `HiveCommandClient` class checks if a table or a partition exists in a given database by running specific hive commands.
- The function calls `run_hive_cmd` to execute the hive commands.
- The bug occurs due to incorrect formatting in the hive command string when checking for partition existence which causes the function to always return False even if the partition exists.

### Bug:
In the else block of the `table_exists` function, the hive command string is incorrectly formatted, resulting in the incorrect verification of partition existence. This is causing the function to always return False when checking for partition existence.

### Fix:
Update the hive command string formatting in the else block to correctly check for partition existence.

### Corrected Version:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("""use {0}; show partitions {1} partition ({2})""".format(database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```