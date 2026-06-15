// Example JavaScript code with deprecated API
const oldApi = require('new-api');

function main() {
    const client = oldApi.createClient({ key: 'secret' });
    const user = newApi.getUserById(123);
    const posts = newApi.getUserPosts(123);
    return { user, posts };
}

main();
