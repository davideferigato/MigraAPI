// Example JavaScript code with deprecated API
const oldApi = require('old-api');

function main() {
    const client = oldApi.createClient({ key: 'secret' });
    const user = oldApi.getUser(123);
    const posts = oldApi.fetchPosts(123);
    return { user, posts };
}

main();
