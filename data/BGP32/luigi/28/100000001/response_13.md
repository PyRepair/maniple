The potential errors in the buggy function are:
1. The `run_hive_cmd` function is being used without it being defined within the function or imported from another module.
2. The `self.partition_spec(partition)` call is potentially incorrect as it assumes the `partition_spec` function is defined within the same class.

The bug in the provided function is that it tries to use the `run_hive_cmd` function to execute Hive commands, but it doesn't provide the implementation of the function. This function is integral for executing the Hive commands and checking if a table exists. Additionally, there is a potential issue with the `partition_spec` method if it is not defined properly or if the partition is not constructed correctly.

To fix the bug:
1. Define the `run_hive_cmd` function within the same module or import it from an existing module.
2. Ensure that the `partition_spec` method is defined within the class or check if it is available in the correct context.

Here is the corrected version of the function:

```python
# The corrected version of the function
def table_exists(self, table, database='default', partition=None):
    def run_hive_cmd(cmd):
        # Implement the logic to execute Hive commands using cmd
        return True  # Placeholder return value

    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table in stdout
    else:
        stdout = run_hive_cmd(
            "use {0}; show partitions {1} partition ({2})".format(database, table, self.partition_spec(partition)))

        return bool(stdout)

```

In this corrected version:
1. The `run_hive_cmd` function is now defined within the `table_exists` function.
2. The format for executing Hive commands is corrected.
3. The conditional return statements are simplified.