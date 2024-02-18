Class docstring: The `HiveCommandClient` class uses `hive` invocations to find information.

`def run_hive_cmd(hivecmd, check_return_code=True)`: This function is called within the `table_exists` function to execute a Hive command and return the standard output.

`def partition_spec(self, partition)`: This function is also called within the `table_exists` function to format the partition specification before running the Hive command.

`def table_exists(self, table, database='default', partition=None)`: This function checks whether a table exists in a given database. It calls `run_hive_cmd` to execute Hive commands and uses `partition_spec` to format partition specifications, if provided.