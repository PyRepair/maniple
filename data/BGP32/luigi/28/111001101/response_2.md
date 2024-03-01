### Bug Explanation
The bug in the `table_exists` function is due to the comparison `table in stdout` where `table` is being compared to values in `stdout`. This comparison will always return `False` because `table` is expected to match exactly with a line in `stdout`, which is not the case when `stdout` contains multiple lines separated by newline characters.

### Bug Fix Strategy
To fix this bug, we need to split the `stdout` variable by newline characters and then check if any of the lines match the `table` we are looking for.

### Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
        return stdout and table in stdout.split('\n')
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                          (%s)""" % (database, table, self.partition_spec(partition)))
    
        return bool(stdout)
``` 

This corrected version splits the `stdout` variable by newline characters before comparing `table in stdout`. Additionally, it directly returns the boolean value of `stdout` in the `else` case for better clarity.