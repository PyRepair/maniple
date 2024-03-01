### Bug Explanation:
The bug in the `table_exists` function arises from the incorrect logic in checking the presence of the table in the output. The function is checking if the table name is directly contained in the output string, which can lead to false positives. The function should accurately parse the output string to ensure that the table name is not just a part of another word or string within the output.

### Bug Fix Strategy:
1. Change the logic to accurately parse the output and check if the table name is present in the list of tables or partitions.
2. Implement a more robust check to handle cases where the table name might be part of another string or word in the output.
3. Ensure that the function returns `True` only if the table name is present as a standalone entry in the output list.

### Corrected Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables in {1};'.format(database, table))
        tables = stdout.split('\n')[1:]  # Skip the "OK" in the beginning

        return table in tables
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
        partitions = stdout.split('\n')[1:]  # Skip the "OK" in the beginning

        return any(partition in p for p in partitions)
```

By splitting the `stdout` string and parsing the tables or partitions correctly, we can ensure that the `table_exists` function behaves as expected and passes the failing tests.