### Bug Explanation
The bug in the `table_exists` function is caused by the incorrect comparison of the `table` name with the `stdout` output when checking if the table exists. The current implementation checks if the `table` name is directly in the `stdout` output, leading to false negatives in cases where the `table` appears in a new line after other content in the `stdout`.

### Bug Fix Strategy
To fix the bug, we need to modify the comparison logic when checking if the table exists in the `stdout`. We should split the `stdout` based on newlines and then check if the `table` name exists in any of the lines.

### Corrected Code
Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        
        return stdout and any(table == t.strip() for t in stdout.split('\n'))
    else:
        stdout = run_hive_cmd("use %s; show partitions %s partition (%s)" % (database, table, self.partition_spec(partition)))
        
        return bool(stdout)
```

By splitting the `stdout` on newlines and checking each line for the presence of the `table` name, we ensure that the function correctly identifies if the table exists in the database. This fix should pass the failing tests and meet the expected input/output values.