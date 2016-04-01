'use strict';

/**
 * Load dependencies
 */
var config             = require('./gulp-config.json'),
    gulp               = require('gulp'),
    $                  = require('gulp-load-plugins')(),
    browserSync        = require('browser-sync').create(),
    reload             = browserSync.reload,
    argv               = require('yargs').argv,
    runSequence        = require('run-sequence'),
    webpackConfig      = require('./webpack-config.js')(argv.production),
    webpack            = require('webpack')(webpackConfig);


/*----------------------------------------*\
  TASKS
\*----------------------------------------*/

/**
 * Watching files for changes
 */
gulp.task('serve', function() {
  browserSync.init({
    proxy: 'rank-me.lo',
    notify: false,
    open: false
  });

  gulp.watch(config.src.sass, ['sass']);
  gulp.watch(config.src.javascript, ['webpack', reload]);
  gulp.watch(config.src.templates, reload);
});

/**
 * Compile Sass into CSS
 * Add vendor prefixes with Autoprefixer
 */
gulp.task('sass', function() {
  return gulp.src(config.src.sass)
    .pipe($.if(!argv.production, $.sourcemaps.init()))
    .pipe($.sass({
      outputStyle: 'compressed'
    }).on('error', $.sass.logError))
    .pipe($.autoprefixer(config.autoprefixer))
    .pipe($.if(!argv.production, $.sourcemaps.write('.')))
    .pipe(gulp.dest(config.dest.css))
    .pipe(browserSync.stream({match: '**/*.css'}));
});

/**
 * Optimize images
 */
gulp.task('images', function() {
  return gulp.src(config.src.images)
    .pipe($.imagemin({
      progressive: true,
      svgoPlugins: [{removeViewBox: false}]
    }))
    .pipe(gulp.dest(config.dest.images));
});

/**
 * Pack JavaScript modules
 */
gulp.task('webpack', function(done) {
  webpack.run(function(err, stats) {
    if(err) throw new $.util.PluginError('webpack', err);
    $.util.log('[webpack]', stats.toString());
    done();
  });
});

/**
 * Build for production
 */
gulp.task('build', ['webpack', 'sass']);

/**
 * Default task build, watch & serve
 */
gulp.task('default', function(cb) {
  runSequence('build', 'serve', cb);
});
