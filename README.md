# Sublime Text 3 Extended File Icons

This Sublime Text 3 package is the syntax aliases storage of the default syntaxes.

Its aim is to add support of such icons as NPM, Gulpfile, Font & etc.

## Get It

### Package Control (coming soon)

The easiest way to install is using [Package Control](https://packagecontrol.io/), where [it](https://packagecontrol.io/packages/File%20Icons%20Extended) is listed as `File Icons Extended`.

1. Open `Command Palette` using menu item `Tools → Command Palette...`
2. Choose `Package Control: Install Package`
3. Find `File Icons Extended` and hit `Enter`

### Download

1. [Download the .zip](https://github.com/oivva/file-icons-extended/releases)
2. Unzip and rename the folder to `File Icons Extended`
3. Copy the folder into `Packages` directory, which you can find using the menu item `Preferences → Browse Packages...`

### Clone

1. Go to `Packages` directory, which you can find using the menu item `Preferences → Browse Packages...`
2. Clone repository here: `git clone https://github.com/oivva/file-icons-extended.git "File Icons Extended"`


## Users

In some cases you can see that some icons from your current theme are missing or conflicted with other custom themes. 

> **You should remove other custom themes and use only the one which supports it or you can request support of this package from the developer of the theme that caused conflicts.**

[More details here →](https://forum.sublimetext.com/t/sublime-text-3-file-icons-in-sidebar/21134/4) 

## Theme Developers

If you are a theme developer and you want to have extended file icons support, you should:

* Remove all `.tmPreferences` files from your theme

* Check the name of the each icon that you provide with the theme. They should be the same as in [ICONS](ICONS.md). Also you can see the [BOXY THEME](https://github.com/oivva/boxy), it supports this package.

## Support

Themes that already have support of this package:

* [Boxy Theme](https://github.com/oivva/boxy)
