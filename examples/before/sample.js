// Esempio di codice JavaScript con vecchia API
const oldApi = require('old-api');

const client = oldApi.createClient({ key: 'test' });
const user = client.getUser(123);
const posts = client.fetchPosts(123);
console.log(user, posts);
