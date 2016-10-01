/* File Icons Builder
 * -------------------------------------------------------------------------- *
 * Developed with love & patience by Ihor Oleksandrov
 * -------------------------------------------------------------------------- */

'use strict';

/*
 * > Plugins
 */

var gulp = require('gulp');
var runSequence = require('run-sequence');
var conventionalChangelog = require('conventional-changelog');
var conventionalGithubReleaser = require('conventional-github-releaser');
var argv = require('yargs').argv;
var fs = require('fs');
var $ = require('gulp-load-plugins')();

/*
 * > Generate the Change Log
 */

gulp.task('changelog', function() {
  return conventionalChangelog({
    preset: 'angular',
    releaseCount: 0
  })
  .pipe(fs.createWriteStream('CHANGELOG.md'));
});

/*
 * > Bump Version
 */

gulp.task('bump-version', function() {
  return gulp.src('./package.json')
    .pipe($.if((Object.keys(argv).length === 2), $.bump()))
    .pipe($.if(argv.patch, $.bump()))
    .pipe($.if(argv.minor, $.bump({ type: 'minor' })))
    .pipe($.if(argv.major, $.bump({ type: 'major' })))
    .pipe(gulp.dest('./'));
});

/*
 * > Git
 */

gulp.task('commit-version', function() {
  return gulp.src('.')
    .pipe($.git.add())
    .pipe($.git.commit('chore: bump version number'));
});

gulp.task('commit-changelog', function() {
  return gulp.src('.')
    .pipe($.git.add())
    .pipe($.git.commit('chore: update change log'));
});

gulp.task('create-new-tag', function(cb) {
  var version = getPackageJsonVersion();

  $.git.tag('v' + version, 'version: ' + version, function (error) {
    if (error) {
      return cb(error);
    }
    $.git.push('origin', 'master', {args: '--tags'}, cb);
  });

  function getPackageJsonVersion() {
    return JSON.parse(fs.readFileSync('./package.json', 'utf8')).version;
  }
});

gulp.task('github-release', function(done) {
  conventionalGithubReleaser({
    type: 'oauth',
    token: process.env.CONVENTIONAL_GITHUB_RELEASER_TOKEN
  }, {
    preset: 'angular'
  }, done);
});

/*
 * > Release
 */

gulp.task('release', function(cb) {
  runSequence(
    'create-new-tag',
    'github-release',
    function (error) {
      if (error) {
        console.log('[release]'.bold.magenta + ' There was an issue releasing package:\n'.bold.red + error.message);
      } else {
        console.log('[release]'.bold.magenta + ' Finished successfully'.bold.green);
      }
      cb(error);
    }
  );
});


/*
 * > Default
 */

gulp.task('default', ['build']);
