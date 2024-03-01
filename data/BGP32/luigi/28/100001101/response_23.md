### Bug Explanation
The bug in the `table_exists` function is due to the incorrect logic inside the function. In the first if condition, the function checks if the table exists by looking for the table name in the output of the `show tables` command. However, it does not consider case sensitivity, leading to a potential mismatch since table names in Hive are case-sensitive. In the second else condition, the function always returns `True` if the `stdout` is not empty, which might not accurately represent the existence of the table.

### Bug Fixing Strategy
To fix the bug:
1. Ensure that the table comparison is case-insensitive to correctly detect the existence of the table.
2. Improve the logic to accurately determine the table's existence based on the provided inputs.

### Corrected Version of the Function

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables;'.format(database))
        tables = stdout.split('\n')
        table_lower = table.lower()
        for t in tables:
            if t.lower() == table_lower:
                return True
        return False
    else:
        stdout = run_hive_cmd("use {0}; show partitions {1} partition ({2});".format(database, table, self.partition_spec(partition)))
        return bool(stdout)
``` 

In the corrected version, we split the output of `show tables` to compare table names in a case-insensitive manner. Additionally, the second part of the function now correctly returns `True` if `stdout` is not empty.