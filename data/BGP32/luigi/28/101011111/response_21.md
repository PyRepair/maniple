To fix the bug in the `table_exists` function, we need to make the comparison between the table name and the tables in the Hive database case insensitive. This will ensure that the function works correctly regardless of the case of the input table name. 

Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
        return bool(stdout)
```

By converting both the `table` and the `stdout` to lowercase before comparing, we ensure that the function is case insensitive and correctly identifies if the table exists in the database.

This change addresses the issue described in the GitHub post (#896) and the failing test cases provided. The function now satisfies the expected input/output values and should pass the test cases.