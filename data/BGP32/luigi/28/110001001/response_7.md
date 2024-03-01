### Explanation of the bug

The bug in the `table_exists` function lies in how it checks for the existence of a table in the given database. 

In the first part of the function, when `partition` is `None`, it runs a Hive command to `show tables` in the specified database and then checks if the `table` exists in the output. The bug here is that it directly checks if the `table` string is in `stdout`, which can lead to false positives (e.g., if the table name is a substring of another table name in the output).

In the second part of the function, when `partition` is provided, it runs a Hive command to `show partitions` for the specified `table` and `partition` values. However, the bug here is that it checks if the `stdout` is truthy, which can also lead to incorrect results, as the presence of partitions doesn't necessarily indicate the existence of the main table.

### Strategy to fix the bug

To fix the bug, we can modify the function to have more robust checks for table existence. Instead of directly checking if the table name is in the `stdout`, we can parse the output for exact match. Additionally, when checking for partitions, we should first verify if the main table exists and then proceed to check the partitions.

### Corrected version of the function

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd(f'use {database}; show tables;')
        tables = stdout.strip().split("\n")
        return table in tables
    else:
        table_exists_output = run_hive_cmd(f'use {database}; show tables;')
        if table not in table_exists_output:
            return False
        
        stdout = run_hive_cmd(f'use {database}; show partitions {table} partition ({self.partition_spec(partition)});')
        return bool(stdout)
``` 

In the corrected version:
- When `partition` is `None`, it shows all tables instead of using `LIKE`, and then checks for an exact match in the table names.
- When `partition` is provided, it first verifies if the `table` exists before checking for partitions.