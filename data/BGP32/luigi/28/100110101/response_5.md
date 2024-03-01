## Correction:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return table in stdout.split()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
        return bool(stdout)
``` 

Explanation:
1. The bug was caused by the incorrect evaluation of the condition in the function's return statement. The buggy function did not properly split the stdout to check if the table name exists.
   
2. The corrected version splits the stdout into separate lines and checks if the table name is present in the lines, returning the appropriate boolean value based on the result.

By making this adjustment, the corrected function should now pass the failing test cases and provide the expected output values.