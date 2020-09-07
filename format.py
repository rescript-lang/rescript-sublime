import sublime
import sublime_plugin
import subprocess
import re
import os
import tempfile
import pathlib
import platform

SETTINGS_PATH = 'Default.sublime-settings'

resExt = ".res"
resiExt = ".resi"
platformSystem = platform.system()
# rescript currently supports 4 platforms: darwin, linux, win32, freebsd.
# These also happen to be folder names for the location of the bsc binary.
# We're in python, so we're gonna translate python's output of system to
# nodejs'. Why don't we just use the binary in node_modules/.bin/bsc? Because
# that one's a nodejs wrapper, which has a startup cost. It makes it so that
# every time we call it for e.g. formatting, the result janks a little.
platformInNodeJS = "linux"
if platformSystem == "Darwin":
  platformInNodeJS = "darwin"
elif platformSystem == "Windows":
  platformInNodeJS = "win32"
elif platformSystem == "FreeBSD":
  platformInNodeJS = "freebsd"

bscPartialPath = os.path.join("node_modules", "bs-platform", platformInNodeJS, "bsc.exe")

def findBsConfigDirFromFilename(filename):
  currentDir = os.path.dirname(filename)
  while True:
    if os.path.exists(os.path.join(currentDir, "bsconfig.json")):
      return currentDir

    parentDir = os.path.dirname(currentDir)
    if parentDir == currentDir: # reached root
      return None

    currentDir = parentDir

def formatUsingValidBscPath(code, bscPath, isInterface):
    extension = resiExt if isInterface else resExt
    tmpobj = tempfile.NamedTemporaryFile(mode='w+', suffix=extension, encoding='utf-8', delete=False)
    tmpobj.write(code)
    tmpobj.close()
    proc = subprocess.Popen(
      [bscPath, "-color", "never", "-format", tmpobj.name],
      stderr=subprocess.PIPE,
      stdout=subprocess.PIPE,
    )
    stdout, stderr = proc.communicate()
    if proc.returncode == 0:
      return {
        "kind": "success",
        "result": stdout.decode(),
      }
    else:
      return {
        "kind": "error",
        "result": stderr.decode(),
      }

# Copied over from rescript-language-server's server.ts
def parseBsbOutputLocation(location):
  # example bsb output location:
  # 3:9
  # 3:5-8
  # 3:9-6:1

  # language-server position is 0-based. Ours is 1-based. Don't forget to convert
  # also, our end character is inclusive. Language-server's is exclusive
  isRange = location.find("-") >= 0
  if isRange:
    [from_, to] = location.split("-")
    [fromLine, fromChar] = from_.split(":")
    isSingleLine = to.find(":") >= 0
    [toLine, toChar] = to.split(":") if isSingleLine else [fromLine, to]
    return {
      "start": {"line": int(fromLine) - 1, "character": int(fromChar) - 1},
      "end": {"line": int(toLine) - 1, "character": int(toChar)},
    }
  else:
    [line, char] = location.split(":")
    start = {"line": int(line) - 1, "character": int(char)}
    return {
      "start": start,
      "end": start,
    }

# Copied over from rescript-language-server's server.ts
def parseBsbLogOutput(content):
  res = []
  lines = content.splitlines()
  for line in lines:
    if line.startswith("  We've found a bug for you!"):
      res.append([])
    elif line.startswith("  Warning number "):
      res.append([])
    elif line.startswith("  Syntax error!"):
      res.append([])
    elif re.match(r'^  [0-9]+ ', line):
      # code display. Swallow
      pass
    elif line.startswith("  "):
      res[len(res) - 1].append(line)

  ret = {}
  # map of file path to list of diagnosis
  for diagnosisLines in res:
    fileAndLocation, *diagnosisMessage = diagnosisLines
    lastSpace = fileAndLocation.rfind(" ")
    file = fileAndLocation[2:lastSpace]
    location = fileAndLocation[lastSpace:]
    if not file in ret:
      ret[file] = []
    cleanedUpDiagnosis = "\n".join([line[2:] for line in diagnosisMessage]).strip()
    ret[file].append({
      "range": parseBsbOutputLocation(location),
      "message": cleanedUpDiagnosis,
    })

  return ret

