var redis = require('redis')

var client = redis.createClient();

client.on('connect', function () {
  console.log('Connecté à la base Redis');
});
client.on('error', function (err) {
  console.log('Erreur : ' + err);
});

client.set('host', 'localhost:8080', function (err, reply) {
  if (err !== null) {
    console.warn('Erreur : ' + err);
  }
});

client.set('formatTicket', JSON.stringify({
  'categorie': {
    'type': 'list',
    'title': 'Catégorie',
    'items': [
      'espaces verts',
      'voirie',
      'bâtiments'
    ],
    // ...
  },
  // ...
  'description': {
    'type': 'text',
    'title': 'Description'
  },
  // ...
}), function (err, reply) {
  if (err !== null) {
    console.warn('Erreur : ' + err);
  }
});

client.exists('formatTicket', function (err, reply) {
  if (reply === 1) {
    console.log('Clé formatTicket trouvée');
  } else {
    console.log('La clé formatTicket n\'existe pas');
  }
});

client.get('host', function (err, reply) {
  if (err === null) {
    console.log('Valeur de host : ' + reply);
  }
});

client.get('formatTicket', function (err, reply) {
  if (err === null) {
    console.log('Valeur de formatTicket : ');
    console.log(JSON.parse(reply));
  }
});

client.del('host', function(err, reply) {
  if (err === null) {
    console.log('La clé host a été supprimée');
  }
});
