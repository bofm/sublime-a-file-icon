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

then run task to build icon that you've added:

```bash
$ gulp
```
