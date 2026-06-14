// Dopo migrazione: nuova API
const newApi = require('new-api');

const client = newApi.createClient({ key: 'test' });
const user = client.getUserById(123);
const posts = client.getUserPosts(123);
console.log(user, posts);
