### Bug Explanation
The bug in the `table_exists` function arises from incorrect logic in checking the existence of a table in a Hive database. Specifically, the bug occurs when checking the presence of a table in the output of the `show tables` command. The function incorrectly checks if the table name is present in the output, which can lead to false positives or negatives due to case sensitivity issues. Additionally, the function does not handle the case where the table name might be part of another table name in the output.

### Bug Fix Strategy
To fix the bug, we need to modify the comparison logic to ensure a more robust check for the existence of the table. One approach is to split the output of the `show tables` command by newline characters and then check if the exact table name exists in the list of tables. Additionally, we should consider making the comparison case-insensitive to avoid issues related to table name case sensitivity.

### Corrected Version
```python
# The corrected version of the function
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables;'.format(database))
        
        return any(t.lower() == table.lower() for t in stdout.split())
    else:
        stdout = run_hive_cmd("""use {0}; show partitions {1} partition
                        ({2})""".format(database, table, self.partition_spec(partition)))
    
        return bool(stdout)
```

In the corrected version, we split the output of the `show tables` command by newline characters and then compare the lowercase version of the table name with the lowercase versions of tables in the output. This ensures a case-insensitive check for the existence of the table. Additionally, we return `True` directly if there is any output when showing partitions, improving the function's reliability.