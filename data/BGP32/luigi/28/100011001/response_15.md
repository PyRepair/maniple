### Cause of the Bug:
The bug in the `table_exists` function lies in the conditional check for the presence of the table name in the `stdout` variable. The current implementation checks if the `stdout` contains the exact table name, leading to failures in cases where the table name is present along with additional text.

#### Strategy for Fixing the Bug:
To fix the bug, the function should check if the table name is included in the `stdout` variable, rather than an exact match.

### Corrected Version of the Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables;'.format(database))
        
        return any(table == t.strip() for t in stdout.split('\n'))
    else:
        stdout = run_hive_cmd('use {0}; show partitions {1} partition ({2});'.format(database, table, self.partition_spec(partition)))
        
        return any(table == t.strip() for t in stdout.split('\n'))
``` 

In the corrected version, the function checks if the table name is included in each line of `stdout` by splitting the lines and comparing each table name with the desired table. This approach ensures that the function correctly identifies the table's existence regardless of the additional text in `stdout`.