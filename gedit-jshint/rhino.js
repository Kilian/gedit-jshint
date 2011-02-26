/*jshint boss: true */
load(arguments[0].split("jshint.tmp")[0] + "jshint.js");

(function (args) {
    var name   = args[0],
        optstr = args[1], // arg1=val1,arg2=val2,...
        opts   = { rhino: true },
        input,
        errors = [];

    if (!name) {
        print('Usage: jshint.js file.js');
        quit(1);
    }

    if (optstr) {
        optstr.split(',').forEach(function (arg) {
            var o = arg.split('=');
            opts[o[0]] = o[1];
        });
    }

    input = readFile(name);
    if (!input) {
        print('jshint: Couldn\'t open file ' + name);
        quit(1);
    }

    if (!JSHINT(input, opts)) {
      if(JSHINT.errors){
          for(var i=0; i<JSHINT.errors.length; i++){
              if(JSHINT.errors[i]){
                  errors.push(
                    '{"reason"   :"' + escape(JSHINT.errors[i].reason) + '", ' +
                    ' "line"     :' + JSHINT.errors[i].line           + ', ' +
                    ' "character":' + JSHINT.errors[i].character   + '}\n');
              }
          }
          print('{"errors": [' + errors + ']}');
      }
    }

    quit(0);
}(arguments));

