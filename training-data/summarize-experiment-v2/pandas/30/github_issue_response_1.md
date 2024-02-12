Title: read_json with typ="series" results in timestamps/Exception

Description:
When using pd.read_json with typ="series" to convert a JSON list of bools, it results in a Pandas Series object with timestamps in older Pandas versions and raises a TypeError in version 1.0.0. This is inconsistent with the "frame" case and users would expect a Series of bools. This issue does not occur when convert_dates is set to False. The expected output is a Pandas Series of boolean values.