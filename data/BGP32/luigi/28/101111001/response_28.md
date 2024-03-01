### Bug Explanation:
The bug in the `table_exists` function arises from the way it checks for the presence of the table in the `stdout` output from the `run_hive_cmd` function. The function incorrectly assumes that simply checking if the table name is present in `stdout` is sufficient, leading to incorrect results. The bug manifests when the function fails to correctly identify the table existence based on the `stdout` content.

### Bug Fix Strategy:
To fix the bug, we need to enhance the logic used to determine the existence of the table based on the `stdout` content. Instead of just checking if the table name is present, we should verify that the table name is a standalone name and not part of another string.

### Corrected Code:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table in stdout.split()

    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
```

By splitting the `stdout` content based on whitespaces, we can ensure that we are dealing with only the table names and not partial matches. This corrected version should now pass the failing tests and provide the expected results.