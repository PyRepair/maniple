### Bug Explanation:
The bug in the `table_exists` function is due to the incorrect logic in checking the presence of the table in the stdout. The function checks if the table name is present in the stdout string, but this logic is flawed as it can lead to false positives when a substring matches the table name but is not actually the table.

### Bug Fix Strategy:
To fix the bug, we need to modify the function to ensure that it correctly checks for the exact table name match in the stdout returned from the `run_hive_cmd` function.

### Corrected Function:
```python
# The relative path of the corrected file: luigi/contrib/hive.py

def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables;'.format(database))

        tables = stdout.split('\n')
        return table in tables
    else:
        stdout = run_hive_cmd('use {0}; show partitions {1} partition ({2})'.format(database, table, self.partition_spec(partition)))

        partitions = stdout.split('\n')
        return partition in partitions
```

By splitting the stdout output and checking for the exact match of the table or partition name in the list of tables or partitions, we ensure a more accurate check for table existence. This corrected function should now pass the failing test cases.