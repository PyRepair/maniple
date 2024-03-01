### Bugs Analysis:
1. In the `table_exists` function, the conditional statements are not handling the case of the table name being present in the returned `stdout` properly.
2. The function is not correctly checking if the table exists in the database.

### Bug Fix Strategy:
1. Update the conditional statements to correctly handle the presence of the table in the `stdout`.
2. Properly check if the table exists in the database.

### Corrected Version of the Function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return table in stdout if stdout else False
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))

        return True if stdout else False
```