def findFormatter(view, filename):
  # filename = view.file_name()
  # globalFormatterExe = sublime.load_settings(SETTINGS_PATH).get('optionalGlobalFormatter')

  # if filename == None:
  #   # temp file
  #   if globalFormatterExe == None or not os.path.exists(globalFormatterExe):
  #     sublime.error_message(
  #       "This seems to be a temporary file, which we can format using a global formatter; " +
  #       "but the package's % s's optionalGlobalFormatter can't be found.\n"% SETTINGS_PATH +
  #       "Please make sure it exists."
  #     )
  #     return None
  #   else:
  #     return globalFormatterExe
  # else:
  bsconfigDir = findBsConfigDirFromFilename(filename)
  if bsconfigDir == None:
    # # bsconfig doesn't exist... gracefully degrade to using the optional global formatter
    # # might be bad to do this
    # if globalFormatterExe == None or not os.path.exists(globalFormatterExe):
    #   sublime.error_message(
    #     "Can't find bsconfig.json in current or parent directories. " +
    #     "We needed it to determine the location of the formatter.\n" +
    #     "We fell back to use the package's % s's optionalGlobalFormatter, "% SETTINGS_PATH +
    #     "but that also can't be found. Please make sure either a " +
    #     "bsconfig.json or the optionalGlobalFormatter exists."
    #   )
    #   return None
    # else:
    #   return globalFormatterExe
    sublime.error_message(
      "Can't find bsconfig.json in current or parent directories. " +
      "We needed it to determine the location of the formatter."
    )
    return None
  else:
    bscExe = os.path.join(bsconfigDir, bscPartialPath)
    if os.path.exists(bscExe):
      return bscExe
    else:
      sublime.error_message("Can't find bsc % s; it's needed for formatting."% bscExe)
      return None

class FormatCommand(sublime_plugin.TextCommand):
  def run(self, edit, formatBuffer=True):
    view = self.view
    view.erase_regions("syntaxerror")
    view.erase_phantoms("errns")

    currentBuffer = sublime.Region(0, view.size())
    code = view.substr(currentBuffer)

    filename = view.file_name()
    if filename == None:
      sublime.error_message(
        "Formatting is currently not supported for temporary files."
      )
      return

    bscExe = findFormatter(view, filename)
    if bscExe == None:
      return

    extension = pathlib.Path(filename).suffix
    formattedResult = formatUsingValidBscPath(
      code,
      bscExe,
      extension == resiExt
    )

    if formattedResult["kind"] == "success":
      view.replace(edit, currentBuffer, formattedResult["result"])
    else:
      regions = []
      phantoms = []

      filesAndErrors = parseBsbLogOutput(formattedResult["result"])
      for _file, diagnostics in filesAndErrors.items():
        for diagnostic in diagnostics:
          range_ = diagnostic["range"]
          message = diagnostic["message"]
          region = sublime.Region(
            view.text_point(range_["start"]["line"], range_["start"]["character"]),
            view.text_point(range_["end"]["line"], range_["end"]["character"]),
          )
          regions.append(region)
          html = '<body> <style> div.error {padding: 5px; border-radius: 8px;} </style> <div class="error">' + message +  '</div> </body>'
          view.add_phantom("errns", region, html, sublime.LAYOUT_BELOW)

      view.add_regions('syntaxerror', regions, 'invalid.illegal', 'dot', sublime.DRAW_NO_FILL)


packageName = 'ReScript'

# class NsListener(sublime_plugin.ViewEventListener):
#   def on_pre_save(self):
#     if self.view.settings().get('syntax') == packageName:
#       shouldFormat = sublime.load_settings(SETTINGS_PATH).get('formatOnSave')
#       self.view.run_command('format', {"formatBuffer": shouldFormat or False})

# def on_activated(self):
#   if self.view.settings().get('syntax') == packageName:
#     self.view.run_command('format', {"formatBuffer": False})

# def on_post_text_command(self, command_name, args):
#   if self.view.settings().get('syntax') == packageName:
#     # write syntax error -> save/format (get syntax error visible) -> undo
#     # re-render all syntax error diagnostics, otherwise you see stale diagnostics
#     if command_name == "undo":
#       self.view.run_command('format', {"formatBuffer": False})
