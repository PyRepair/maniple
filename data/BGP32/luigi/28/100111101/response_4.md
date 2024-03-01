The bug in the provided function `table_exists` lies in how it handles the conditionals for checking if a table exists in Hive. The issue arises from how the function processes the output from the `run_hive_cmd` function and checks for the existence of the table.

### Problem:
1. The function incorrectly checks for the table existence by simply searching the table name in the stdout output. This method is not always reliable, especially when multiple tables are listed in the output.
2. The function does not handle case sensitivity for table names, leading to inconsistent results.

### Solution:
1. To solve the bug, we should parse the `stdout` to extract all table names before checking for the existence of the specific table.
2. Implement case insensitivity when comparing table names.

### Corrected Version:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables;'.format(database))
        tables = stdout.split('\n')

        return any(t.lower() == table.lower() for t in tables)
        
    else:
        stdout = run_hive_cmd("""use {0}; show partitions {1} partition
                              ({2})""".format(database, table, self.partition_spec(partition)))
        
        return bool(stdout)
```

By splitting the `stdout` by newlines and then checking if the lowercase table names match the provided table name, we ensure a more robust table existence check. Additionally, we handle the case sensitivity issue by lowercase all table names for comparison.