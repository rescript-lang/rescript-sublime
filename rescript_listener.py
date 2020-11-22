import sublime_plugin

class RescriptListener(sublime_plugin.ViewEventListener):
  def on_pre_save(self):
    if self.view.settings().get('syntax').endswith('ReScript.sublime-syntax') and self.view.settings().get("rescript.formatOnSave"):
      self.view.run_command('rescript_format')

# def on_activated(self):
#   if self.view.settings().get('syntax') == packageName:
#     self.view.run_command('format', {"formatBuffer": False})

# def on_post_text_command(self, command_name, args):
#   if self.view.settings().get('syntax') == packageName:
#     # write syntax error -> save/format (get syntax error visible) -> undo
#     # re-render all syntax error diagnostics, otherwise you see stale diagnostics
#     if command_name == "undo":
#       self.view.run_command('format', {"formatBuffer": False})