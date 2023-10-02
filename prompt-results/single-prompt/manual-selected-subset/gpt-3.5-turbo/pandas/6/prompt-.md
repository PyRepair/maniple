You need to fix a bug in a python code snippet.

The buggy source code is following, and you should follow all specifications in comment if there exists comment:

	def is_in_obj(gpr) -> bool:
		if not hasattr(gpr, "name"):
			return False
		try:
			return gpr is obj[gpr.name]
		except (KeyError, IndexError):
			return False



You need to provide a drop-in replacement, with 'minimum changes to source code' that 'pass failed test' while 'won't affect other already passed tests'. And the fixed patch can be directly used in original project.