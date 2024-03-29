---
title: A look at Grunt.js
author: evan
categories: [Programming]
tagline: "Reflections on Grunt after TJ Krusinski's talk at Envy Labs"
---

Grunt is a task runner that allows you to automate repetitive tasks like compiling CoffeeScript and SASS, minifying sources, testing. It is a tool to support a Continusous Integration pipeline and to kick off tasks in less time.

Automation tasks themselves can "take on a life of their own":http://xkcd.com/1319/, but with Grunt there is a big return for little investment for tasks like linting and rebuilding your sources.

Envy Labs has hosted two different talks this past week and I got the chance to find out what  TJ Krusinski knows about Grunt.js. Installation via NPM is easy but Grunt itself is two packages: the cli tool that adds grunt to the command line, and the local Grunt task runner installation.

## Grunt Installation

First, install `grunt-cli` globally using npm

```
npm install -g grunt-cli
```

This grunt-cli package will run other installations installed alongside your application so that you can have multiple versions of Grunt on your machine.  Then, you can install Grunt alongside your project.

```
npm install grunt --save-dev
```

This installs Grunt and saves the grunt dependency in the dev section of your package.json file, which is what we want since we won't be running Grunt in production.

## Grunt Configuration

After installing our Grunt task runner, create a Gruntfile.js in your project root and add a bunch of tasks. The Gruntfile is a javascript module exporting a function that performs three operations on a Grunt object: initConfig(), loadNpmTasks(), or registerTask().


The method initConfig is where the details are. The object parameter is an object where you specify a task name, the options, and the files to operate on. The most useful task seems to be "watch", for which the options would look like this:

```js
grunt.initConfig({
  watch: {
    files: '*/*.md',
    tasks: /* task name or array of names */,
    options: { /* interrupt, atBegin, etc */ }
  }
});
```

Any tasks used are loaded using loadNpmTasks()

```js
grunt.loadNpmTasks('grunt-contrib-watch');
```

Finally, the last registration method give you control over executing tasks as well as specifying custom tasks that you write yourself.

```js
grunt.registerTask('default', ['watch']);
```

The "Grunt.js website":http://gruntjs.com/getting-started illustrates a custom task simply with this example

```js
module.exports = function(grunt) {

  // A very basic default task.
  grunt.registerTask('default', 'Log some stuff.', function() {
    grunt.log.write('Logging some stuff...').ok();
  });

};
```


With those Grunt basics we can set up Grunt to watch our source files use a few packages to live-reload a jekyll website when a page is updated.

## Blogging with Live Reload

The _watch_ task for Grunt has a LiveReload feature that starts a service that opens a connection to a webpage and prompts a refresh when a page contents change. With this feature, I can place my editor next to my browser and easily get feedback on the changes that I have made.  We can accomplish this with a properly configured gruntfile and a script in the header.

As a prerequisite, install "Jekyll":http://jekyllrb.com/. This depends on Ruby. On a Mac, installing Jekyll is as simple as:

```bash
npm install jekyll
```

Then, create a jekyll website and install grunt into the site root with the _watch_ and the _shell_ task runner packages.

```bash
jekyll install
npm install grunt --save-dev
npm install grunt-contrib-watch --save-dev
npm install grunt-shell --save-dev
```
A quick aside; Jekyll has a watch feature built-in that will rebuild the site when the contents change. To enable it you simply serve the Jekyll site with the watch flag.

```bash
jekyll serve -w // watch files
```

My Gruntfile is able to use the command line with the _shell_ task to interact with Jekyll to build and serve my blog. The watch task specifies the _files_ to watch using a glob to watch my markdown and textile files, and the _tasks_ array forces a new build and server restart when a change is made.

```js
module.exports = function(grunt) {
	grunt.initConfig({
		shell: {
			bld: {
				command: 'jekyll build'
			},
			srv: {
				command: 'jekyll serve'
			},
		},
		watch: {
			files: '_posts/*',
			tasks: ['shell:bld', 'shell:srv'],
			options: {
				interrupt: true,
				atBegin: true,
				livereload: 1337,
				debounceDelay: 1500
			}
		}
	})

	//load task dependencies
	grunt.loadNpmTasks('grunt-shell'); 	// package for running shell commands
	grunt.loadNpmTasks('grunt-contrib-watch'); // watch package

	//register default task
	grunt.registerTask('default', ['shell']);
}
```

There are some options on the _watch_ task to specify the timing and interruption of the watch. The _livereload_ option starts livereload service and the client side needs to load a script from this service, so we add a script tag to our header file.

```html
<script src="http://localhost:1337/livereload.js"></script>
```

This is how Grunt is able to communicate when a refresh is needed. Point the browser at http://localhost:1337/ and you will see a bit of json.

```js
{"tinylr":"Welcome","version":"0.0.4"}
```

I don't know the details of how LiveReload works, but it is working. Note, I had to introduce a debounceDelay of 1500 ms to prevent an error:

```bash
code. Fatal error: Maximum call stack size exceeded
```

## Summary

With "Grunt plugins":http://gruntjs.com/plugins, you can do some cool things with just a bit of configuration. Its probably worth your time to get to know a task runner like grunt, or other promising task runners like "Gulp":http://gulpjs.com/.
