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

	if proc.returncode == 0:
	  return {
	    "kind": "success",
	    "result": json.loads(stdout.decode().splitlines()[0]),
	  }
	else:
		return {
		  "kind": "error",
		  "result": stderr.decode(),
		}

class RescriptGotoDefinition(sublime_plugin.TextCommand):
	def run(self, edit):
		selectedRegions = self.view.sel()

		# no cursors/selected regions (is this even possible?)
		if len(selectedRegions) < 1:
			return

		# if we have more than one cursor, we only jump to the first one
		line, col = self.view.rowcol(selectedRegions[0].begin())

		cmdOutput = runDumpCommand(self.view.file_name(), line, col)

		if cmdOutput["kind"] == "success":
			result = cmdOutput["result"]
			if len(result) < 1:
				# no goto definition results
				return

			definition = result[0]["definition"]

			row = definition["range"]["start"]["line"]
			col = definition["range"]["start"]["character"]

			# sublime.ENCODED_POSITION is 1-indexed
			encodedPosition = ":" + str(row + 1) + ":" + str(col + 1)

			# 'uri' is absent when jumping to a location in the same file
			filename = self.view.file_name()
			if definition.get('uri'):
				# parse file uri (i.e. file:///) into a normal file name
				p = urlparse(definition.get('uri'))
				filename = os.path.abspath(os.path.join(p.netloc, p.path))

			self.view.window().open_file(filename + encodedPosition, sublime.ENCODED_POSITION)