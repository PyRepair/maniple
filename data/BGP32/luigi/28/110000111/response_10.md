Potential Bug Locations:
1. The conditional check for `table in stdout` without considering the case sensitivity of the table name.
2. The conditional check for `return True` without considering the case sensitivity of the partition details.

Cause of the bug:
The bug arises from the case sensitivity issue in comparing the table name and partition details with the output obtained from the hive commands. Hive is case insensitive, so the comparison should be done in a case-insensitive manner to ensure correctness.

Strategy for fixing the bug:
To fix the bug, we need to ensure that the comparison of table names and partition details with the output from the hive commands is case insensitive. This can be achieved by converting both the table and output to lowercase before comparison.

Corrected Version of the Function:
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