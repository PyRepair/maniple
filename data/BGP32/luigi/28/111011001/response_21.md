### Analysis
The `table_exists` function in the `HiveCommandClient` class is not correctly checking if a table exists in the specified database. The bug seems to be related to how the function checks for the existence of the table both with and without partitions. 

### Bug Explanation
1. In the first part of the function, when `partition` is `None`, the function constructs a Hive command to check if the table exists in the specified database. However, the comparison `table in stdout` is flawed because `stdout` is the result of a Hive command that might contain additional information beyond just the table name, leading to a false negative result.

2. In the second part of the function, when `partition` is not `None`, a similar issue arises. The constructed Hive command might return more information than just the table name, causing the function to incorrectly identify the existence of the table.

### Bug Fix Strategy
To fix the bug, we need to modify how the function checks for the existence of the table in both cases. Instead of relying on a substring comparison in the output of the Hive commands, we should parse the output to extract the relevant information (table name) and then check if the specified table exists based on that extracted information.

### Corrected Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        tables = [line.strip() for line in stdout.split('\n')]
        
        return table in tables
    else:
        partition_spec = self.partition_spec(partition)
        stdout = run_hive_cmd(f'use {database}; show partitions {table} partition ({partition_spec})')
        partitions = [line.split('=')[0].strip() for line in stdout.split('\n')]
        
        return partition_spec in partitions
```

### Changes Made
1. In the first part, the `stdout` is split by lines, and each line is stripped to get a list of tables. We then check if the `table` exists in this list.

2. In the second part, we extract the partition specification and split the `stdout` by lines to get a list of partitions. We then check if the extracted partition spec exists in this list.