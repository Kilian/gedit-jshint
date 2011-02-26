# JSHint plugin for Gedit
gedit-jshint is a plugin that allow you to check javascript files with the jshint syntax checker.
For more infomation on JSHint, visit [jshint.com](http://jshint.com).
It is based on the [gedit-jslint plugin](https://github.com/Kilian/gedit-jslint]) by Caolan McMahon (2008) and Kilian Valkhof (2009 - 2011)

## INSTALLING:

To install extract the files to: /usr/lib/gedit-2/plugins/

## DEPENDENCIES:

It requires rhino and simplejson. On Ubuntu 10.04 and later you can get the packages with the following command:
    sudo apt-get install rhino python-simplejson

On earlier versions of Ubuntu, and on certain other Linux systems, you might need "spidermonkey" instead of "rhino".

## USAGE:

The plugin should then appear in the Gedit plugins list under Edit > Preferences > Plugins.

Click Tools > JSHint Check or press Shift+Ctrl+j to run it.

In the configuration dialog you can edit your globals and your configuration. A default configuration is supplied:
    /* curly: true, eqeqeq: true, forin: true, undef: true,*/
By default, no globals are defined.

