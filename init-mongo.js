db = db.getSiblingDB('recon');

db.createCollection('domains');
db.createCollection('subdomains');


db.createUser({
  user: 'admin',
  pwd: 'admin123',
  roles: [
    { role: 'readWrite', db: 'recon' }
  ]
});
