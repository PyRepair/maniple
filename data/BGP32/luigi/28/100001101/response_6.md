## Bug Fix Strategy
The bug in the `table_exists` function seems to stem from the condition checking when the `partition` parameter is not `None`. Instead of comparing the output (stdout) directly, the function should check if the table exists in the output. Additionally, there is inconsistency in case sensitivity between the input table name and the one in the output.

To fix the bug:
1. Adjust the condition for checking table existence.
2. Normalize the table names for comparison.

## The Corrected Version of the Function
```python
# The relative path of the fixed file: luigi/contrib/hive.py

def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
        return bool(stdout)
```