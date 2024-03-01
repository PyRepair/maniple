### Bug Explanation
The bug in the `table_exists` function is related to the condition checking for the existence of the table. When the function checks for the presence of the table in the output received from `run_hive_cmd`, it only checks if the table name is present in the string without considering other content. This results in incorrect evaluations of table existence, especially when the table name appears as part of a larger output string. 

### Bug Location
The buggy section of the function is this line:
```python
return stdout and table in stdout
```
This line only checks if the table name is present in the entire `stdout` string. It should be modified to ensure that the match is on a separate line for accurate evaluation.

### Fix Strategy
To fix the bug, we need to modify the condition where we check for the presence of the table name in the `stdout` string. The table name should be checked for its existence on a separate line in the `stdout`. This will make the evaluation accurate regardless of the context in which the table name appears in the output.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
        return stdout and '\n' + table + '\n' in stdout
    else:
        stdout = run_hive_cmd(
            """use %s; show partitions %s partition (%s)""" % (database, table, self.partition_spec(partition)))
    
        return bool(stdout)
```

In the corrected version, we check if `'\n' + table + '\n'` exists in the output string `stdout`. This ensures that we are checking for the table name on a separate line, making the evaluation more accurate. Additionally, I have simplified the return statements for better readability.