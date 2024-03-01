### Bug Explanation
The bug in the `table_exists` function lies in the condition for checking if the table exists in the output. The function checks if the table name is directly in the output, which may lead to incorrect results depending on the format of the output.

In Case 1, the function returns `True` because `'mytable'` is directly in the output `'OK'`.

In Case 2, the function returns `False` because `'MyTable'` is not directly in the output `'OK\nmytable'`.

### Bug Fix Strategy
To fix the bug, we should modify the condition for checking if the table exists to ensure that we are correctly parsing the output and not relying solely on a direct name match.

### Corrected Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables;'.format(database))
        tables = set(stdout.strip().split('\n'))
        return table in tables
    else:
        stdout = run_hive_cmd('use {0}; show partitions {1} partition ({2});'.format(database, table, self.partition_spec(partition)))
        return bool(stdout.strip())
``` 

With this correction, the function now properly parses the output to check whether the table exists based on the results of the query, providing a more robust and accurate evaluation.