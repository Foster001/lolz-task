async def is_int(_):
	try:
		int(_)
		return True
	except:
		return False