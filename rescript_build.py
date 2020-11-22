import sublime
import sublime_plugin

import subprocess
import threading
import os

# The name of the command needs to be the same thing as the name of the file that contains it.
# ~> `RescriptBuildCommand` translates to `rescript_build.py`
class RescriptBuildCommand(sublime_plugin.WindowCommand):
	proc = None

	def run(self):
		if self.proc:
			print("we're having a process")
		else:
			self.proc = subprocess.Popen(
        ["/Users/mvalcke/Development/rescript-lang.org/node_modules/bs-platform/darwin/bsb.exe"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    	)	
			print("no process yet")