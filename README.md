> **Coming soon ...** 

![Logo][img-logo]

[![Release][img-release]][release]
[![Downloads][img-downloads]][downloads]
[![Make a donation at patreon.com][img-patreon]][patreon]

This package adds file specific icons to Sublime Text for improved visual grepping. It's heavily inspired by [Atom File Icons][atom-file-icons].

Its aims are:

* be a `tmPreferences` storage for UI themes those support file icons,
* provide file type icons for themes those don't (fully) support file icons.

If you have some problems, first search for a similar issue, and then report with [new one][new-issue]. Please read the [known issues][known-issues] before reporting a new one.

## Users

<!-- ### Getting Started -->

### Installation

#### Package Control ([coming soon][coming-soon])

The easiest way to install is using [Package Control][downloads], where it's listed as `zz File Icons`.

1. Open `Command Palette` using menu item `Tools → Command Palette...`
2. Choose `Package Control: Install Package`
3. Find `zz File Icons` and hit `Enter`

#### Download

1. [Download the .zip][release]
2. Unzip and rename the folder to `zz File Icons`
3. Copy the folder into `Packages` directory, which you can find using the menu item `Preferences → Browse Packages...`

> **Note:** Don't forget to restart Sublime Text after installing this package. 

### Customization

You can change the color, opacity level and size of the icons by modifying your user preferences file, which you can find using:

* menu item `Preferences → Package Settings → File Icons → Settings`,
* choose `File Icons: Settings` in `Command Palette`.

### Troubleshooting

If something going wrong try to:

1. Open `Command Palette` using menu item `Tools → Command Palette...`
2. Choose `File Icons: Clean Up`
3. Restart Sublime Text

#### Wrong Icons

Sublime Text file type icons use syntax scopes. That's why the icons for packages provided by the community require them to be installed.

See the list of [custom packages][packages] those you may need to install to see the right icon.

#### Missing Icons

In some cases you can see that some icons from your current theme are missing. You can:

- Request support of this package from the theme's developer
- Submit a request to add missing icons if the theme already supports it

[More details here →][details] 

#### Sublime Linter Setup

This package adds some syntax aliases which Sublime Linter doesn't recognize. Just update your Sublime Linter settings, e.g.:

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

Full list of the syntax aliases can be found [here][aliases].

## Developers

### Bring Support to Your Theme

If you are a theme developer and you want to have support of `zz File Icons`, you should:

* Remove all stuff related to the icon setup: `.tmPreferences`, `.sublime-settings` and `.tmLanguage` files
* Rename all your icons to match [these ones][icons]
* Add `.zz-file-icons` file to the root of your theme (this is how we check if the theme is **supported**)

Also see [MIGRATION.md][migration]. It contains a list of tasks those you have to do to support the next version of the `zz File Icons`.

### How It Works

In simple terms, `zz File Icons` does next steps:

1. Searches all installed and supported themes
2. Checks if themes those don't support it are already patched, if not
3. Patches them
    - Generates `<theme-name>.sublime-theme` files from [template][template]
    - Puts them into `dist/zpatches/` directory
4. For the themes those have support of it, it just provides `.tmPreferences` files by default (user can override icons provided by the theme via `"force_override": true`)
5. After restarting Sublime Text, the patched themes will be enhanced to use the icons provided by `zz File Icons`

It does these steps when:

- you've installed it,
- plugins loaded,
- you've changed its preferences.

The real process is just a little bit more complex to minimize hard drive I/O.

### Contributing

Want to contribute some code? Excellent! Read up on our [guidelines][contributing].

Together we will make **Sublime File Icons** even better than it is today!

## Resources

### Colors

Colors are from the [Boxy Theme][boxy-theme] icon color palette. They are bright because they should look good with the most themes. However you can change the color and the opacity level of all icons, see [customization][customization].

![Palette][img-palette]

### Icons

This package contains icons provided by:

- [Atom File Icons][atom-file-icons]
- [Boxy Theme][boxy-theme]
- [Devicons][devicons]
- [Font Awesome][font-awesome]
- [Font Mfizz][font-mfizz]
- [Icomoon][icomoon]
- [Octicons][octicons]

Source icons provided in SVG format (currently Sublime Text doesn't support it). We convert them to @1x, @2x and @3x PNG assets before each release via `gulp` task. 

Rasterized icons can be found in `dist/zpatches` folder.

## Change Log

See [CHANGELOG.md][changelog].

## Known Issues

This package requires you to restart Sublime Text for the applied icons to take effect when:

- you've installed it,
- you've changed its preferences,
- you've installed a new theme that should be patched.

## Share The Love

I've put a lot of time and effort into making **Sublime File Icons** awesome. If you love it, you can buy me a coffee. I promise it will be a good investment 😉

**Donate with:** [Patreon][patreon].

<!-- Resources -->

[atom-file-icons]: https://github.com/DanBrooker/file-icons
[boxy-theme]: https://github.com/oivva/st-boxy
[devicons]: http://vorillaz.github.io/devicons/#/main
[font-awesome]: http://fontawesome.io/
[font-mfizz]: http://fizzed.com/oss/font-mfizz
[icomoon]: https://icomoon.io/
[octicons]: https://octicons.github.com/

<!-- Misc -->

[aliases]: https://github.com/oivva/zz-file-icons/tree/dev/dist/languages
[bring-support]: https://github.com/oivva/zz-file-icons#bring-support-to-your-theme
[changelog]: https://github.com/oivva/zz-file-icons/blob/dev/CHANGELOG.md
[coming-soon]: https://github.com/wbond/package_control_channel/pull/5852
[contributing]: https://github.com/oivva/zz-file-icons/blob/dev/.github/CONTRIBUTING.md
[customization]: https://github.com/oivva/zz-file-icons#customization
[details]: https://forum.sublimetext.com/t/sublime-text-3-file-icons-in-sidebar/21134/4
[downloads]: https://packagecontrol.io/packages/File%20Icons%20Extended
[icons]: https://github.com/oivva/zz-file-icons/tree/dev/dist/zpatches/icons
[known-issues]: https://github.com/oivva/zz-file-icons#known-issues
[migration]: https://github.com/oivva/zz-file-icons/blob/dev/MIGRATION.md
[new-issue]: https://github.com/oivva/zz-file-icons/issues/new
[packages]: https://github.com/oivva/zz-file-icons/blob/dev/PACKAGES.md
[patreon]: https://www.patreon.com/oivva
[release]: https://github.com/oivva/zz-file-icons/releases
[template]: https://github.com/oivva/zz-file-icons/blob/dev/util/tpl.py

<!-- Assets -->

[img-downloads]: https://img.shields.io/packagecontrol/dt/File%20Icons%20Extended.svg?maxAge=3600&style=flat-square
[img-logo]: https://github.com/oivva/zz-file-icons/blob/dev/media/logo.png
[img-patreon]: https://img.shields.io/badge/donate-patreon-orange.svg?maxAge=2592000&style=flat-square
[img-release]: https://img.shields.io/github/release/oivva/zz-file-icons.svg?maxAge=86400&style=flat-square
[img-palette]: https://github.com/oivva/zz-file-icons/blob/dev/media/palette.png
