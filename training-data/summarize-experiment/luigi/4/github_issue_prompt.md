You have been provided with a GitHub issue that details a bug. Your task is to create a summary of it, aiming for a comprehensive and insightful output. This thorough analysis is intended to enhance the efficiency and effectiveness of the debugging process.

# A GitHub issue title for this bug
```text
Redshift COPY fails in luigi 2.7.1 when columns are not provided
```

## The associated detailed issue description
```text
Running Redshift COPY jobs with columns = None to prohibit table creation fails in luigi 2.7.1 with

TypeError: object of type 'NoneType' has no len()
The root cause seems to be https://github.com/spotify/luigi/pull/2245/files#diff-778ea3db4cccaf4de6564889c5eb670fR338

A possible solution would be to change the line to

if self.columns and len(self.columns) > 0:
unless I am missing some reason to explicitly ask only for len(self.columns).
```

