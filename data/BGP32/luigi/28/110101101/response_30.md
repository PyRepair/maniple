### Bug Explanation
The bug in the `table_exists` function lies in how the stdout output is being checked for table existence. In the first `if` block, the function checks if the table name is in the stdout, which can cause false positives if the table name is a substring of another table name in the output. 
In the second `else` block, the function simply checks if the stdout is not empty but doesn't actually check if the specific table exists.

### Bug Fix Strategy
1. Update the first `if` block to split the stdout output by newlines and then check if the table name exists in the list of tables.
2. Alternatively, in the second `else` block, parse the stdout for the specific table name to ensure it exists in the output.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
        tables = stdout.split('\n')
        return table in tables
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition (%s)""" % (database, table, self.partition_spec(partition)))
    
        table_found = False
        if stdout:
            partitions = stdout.split('\n')
            for part in partitions:
                if table in part:
                    table_found = True
                    break
        
        return table_found
``` 

With this correction, the function now properly checks for the existence of the specified table in the Hive output, ensuring no false positives or negatives occur.