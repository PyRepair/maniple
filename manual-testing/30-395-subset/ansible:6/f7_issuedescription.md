The issue description is:

When installing a collection it scans existing collections at the path specified and if a collection has a MANIFEST.json file with a version set to an empty string it will fail with

```text
ERROR! Unexpected Exception, this is probably a bug: 'LooseVersion' object has no attribute 'version'
the full traceback was:                                                                                  
                                                                                                         
Traceback (most recent call last):                                                                       
  File "/home/jborean/dev/ansible/bin/ansible-galaxy", line 123, in <module>                 
    exit_code = cli.run()                                                                                
  File "/home/jborean/dev/ansible/lib/ansible/cli/galaxy.py", line 387, in run       
    context.CLIARGS['func']()                    
  File "/home/jborean/dev/ansible/lib/ansible/cli/galaxy.py", line 848, in execute_install                                                                                                                         
    no_deps, force, force_deps)                                                                          
  File "/home/jborean/dev/ansible/lib/ansible/galaxy/collection.py", line 435, in install_collections    
    existing_collections = find_existing_collections(output_path)                    
  File "/home/jborean/dev/ansible/lib/ansible/galaxy/collection.py", line 792, in find_existing_collections
    req = CollectionRequirement.from_path(b_collection_path, False)                                                                                                                                                
  File "/home/jborean/dev/ansible/lib/ansible/galaxy/collection.py", line 309, in from_path
    metadata=meta, files=files, skip=True)                                                               
  File "/home/jborean/dev/ansible/lib/ansible/galaxy/collection.py", line 88, in __init__                
    self.add_requirement(parent, requirement)                                                            
  File "/home/jborean/dev/ansible/lib/ansible/galaxy/collection.py", line 120, in add_requirement
    new_versions = set(v for v in self.versions if self._meets_requirements(v, requirement, parent))
  File "/home/jborean/dev/ansible/lib/ansible/galaxy/collection.py", line 120, in <genexpr> 
    new_versions = set(v for v in self.versions if self._meets_requirements(v, requirement, parent))
  File "/home/jborean/dev/ansible/lib/ansible/galaxy/collection.py", line 233, in _meets_requirements    
    if not op(LooseVersion(version), LooseVersion(requirement)):                             
  File "/usr/local/lib/python3.7/distutils/version.py", line 46, in __eq__                                                                                                                                         
    c = self._cmp(other)                  
  File "/usr/local/lib/python3.7/distutils/version.py", line 335, in _cmp            
    if self.version == other.version:                                                                                                                                                                              
AttributeError: 'LooseVersion' object has no attribute 'version'  
```
