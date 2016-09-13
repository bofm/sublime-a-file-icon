# Sublime Text 3 Extended File Icons

[![Release][img-release]][release]
[![Downloads][img-downloads]][downloads]
[![Make a donation at patreon.com][img-patreon]][patreon]

This package is a storage of syntax aliases to the [Default Sublime Text Packages][default-packages].

Its aim is to add support of such icons as NPM, Gulpfile, Font & etc.

## Get It

### Package Control

The easiest way to install is using [Package Control][downloads], where it's listed as `File Icons Extended`.

1. Open `Command Palette` using menu item `Tools → Command Palette...`
2. Choose `Package Control: Install Package`
3. Find `File Icons Extended` and hit `Enter`

### Download

1. [Download the .zip][release]
2. Unzip and rename the folder to `File Icons Extended`
3. Copy the folder into `Packages` directory, which you can find using the menu item `Preferences → Browse Packages...`

## Users

### Icons

In some cases you can see that some icons from your current theme are missing or conflicted with other custom themes. 

> **You should remove other custom themes and use only the one which supports it or you can request support of this package from the developer of the theme that caused conflicts.**

[More details here →][details] 

### Sublime Linter

This package adds some syntax aliases which Sublime Linter doesn't recognize. Just update your Sublime Linter settings:

```js
  "syntax_map": {
    "html (django)": "html",
    "html (rails)": "html",
    "html 5": "html",
    "javascript (babel)": "javascript",
    "javascript (gruntfile)": "javascript",
    "javascript (gulpfile)": "javascript",
    "json (bower)": "json",
    "json (npm)": "json",
    "json (settings)": "json",
    "magicpython": "python",
    "php": "html",
    "python django": "python",
    "pythonimproved": "python"
  },
```

## Theme Developers

If you are a theme developer and you want to have extended file icons support, you should:

* Remove [these][preferences] syntax alias `.tmPreferences` files from your theme
* Check the name of the each icon that you provide with the theme. They should be the same as in [ICONS.md][icons].

## Support

Themes those already have support of this package:

* [Boxy Theme][boxy-theme]
* [Material Theme][material-theme]

<!-- Themes -->

[boxy-theme]: https://github.com/oivva/st-boxy
[material-theme]: https://github.com/equinusocio/material-theme

<!-- Misc -->

[default-packages]: https://github.com/sublimehq/Packages
[details]: https://forum.sublimetext.com/t/sublime-text-3-file-icons-in-sidebar/21134/4
[downloads]: https://packagecontrol.io/packages/File%20Icons%20Extended
[icons]: ICONS.md
[patreon]: https://www.patreon.com/oivva
[preferences]: /preferences
[release]: https://github.com/oivva/st-file-icons-extended/releases

<!-- Assets -->

[img-downloads]: https://img.shields.io/packagecontrol/dt/File%20Icons%20Extended.svg?maxAge=3600&style=flat-square
[img-patreon]: https://img.shields.io/badge/donate-patreon-orange.svg?maxAge=2592000&style=flat-square
[img-release]: https://img.shields.io/github/release/oivva/st-file-icons-extended.svg?maxAge=86400&style=flat-square
