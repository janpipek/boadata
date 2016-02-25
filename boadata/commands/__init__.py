def enable_ctrl_c():
	"""Enable Ctrl-C in the console."""
	import signal
	signal.signal(signal.SIGINT, signal.SIG_DFL)