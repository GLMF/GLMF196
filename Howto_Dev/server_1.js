yaml = require('js-yaml');
fs   = require('fs');

function syntaxError(msg) {
  console.error('Syntax error in configuration file : ' + msg);
  process.exit(2);
}

function readConfiguration() {
  try {
    return yaml.safeLoad(fs.readFileSync('config.yml', 'utf8'));
  } catch (e) {
    if (e.errno == -2) {
      console.error('Error : Can\'t open file ' + e.path);
      process.exit(1);
    }
    else if (e.name == 'YAMLException') {
      syntaxError(e.reason);
    }
    else {
      console.log(e);
      process.exit(3);
    }
  }
};

function validateConfiguration(config) {
  if (!('host' in config)) {
    syntaxError('host key MUST be present');
  }

  host = config['host'].split(':');
  if (host.length != 2) {
    syntaxError('host key format is url:port');
  }
  if (isNaN(parseInt(host[1], 10))) {
    syntaxError('in host key the port MUST be an integer');
  }

  for (key in config) {
    if (key == 'host') {
      continue;
    }
    if (!('type' in config[key])) {
      syntaxError(key + ' key has no \'type\' entry');
    } else {
      if (config[key]['type'] == 'list') {
        if (!('items' in config[key])) {
          syntaxError(' no \'items\' entry in list ' + key);
        }
      }
    }
    if (!('title' in config[key])) {
      syntaxError(key + ' key has no \'title\' entry');
    }

  }
};

config = readConfiguration();
validateConfiguration(config);
console.log(config)
