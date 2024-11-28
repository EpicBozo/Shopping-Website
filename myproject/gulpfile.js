const gulp = require('gulp');
const browserSync = require('browser-sync').create();

// Static server
gulp.task('serve', function() {
    browserSync.init({
        proxy: "127.0.0.1:8000" // Your Django server address
    });

    // Live updates the home page
    gulp.watch("myproject/myapp/templates/myapp/index.html").on('change', browserSync.reload);
    gulp.watch("myproject/myapp/static/css/style.css").on('change', browserSync.reload);

    // Live updates the results page
    gulp.watch("myproject/myapp/templates/myapp/results.html").on('change', browserSync.reload);
    gulp.watch("myproject/myapp/static/css/results.css").on('change', browserSync.reload);

});

gulp.task('default', gulp.series('serve'));
