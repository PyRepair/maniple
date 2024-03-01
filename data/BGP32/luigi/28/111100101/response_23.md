### Analysis:
1. The buggy function is `table_exists` inside the `HiveCommandClient` class in the `luigi.contrib.hive` module. 
2. The function uses the `run_hive_cmd` function and `partition_spec` method from the same class.
3. The bug seems to be in the conditional checks and string formatting of the SQL queries.
4. The bug causes incorrect evaluation of whether a table exists based on the output of the `run_hive_cmd` function.
5. The strategy for fixing the bug involves correcting the SQL queries and checking the stdout output more accurately.

### Correction:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
        return stdout and table in stdout
    else:
        partition_str = ' AND '.join(['{0} = "{1}"'.format(k, v) for k, v in partition.items()])
        stdout = run_hive_cmd('use {0}; show partitions {1} partition ({2});'.format(database, table, partition_str))
    
        return bool(stdout)
```

### Explanation:
I fixed the buggy function by correcting the query string formatting for table existence and partition checking. In the `else` block, I construct the partition condition string by iterating over the key-value pairs in the `partition` dictionary. Then, the query is properly formatted using this condition. Finally, the function returns a boolean value based on whether the `stdout` variable has any content.

This corrected version of the function should pass all the failing test cases provided.