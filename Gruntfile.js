const src = 'frontend/src/';
const dist = 'lol/static/lol/dist/';

const paths = {
	css: src + 'css/',
	js: src + 'js/',
	sprites: src + 'images/sprites/',
	build: src + 'build/',
};

const css = {
	files: paths.css + '**/*.less',
	starts_at: paths.css + 'screen.less',
	middle_file:  paths.build + 'unprocessed.css',
	dist:  dist + 'screen.css',
};

const sprites = {
	files: paths.sprites + '*.png',
	dist: paths.build + 'sprite.png',
	css_target: paths.build + 'sprite.css',
};

const js = {
	root: paths.js,
	files: paths.js + '**/*.js',
	starts_at: paths.js + 'main.js',
	dist: dist + 'script.js',
};

const html = {
	files: 'lol/templates/**/*.html',
};

module.exports = function(grunt) {
	grunt.initConfig({
		sprite: {
			all: {
				src: sprites.files,
				dest: sprites.dist,
				destCss: sprites.css_target,
			},
		},
		less: {
			options: {
				relativeUrls: true,
			},
			dev: {
				src: css.starts_at,
				dest: css.middle_file,
				options: {
					sourceMap: true,
					sourceMapFileInline: true,
				},
			},
			prod: {
				src: css.starts_at,
				dest: css.middle_file,
			},
		},
		postcss: {
			dev: {
				src: css.middle_file,
				dest: css.dist,
				options: {
					map: true,
					processors: [
						require('autoprefixer'),
						require('postcss-copy-assets')(),
					],
				}
			},
			prod: {
				src: css.middle_file,
				dest: css.dist,
				options: {
					processors: [
						require('autoprefixer'),
						require('postcss-copy-assets')(),
						require('cssnano'),
					],
				},
			},
		},
		clean: [css.middle_file],
		eslint: {
			dev: {
				src: js.root,
			},
			prod: {
				src: js.root,
				maxWarnings: 0,
			},
			options: {
				configFile: '.eslintrc.json'
			}
		},
		browserify: {
			options: {
				transform: [
					['babelify', {'presets': ['@babel/preset-env']}],
				]
			},
			dev: {
				src: js.starts_at,
				dest: js.dist,
				options: {
					watch: true,
					browserifyOptions: {
						debug: true,
						paths: [js.root],
					},
				},
			},
			prod: {
				src: js.starts_at,
				dest: js.dist,
				options: {
					browserifyOptions: {
						paths: [js.root],
					},
				},
			},
		},
		uglify: {
			prod: {
				src: js.dist,
				dest: js.dist,
			},
		},
		watch: {
			options: {
				atBegin: true,
			},
			sprite: {
				files: [sprites.files],
				options: {livereload: true},
				tasks: ['sprite', 'less:dev', 'postcss:dev'],
			},
			less: {
				files: css.files,
				tasks: ['less:dev', 'postcss:dev', 'clean'],
			},
			css: {
				files: css.dist,
				options: {livereload: true},
				tasks: [],
			},
			js: {
				files: js.files,
				tasks: ['eslint:dev'],
			},
			html: {
				files: html.files,
				options: {livereload: true},
				tasks: [],
			},
		}
	});

	grunt.loadNpmTasks('grunt-spritesmith');
	grunt.loadNpmTasks('grunt-contrib-less');
	grunt.loadNpmTasks('grunt-postcss');
	grunt.loadNpmTasks('grunt-contrib-clean');
	grunt.loadNpmTasks('grunt-contrib-watch');
	grunt.loadNpmTasks('grunt-eslint');
	grunt.loadNpmTasks('grunt-browserify');
	grunt.loadNpmTasks('grunt-contrib-uglify');

	grunt.registerTask('dev', [
		'browserify:dev',
		'watch',
	]);
	grunt.registerTask('prod', [
		'browserify:prod',
		'uglify:prod',
		'sprite',
		'less:dev',
		'postcss:prod',
		'clean',
		'eslint:prod',
	]);
};
