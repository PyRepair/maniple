### Bug Explanation

The bug in the `table_exists` function lies in the condition for checking if the table exists based on the output of the `run_hive_cmd` function. In the current implementation, the `run_hive_cmd` function returns a string with the table names separated by `\n`, but the condition to check if the table exists is checking if the entire string matches the table name, which is causing the bug in the failing tests.

### Fix Strategy

To fix the bug, we need to modify the condition in the `table_exists` function to correctly check if the table name exists in the output of the `run_hive_cmd` function. We should split the stdout string based on `\n` and check if the table name exists in the list of table names.

### Corrected Version

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        tables = stdout.split('\n')
        return any(t.strip() == table for t in tables)
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
``` 

By making this change to the condition in the `table_exists` function, the tests should now pass successfully.