var PORT = 8080;

var journey = require('journey');
var http = require('http');

var router = new(journey.Router);

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

router.get('/hello').bind(function (req, res, params) {
  if (params.name === undefined) {
    sendJSON(res, {}, 400);
  } else {
    sendJSON(res, {msg: 'Hello, ' + params.name + '!'});
  }
});

router.post('/hello').bind(function (req, res, params) {
  if (params.name === undefined) {
    sendJSON(res, {}, 400);
  } else {
    sendJSON(res, {msg: 'Hello (POST), ' + params.name + '!'});
  }
});

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
server.listen(PORT);

console.log('Server running on ' + PORT);
