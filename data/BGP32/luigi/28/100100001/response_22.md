Issue:
The buggy function `table_exists` is not correctly handling the output of the `run_hive_cmd` function. The bug is that the function is checking for the presence of the table name directly in the output without properly parsing the output of the `run_hive_cmd` function.

Fix:
To fix the bug, we should parse the output of the `run_hive_cmd` function to extract the table names correctly. Then, we can check if the given table exists in the extracted table names.

Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables in {1};'.format(database, table))
        tables = stdout.split('\n')
        return table in tables
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
        return bool(stdout)
```