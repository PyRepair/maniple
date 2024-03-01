## Bug Fix Strategy
The bug in the given `table_exists` function seems to lie in the conditional check for the existence of the table based on the output of the `run_hive_cmd` function. The current implementation is not covering all possible cases correctly, leading to failing tests.

To address this issue, we need to modify how we handle the response from the `run_hive_cmd` function in both cases where partition is None and when partition is not None. We should ensure that the function properly checks if the table exists in the output returned by `run_hive_cmd`.

## Bug-Free Function

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition (%s)""" % (database, table, self.partition_spec(partition)))
        return any(part_info.startswith(table) for part_info in stdout.split("\n"))
``` 

By modifying the condition to check for the presence of the given table in each line of the `stdout` response, we ensure that the function correctly identifies table existence in the Hive database. This approach covers all cases and should pass the failing tests.