var yaml = require('js-yaml');
var fs   = require('fs');
var http = require('http');
var journey = require('journey');


function sendJSON(res, json, code) {
  if (typeof code === 'undefined') {
    code = 200;
  }
  res.send(
    code,
    {'Content-Type': 'application/json'},
    json
  );
}

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

function createRouter(config) {
  var router = new(journey.Router);

  router.get('/ticketFormat').bind(function (req, res, params) {
    if (Object.keys(params).length !== 0) {
      sendJSON(res, {}, 400);
    } else {
      sendJSON(res, config);
    }
  });

  router.get('/tickets').bind(function (req, res, params) {
    if (Object.keys(params).length !== 0) {
      sendJSON(res, {}, 400);
    } else {
      sendJSON(res, {msg: 'WORK IN PROGRESS'});
    }
  });

  router.put('/newTicket').bind(function (req, res, params) {
    if (Object.keys(params).length === 0) {
      sendJSON(res, {}, 400);
    } else {
      sendJSON(res, {msg: 'WORK IN PROGRESS'});
    }
  });

  return router
}

function startServer() {
  var config = readConfiguration();
  validateConfiguration(config);

  var host = config['host'].split(':');

  var router = createRouter(config)

  var server = http.createServer(function (req, res) {
    var body = '';

    req.addListener('data', function (chunk) { 
      body += chunk;
    });
    req.addListener('end', function () {
      router.handle(req, body, function (result) {
        res.writeHead(result.status, result.headers);
        res.end(result.body);
      });
    });
  });
  server.listen(host[1]);

  console.log('Server running on ' + host[1]);
}


startServer();
