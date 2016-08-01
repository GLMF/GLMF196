var yaml = require('js-yaml');
var fs   = require('fs');
var http = require('http');
var journey = require('journey');
var redis = require('redis');
var colors = require('colors');

colors.setTheme({
  redis_ok: 'green',
  redis_warn: 'yellow',
  redis_debug : 'blue',
  redis_error: ['red', 'bold']
});


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

function createRouter(config, clientRedis) {
  var router = new(journey.Router);

  router.get('/ticketFormat').bind(function (req, res, params) {
    if (Object.keys(params).length !== 0) {
      sendJSON(res, {}, 400);
    } else {
      /*clientRedis.get('ticketFormat', function (err, reply) {
        if (err === null) {
          console.log(('[REDIS] Clé ticketFormat trouvée!').redis_ok);
          console.log(reply.redis_debug);
          sendJSON(res, reply);
        } else {
          console.warn(('[REDIS] La clé ticketFormat n\'existe pas').redis_warn);
        }
      });*/
      getRedis(clientRedis, 'ticketFormat', function (reply) {
        console.log(reply.redis_debug);
        sendJSON(res, reply);
      });
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

function connectRedis() {
  var client = redis.createClient();

  client.on('connect', function () {
    console.log('[REDIS] Connecté à la base Redis'.redis_ok);
  });
  client.on('error', function (err) {
    console.log(('[REDIS] Erreur : ' + err).redis_error);
  });
  
  return client;
}

function addRedis(client, key, object) {
  client.set(key, JSON.stringify(object), function (err, reply) {
    if (err !== null) {
      console.warn(('[REDIS] Erreur : ' + err).redis_error);
    } else {
      console.log('[REDIS] Objet ajouté à la base'.redis_ok);
      console.log(JSON.stringify(object).redis_debug);
    }
  });
}

function getRedis(client, key, callback) {
  client.get(key, function (err, reply) {
    if (err === null) {
      console.log(('[REDIS] Clé ' + key + ' trouvée!').redis_ok);
      console.log(reply.redis_debug);
      callback(reply);
    } else {
      console.warn(('[REDIS] La clé ' + key + ' n\'existe pas').redis_warn);
    }
  });
}

function startServer() {
  var config = readConfiguration();
  validateConfiguration(config);

  var host = config['host'].split(':');

  delete config['host'];

  var client = connectRedis();

client.del('ticketFormat', function(err, reply) {
  if (err === null) {
    console.log('La clé host a été supprimée');
  }
});

  client.exists('ticketFormat', function (err, reply) {
    if (reply === 1) {
      console.log('[REDIS] Format des tickets déjà présent dans la base'.redis_warn);
    } else {
      addRedis(client, 'ticketFormat', config);
      console.log('[REDIS] Format des tickets ajouté à la base'.redis_ok);
    }
  });

  var router = createRouter(config, client);

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
