import sublime
import sublime_plugin
import os
import subprocess
import json
from urllib.parse import urlparse

from .rescript_utils import platformInNodeJS, findBsConfigDirFromFilename

binaryPath = os.path.join(
	os.path.dirname(os.path.abspath(__file__)),
	platformInNodeJS,
	"rescript-editor-support.exe"
)

def runDumpCommand(filename, line, column):
	command = [
		binaryPath,
		"dump",
		filename + ":" + str(line) + ":" + str(column)
	]

	proc = subprocess.Popen(
	    command,
	    stderr=subprocess.PIPE,
	    stdout=subprocess.PIPE,
	    cwd=findBsConfigDirFromFilename(filename)
	  )
	stdout, stderr = proc.communicate()
	return json.loads(stdout.decode().splitlines()[0])


class RescriptGotoDefinition(sublime_plugin.TextCommand):
	# TODO: multiple/zero cursors
	def run(self, edit):
		regions = self.view.sel()

		line, col = self.view.rowcol(regions[0].begin())

		cmdResult = runDumpCommand(self.view.file_name(), line, col)
		# [{'definition': {'range': {'end': {'character': 5, 'line': 26}, 'start': {'character': 4, 'line': 26}}}}]

		row = cmdResult[0]["definition"]["range"]["start"]["line"]
		col = cmdResult[0]["definition"]["range"]["start"]["character"]

		if cmdResult[0]["definition"].get('uri'):
			p = urlparse(cmdResult[0]["definition"].get('uri'))
			final_path = os.path.abspath(os.path.join(p.netloc, p.path))
			self.view.window().open_file(
					final_path + ":" + str(row + 1) + ":" + str(col + 1),
					sublime.ENCODED_POSITION
				)
		else:
			self.view.window().open_file(
					self.view.file_name() + ":" + str(row + 1) + ":" + str(col + 1),
					sublime.ENCODED_POSITION
				)
