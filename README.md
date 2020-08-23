# rescript-sublime

The official Sublime Text plugin for ReScript.

## Install

Get it from https://packagecontrol.io/packages/ReScript

## Features

- Highlighting
- Formatting: Command Palette (`cmd-shift-p`) -> ReScript: Format File

## Config

- Command Palette -> UI: Select Color Scheme. Use Mariana for best effects. Or try another one and tell us. Mariana colors tokens distinctively (and still pleasantly) enough for module and variant to be visually distinct despite both being capitalized. Gotta have accurate highlighting!

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
