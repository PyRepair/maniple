### Analysis:
- The function `table_exists` is designed to check if a table (with optional partition) exists in a given database by running hive commands.
- The function checks the output of the hive commands to determine if the table exists or not.
- The bug seems to be related to the logic of checking if the table exists based on the output of the hive commands.

### Bug:
- In the faulty code, the function checks if the `table` name is directly present in the `stdout` output from the hive command to determine table existence. This can lead to false positives or negatives based on partial matches.
- The function is not handling case sensitivity properly, as it is doing a direct string match which may lead to incorrect results when comparing table names.

### Fix:
- To fix the bug, we should ensure that the table names are compared case-insensitively.
- We should check for an exact match of the table name in the `stdout` output to reduce false positives.
- Instead of checking if `table in stdout`, we should split the `stdout` by newline characters and check for an exact match of the table name in the list of tables.
- We should also ensure that the comparison is case-insensitive.
- The partitioned table case should also undergo similar checks to improve accuracy.

### Corrected Code:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables;'.format(database))
        tables = stdout.split('\n')
        return any([t.lower() == table.lower() for t in tables])
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
        partitions = stdout.split('\n')
        return any([p.lower() == self.partition_spec(partition) for p in partitions])
```