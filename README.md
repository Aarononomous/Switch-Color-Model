# Switch CSS Color Model

A plugin for Sublime Text. Rapidly and correctly switch between CSS color models (hex, rgb(), and hsl()).

N.b.: this doesn't work with rgba() and hsla() values with an alpha level that isn't 1.

## Usage

### Via the Context Menu

Right-click on the selection you want to switch and choose "Switch CSS Color Model."

### Via the Command Palette

Within the command palette, "Switch CSS Color Model."

### With a Keyboard Shortcut

You can set up a keyboard shortcut to run the command by going to **Sublime Text > Preferences > Key Bindings &ndash; User** and adding your shortcut with the `switch_color_model` command. Here are my recommendations, but you should check the User and Default key bindings to make sure that you don't overwrite another shortcut.

Mac

```
[
  { "keys" : ["ctrl+shift+c"], "command": "switch_color_model" }
]
```

Windows/Linux

```
[
  { "keys" : ["ctrl+alt+shift+c"], "command": "switch_color_model" }
]
```

### Modifying Settings

TODO: modification instructions

## Installation

### Manually

Browse to ~/Library/Application Support/Sublime Text 3/Packages and unzip the download inside.

## Bugs

Please let me know! Email [mailto](hi@aaron-jacobson.com) or submit an issue through GitHub.

## License

MIT &copy; Aaron Jacobson