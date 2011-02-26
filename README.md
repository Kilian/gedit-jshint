# JSHint plugin for Gedit
gedit-jshint is a plugin that allow you to check javascript files with the jshint syntax checker. For more infomation on JSHint, visit http://jshint.com

## INSTALLING:

To install extract the files to: /usr/lib/gedit-2/plugins/

## DEPENDENCIES:

It requires rhino and simplejson. On ubuntu you can get the packages by:

Ubuntu 10.04 and later:
    sudo apt-get install rhino python-simplejson

## USAGE:

The plugin should then appear in the Gedit plugins list under Edit > Preferences > Plugins.

Click Tools > JSHint Check or press <Shift><CTRL>+j to run it.

In the configuration dialog you can edit your Globals and your configuration. A default configuration is supplied: "/* curly: true, eqeqeq: true, forin: true, undef: true,*/"

