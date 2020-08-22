# rescript-sublime

The official Sublime Text plugin for ReScript.

## Install

This is a developer preview, so the installation is manual for now.

- Clone repo locally.
- Cmd-shift-p -> Preferences: Browse Packages. Get the path where ST stores packages (e.g. `~/Library/Application Support/Sublime Text 3/Packages`).
- In the terminal, `ln -s /path/to/your/cloned/repo pathOfSTPackages`

## Features

- Highlighting
- Soon: formatting

## Config

- Cmd-shift-p -> UI: Select Color Scheme. Use Mariana for best effects. Or try another one and tell us. Mariana colors tokens distinctively (and still pleasantly) enough for module and variant to be visually distinct despite both being capitalized. Gotta have accurate highlighting!

<!-- - Open this repo's `Default.sublime-settings`, put in the absolute path to the formatter exe in `optionalGlobalFormatter`. -->

<!-- To format: cmd-shift-r -->

## Test Syntax

Docs at https://www.sublimetext.com/docs/3/syntax.html and https://www.sublimetext.com/docs/3/scope_naming.html

Tldr (documented in first link):

- Change `ReScript.sublime-syntax`
- Open `syntax_test.ml`
- Cmd-shift-p -> Build With: Syntax Tests
