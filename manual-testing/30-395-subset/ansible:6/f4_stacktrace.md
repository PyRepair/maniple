The stacktraces are:

```text
lib/ansible/galaxy/collection.py:305: in from_path
    metadata=meta, files=files, skip=True)
lib/ansible/galaxy/collection.py:88: in __init__
    self.add_requirement(parent, requirement)
lib/ansible/galaxy/collection.py:120: in add_requirement
    new_versions = set(v for v in self.versions if self._meets_requirements(v, requirement, parent))
lib/ansible/galaxy/collection.py:120: in <genexpr>
    new_versions = set(v for v in self.versions if self._meets_requirements(v, requirement, parent))
```

```text
lib/ansible/galaxy/collection.py:305: in from_path
    metadata=meta, files=files, skip=True)
lib/ansible/galaxy/collection.py:88: in __init__
    self.add_requirement(parent, requirement)
lib/ansible/galaxy/collection.py:120: in add_requirement
    new_versions = set(v for v in self.versions if self._meets_requirements(v, requirement, parent))
lib/ansible/galaxy/collection.py:120: in <genexpr>
    new_versions = set(v for v in self.versions if self._meets_requirements(v, requirement, parent))
```
