# rescript-sublime

The official Sublime Text plugin for ReScript.

## Prerequisite

- `>=0.0.9` requires `bs-platform >=8.3.0` installed locally in your project.
- `0.0.8` requires `bs-platform 8.2.0` installed locally in your project.

## Install

Get it from https://packagecontrol.io/packages/ReScript

## Features

- Syntax highlighting (`.res`, `.resi`).
- Formatting: Command Palette (`cmd-shift-p`) -> ReScript: Format File. caveats:
  - Currently requires the file to be part of a ReScript project, i.e. with a `bsconfig.json`.
  - Cannot be a temporary file.
- Snippets to ease a few syntaxes:
  - `external` features such as `@bs.module` and `@bs.val`
  - `try`, `for`, etc.

## Upcoming Features

- Syntax errors diagnosis (only after formatting).
- Formatting of temporary files
- Formatting of files outside of a ReScript project root
- Type diagnosis

## Config

- Command Palette -> UI: Select Color Scheme. Use **Mariana** for best effects (it'll be the new default Sublime Text theme!). Mariana colors tokens distinctively (and still pleasantly) enough for module and variant to be visually distinct despite both being capitalized. Gotta have accurate highlighting!

<!-- - Open this repo's `Default.sublime-settings`, put in the absolute path to the formatter exe in `optionalGlobalFormatter`. -->

<!-- To format: cmd-shift-r -->

## Develop

Thanks for your interest in contributing!

### Test Syntax

Docs at https://www.sublimetext.com/docs/3/syntax.html and https://www.sublimetext.com/docs/3/scope_naming.html

Tldr (documented in first link):

- Change `ReScript.sublime-syntax`
- Open `syntax_test.res`
- Command Palette -> Build With: Syntax Tests

For more grammar inspirations, check ST's own [JavaScript grammar](https://github.com/sublimehq/Packages/blob/2c66f1fdea0dbc74aaa3b1c2f904040e9c1aaefa/JavaScript/JavaScript.sublime-syntax).