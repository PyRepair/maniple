The buggy function `table_exists` has a bug in the way it constructs the Hive query when the `partition` argument is not None. The issue lies in the formatting of the Hive query in the else block, where the `partition_spec` method is called to generate the partition specification.

The bug causes the Hive query to be malformed, leading to incorrect results or errors when trying to check for the existence of a table with a partition.

To fix the bug, we need to adjust the string formatting in the else block to correctly include the partition specification. Here is the corrected version of the `table_exists` function:

```python
    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
            return stdout and table in stdout
        else:
            partition_spec_str = ', '.join(['{}={}'.format(k, v) for k, v in partition.items()])
            stdout = run_hive_cmd('use {0}; show partitions {1} partition ({2});'.format(database, table, partition_spec_str))
    
            if stdout:
                return True
            else:
                return False
```

In this corrected version, we properly format the partition specification string by joining the key-value pairs from the partition dictionary. This ensures that the Hive query is constructed correctly when a partition is provided, fixing the bug.