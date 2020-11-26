import sublime
import sublime_plugin

import subprocess
import threading
import os
import sys
import queue
import time
import signal

from .rescript_utils import findBsConfigDirFromFilename, bsbPartialPath

# References to any existing ReScriptProcess() for a sublime.Window.id().
# For basic get and set operations, the dict is threadsafe.
_PROCS = {}

# References to any existing ReScriptPanel() for a sublime.Window.id().
# For basic get and set operations, the dict is threadsafe.
_PANELS = {}
_PANEL_LOCK = threading.Lock()

class ReScriptPanel():
	"""
	Holds a reference to an output panel used display the result of a ReScript build
	and provides synchronization features to ensure output is printed in proper order
	"""

	# A sublime.View object of the output panel being printed to
	panel = None

	# A queue.Queue() that holds all of the info to be written to the panel
	queue = None

	# A lock used to ensure only one printer is using the panel at any given time
	printerLock = None

	def __init__(self, window):
		"""
		:param window:
			A sublime.Window object the panel is contained in
		"""
		self.printerLock = threading.Lock()
		self.reinitialize(window)


	def reinitialize(self, window):
		"""
		Create a new panel and queue.

		:param window:
			A sublime.Window object the panel is contained in
		"""
		self.queue = queue.Queue()
		self.panel = window.create_output_panel("rescript_build")

	def write(self, txt):
		"""
		Queue data to be written to the output panel. Will be called from possible non UI threads.
		:param txt:
			A string to write to the output panel
		"""
		self.queue.put(txt)
		sublime.set_timeout(self.processQueue, 1)

	def processQueue(self):
		"""
		Callback to be run in the UI thread to actually write data to the output panel.
		"""
		try:
			while True:
				text = self.queue.get(block=False)
				self.panel.run_command('append', {'characters': text})

		except (queue.Empty):
			pass

class ReScriptCompilerProcess():
	# float unix timestamp of when the process was started
	startTime = -1

	# float unix timestamp of when the process ended
	endTime = -1

	projectRoot = ""

	# A subprocess.Popen() object of the running process
	proc = None

	# A queue.Queue object of output from the process
	output = None

	# The result of the process, a unicode string of "cancelled", "success" or "error"
	result = None

	# A threading.Lock() used to prevent the stdout and stderr handlers from both trying to perform process cleanup at the same time
	cleanupLock = None

	def __init__(self, task, projectRoot):
		"""
		:param task:
			Unicode string of "build", "clean" or "world". Defaults to "build" if absent.

		:param projectRoot:
			 A string representing the root of the project. Passed as cwd to the build process.
		"""
		# TODO: do we really need to store this? What use this it have?
		self.projectRoot = projectRoot

		args = [os.path.join(projectRoot, bsbPartialPath)]
		if task == "clean":
			args.append("-clean-world")
		elif task == "world":
			args.append("-make-world")

		startupinfo = None
		preexec_fn = None
		if sys.platform == 'win32':
			startupinfo = subprocess.STARTUPINFO()
			startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
		else:
			# On posix platforms we create a new process group by executing
			# os.setsid() after the fork before the go binary is executed. This
			# allows us to use os.killpg() to kill the whole process group.
			preexec_fn = os.setsid

		self.cleanupLock = threading.Lock()
		self.startTime = time.time()
		self.proc = subprocess.Popen(
			args,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			cwd=projectRoot,
			startupinfo=startupinfo,
			preexec_fn=preexec_fn
		)

		self.endTime = False

		self.output = queue.Queue()

		self.stdoutThread = threading.Thread(
			target=self.readOutput,
			args=(
				self.output,
				self.proc.stdout.fileno(),
				'stdout'
			)
		)
		self.stdoutThread.start()

		self.stderrThread = threading.Thread(
				target=self.readOutput,
				args=(
					self.output,
					self.proc.stderr.fileno(),
					'stderr'
				)
		)
		self.stderrThread.start()

		self.cleanupThread = threading.Thread(target=self.cleanup)
		self.cleanupThread.start()

	def wait():
		""" Blocks waiting for the subprocess to complete """
		self.cleanupThread.wait()

	def terminate(self):
		"""
		Terminates the subprocess
		"""
		self.cleanupLock.acquire()
		try:
			if not self.proc:
				return

			if sys.platform != 'win32':
				# On posix platforms we send SIGTERM to the whole process
				# group to ensure both go and the compiled temporary binary
				# are killed.
				os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)
			else:
				# On Windows, there is no API to get the child processes
				# of a process and send signals to them all. Attempted to use
				# startupinfo.dwFlags with CREATE_NEW_PROCESS_GROUP and then
				# calling self.proc.send_signal(signal.CTRL_BREAK_EVENT),
				# however that did not kill the temporary binary. taskkill is
				# part of Windows XP and newer, so we use that.
				startupinfo = subprocess.STARTUPINFO()
				startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
				killProc = subprocess.Popen(
					['taskkill', '/F', '/T', '/PID', str(self.proc.pid)],
					startupinfo=startupinfo
				)
				killProc.wait()

			self.result = 'cancelled'
			self.endTime = time.time()
			self.proc = None
		finally:
			self.cleanupLock.release()

	def readOutput(self, outputQueue, fileno, outputType):
		"""
		Callback to process output from stdout/stderr
		RUNS IN A THREAD
		:param outputQueue:
				The queue.Queue object to add the output to
		:param fileno:
				The fileno to read output from
		:param outputType:
				A unicode string of "stdout" or "stderr"
		"""
		while self.proc and self.proc.poll() is None:
			chunk = os.read(fileno, 32768)
			if len(chunk) == 0:
					break
			outputQueue.put((outputType, chunk.decode('utf-8')))

	def cleanup(self):
		"""
		Cleans up the subprocess and marks the state of self appropriately
		RUNS IN A THREAD
		"""

		self.stdoutThread.join()
		self.stderrThread.join()

		self.cleanupLock.acquire()
		try:
			if not self.proc:
					return
			# Get the returncode to prevent a zombie/defunct child process
			self.proc.wait()
			self.result = 'success' if self.proc.returncode == 0 else 'error'
			self.endTime = time.time()
			self.proc = None
		finally:
			self.cleanupLock.release()
			self.output.put(('eof', None))

