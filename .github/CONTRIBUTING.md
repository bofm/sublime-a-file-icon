## Found an Issue?

If you have some problems, first search for a similar issue, and then report with [new one](https://github.com/oivva/zz-file-icons/issues) (don't forget to **follow the issue template**). Please read the [**known issues**](https://github.com/oivva/zz-file-icons#known-issues) before reporting a new one.

Don't forget to provide your environment details:

[![Environment](https://github.com/oivva/zz-file-icons/blob/dev/media/env.gif)](https://github.com/oivva/zz-file-icons/blob/dev/media/env.gif)

## Git Commit Guidelines

We have very precise rules over how our git commit messages can be formatted. This leads to more readable messages that are easy to follow when looking through the project history. But also, we use the git commit messages to generate the **Sublime File Icons** change log. 

We use [**Angular JS commit guidelines**](https://github.com/angular/angular.js/blob/master/CONTRIBUTING.md#-git-commit-guidelines) (except the scope notes, we don't need them).

## Building

This package uses a custom Gulp builder. If you want to add new icons you must install it first:

```bash
$ npm install
```

then run task to build an icon that you've added:

```bash
$ gulp
```

Build process consists of next parts:

* Build settings those are required for applying icons.
* Build SVG sources to dist icons.

## Want to add new icons?

If you want to add new icon please follow next steps:

1. Try to find an icon in the one of [these resources](https://github.com/oivva/zz-file-icons#icons). We always try to be pretty similar to [Atom File Icons](https://github.com/DanBrooker/file-icons) package. If you unable to find anything – add your own.
2. Add an example file that shows this icon to the `test` folder
3. Provide the icon in SVG format and put it to the `src/assets` directory
4. Add `icon` settings to the [src/icons.json](https://github.com/oivva/zz-file-icons/blob/dev/src/icons.json) file
5. Build it to test
6. It's recommended to add a link to the package which provides the syntax (see [PACKAGES.md](https://github.com/oivva/zz-file-icons/blob/dev/PACKAGES.md))

> All that you need to add are the SVG icon, its settings and the example file(s).

> All settings should be alphabetically sorted.

> Please do not change any other files, especially in `dist` folder.
> We build and provide distribution files once, right before the release.

### Icon

Requirements:

- The size should be `16x16` (`width`, `height` and `viewBox`)
- The color should be black via `i-color` class
- You should build and check if it looks good, if not make some tweaks to fit the pixel grid

Example:

[![ActionScript Icon](https://cdn.rawgit.com/oivva/zz-file-icons/dev/src/assets/file_type_actionscript.svg)](https://github.com/oivva/zz-file-icons/blob/dev/src/assets/file_type_actionscript.svg)

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <defs>
    <style>
      .i-color {
        fill: #000;
        fill-rule: evenodd;
      }
    </style>
  </defs>
  <path id="file_type_actionscript.svg" class="i-color" d="M11.174,9.341A2.586,2.586,0,1,1,9.345,6.176,2.586,2.586,0,0,1,11.174,9.341Zm1.389-1.713A6.757,6.757,0,0,1,12.6,4.2,2.639,2.639,0,0,0,7.5,2.879,6.749,6.749,0,0,1,5.958,5.7a6.41,6.41,0,0,1-3,1.766,2.641,2.641,0,1,0,1.368,5.1,6.349,6.349,0,0,1,3.309-.016,6.782,6.782,0,0,1,2.985,1.776,2.611,2.611,0,0,0,3.609-.108,2.639,2.639,0,0,0,.09-3.631A6.786,6.786,0,0,1,12.562,7.628Z" transform="translate(0 -1)"/>
</svg>
```

### Settings

Currently Sublime Text requires syntax definitions to apply the icons. It means that you need to have installed syntax package to see its icon. However we can abuse syntax definitions in order to provide different file icons to files with the same underlying syntax but different semantics (`Gulpfile.js`, `package.json` & etc.). That's why we provide two types of icons:

- syntax (apply via syntax scope)
- aliases (apply via syntax scope and syntax alias abuse)

For example:

```js
"file_type_git": {
  "color": "orange",
  "syntaxes": [
    {
      "name": "GitSyntaxes",
      "scope": "text.git"
    },
    {
      "name": "Git Misc Packages",
      "scope": "source.git"
    }
  ],
  "aliases": [
    {
      "name": "Shell Script (Git)",
      // `extensions` should be provided for aliases only
      "extensions": [
        "gitignore",
        "gitkeep"
      ],
      // It's the scope of the syntax which this alias inherits
      // `base` should be provided for aliases only
      "base": "source.shell",
      "scope": "source.shell.git"
    }
  ]
}
```

These settings will create three files after the building: 

* `dist\extensions\Shell Script (Git).sublime-settings`
* `dist\languages\Shell Script (Git).tmLanguage`
* `dist\preferences\file_type_git.tmPreferences`

Git icons will be applied to such files as `.gitconfig`, `.gitmodules` and etc when you install `GitSyntaxes` package. However this package doesn't provide syntaxes for `.gitignore` and `.gitkeep` that's why `zz File Icons` creates syntax alias to `Shell Script` to use its highlighting and git icon on these files.
