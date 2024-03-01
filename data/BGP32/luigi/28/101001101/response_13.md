### Bug Explanation
The bug in the `table_exists` function lies in how the condition to check if a table exists in Hive is implemented. In the case where a partition is provided, the function constructs a Hive query incorrectly, leading to incorrect results. The bug stems from the incorrect construction of the query in this case.

### Bug Fix Strategy
To fix the bug, we need to ensure that the Hive query is constructed accurately, especially when dealing with partitions. The function should properly handle the partition specification when constructing the `show partitions` query.

### Corrected Function
```python
# The relative path of the corrected file: luigi/contrib/hive.py

def run_hive_cmd(hivecmd, check_return_code=True):
    # Please ignore the body of this function

class HiveCommandClient(HiveClient):
    def partition_spec(self, partition):
        # Please ignore the body of this function

    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
            return stdout and table in stdout
        else:
            partition_query = ', '.join(["{}='{}'".format(k, v) for k, v in partition.items()])
            stdout = run_hive_cmd("""use {0}; show partitions {1} partition
                                ({2});""".format(database, table, partition_query))
            return bool(stdout)
```

### Changes Made
1. Modified the query construction in the case where a partition is provided to correctly include the partition specification.
2. Used proper string formatting to build the Hive query with the partition details.
3. Used boolean conversion `bool(stdout)` instead of unnecessary if-else for returning True/False based on the presence of stdout.

By making these changes, the `table_exists` function should now work correctly for both cases with and without partitions.