class ReScriptProcessPrinter():
	"""
	Prints the result of a ReScript build process
	"""

	# The ReScriptCompilerProcess() object the printer is displaying output from
	proc = None

	# The ReScriptPanel() object the information is written to
	panel = None

	def __init__(self, proc, panel):
		"""
		:param proc:
			A ReScriptCompilerProcess() object

		:param panel:
			A ReScriptPanel() object to write information to
		"""

		self.proc = proc;
		self.panel = panel;

		self.thread = threading.Thread(
			target=self.run
		)
		self.thread.start()

	def run(self):
		"""
		Process a ReScriptCompilerProcess() output's queue, runs in a thread.
		"""
		self.panel.printerLock.acquire()

		try:
			while True:
				msgType, msg = self.proc.output.get()

				if msgType == "eof":
					break

				self.panel.write(msg)

			runtime = self.proc.endTime - self.proc.startTime
			self.panel.write(">>>> Finished compiling %0.3fs\n" % runtime)

		finally:
			self.panel.printerLock.release()


def storeProcess(window, proc):
	"""
	Sets the ReScriptBuildProcess() object associated with a sublime.Window
	:param window:
		A sublime.Window object
	:param proc:
		A ReScriptBuildProcess() object that is being run for the window
	"""
	_PROCS[window.id()] = proc

def fetchProcess(window):
	"""
	Returns the ReScriptBuildProcess() object associated with a sublime.Window
	:param window:
			A sublime.Window object
	:return:
			None or a ReScriptBuildProcess() object. The ReScriptBuildProcess() may or may not still be running.
	"""
	return _PROCS.get(window.id())

def fetchPanel(window):
	"""
	Returns the ReScriptPanel() object associated with a sublime.Window

	:param window:
		A sublime.Window object

	:return:
		A ReScriptPanel() object
	"""
	_PANEL_LOCK.acquire()
	try:
		if window.id() not in _PANELS:
			_PANELS[window.id()] = ReScriptPanel(window)
		return _PANELS.get(window.id())
	finally:
		_PANEL_LOCK.release()

def askUserIfCurrentBuildShouldBeCancelled(window):
	"""
	Check if a build is already running, and if so, allow the user to stop it,
	or cancel the new build
	:param window:
			A sublime.Window of the window the build is being run in
	:return:
			A boolean - if the new build should be abandoned
	"""
	proc = fetchProcess(window)
	if proc and not proc.endTime:
		message = "ReScript Build is in progress. Would you like to stop it?"
		if not sublime.ok_cancel_dialog(message, 'Stop Running Build'):
			return True

		proc.terminate()
		storeProcess(window, proc)

	return False

def killRunningBuild(window):
	proc = fetchProcess(window)
	if proc and not proc.endTime:
		proc.terminate()
	if proc is not None:
		storeProcess(window, None)

def runReScriptBuildProcess(task, window, projectRoot):
	"""
	Starts a ReScriptCompilerProcess and creates a ReScriptCompilerProcessPrinter() for it.

	:param task:
		Unicode string of "build", "clean" or "world".

	:param window:
		A sublime.Window object of the window to display the output panel in.

	:param projectRoot:
		A string representing the root of the project. Passed as cwd to the build process.
		
	:return:
		A ReScriptCompilerProcess() object
	"""
	panel = fetchPanel(window)
	proc = ReScriptCompilerProcess(task, projectRoot)

	# If no one is using the panel, reinitialize it
	if panel.printerLock.acquire(False):
		panel.reinitialize(window)
		panel.printerLock.release()

	ReScriptProcessPrinter(proc, panel)

	window.run_command('show_panel', {'panel': 'output.rescript_build'})

	return proc


# The name of the command needs to be the same thing as the name of the file that contains it.
# ~> `RescriptBuildCommand` translates to `rescript_build.py`
class RescriptBuildCommand(sublime_plugin.WindowCommand):
	"""
	 Command to run rescript compiler builds "bsb", "bsb -make-world" and "bsb -clean-world"
	"""

	def run(self, task="build", kill=False):
		"""
		Runs the "RescriptBuild" command - invoked by Sublime Text via the command palette or sublime.Window.run_command()

		:param task:
			Unicode string of "build", "clean" or "world". Defaults to "build" if absent.

		:param kill:
		  Boolean indicating whether the current running build should be cancelled.
		"""

		if kill is True:
			killRunningBuild(self.window)
			return

		if askUserIfCurrentBuildShouldBeCancelled(self.window):
			return

		# TODO: make this more robust, if there's no active view? -> extract_variables() project_path?
		projectRoot = findBsConfigDirFromFilename(self.window.active_view().file_name())

		proc = runReScriptBuildProcess(task, self.window, projectRoot)
		storeProcess(self.window, proc)

		self.window.active_view().set_status("lala", "yolo")

