import platform
import os

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

bsbPartialPath = os.path.join("node_modules", "bs-platform", platformInNodeJS, "bsb.exe")

def findBsConfigDirFromFilename(filename):
  currentDir = os.path.dirname(filename)
  while True:
    if os.path.exists(os.path.join(currentDir, "bsconfig.json")):
      return currentDir

    parentDir = os.path.dirname(currentDir)
    if parentDir == currentDir: # reached root
      return None

    currentDir = parentDir