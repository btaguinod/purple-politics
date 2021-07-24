let config = {}

let localDomains = ["localhost", "127.0.0.1", ""]
let isLocal = localDomains.includes(window.location.hostname)
config.backendUrl = isLocal ? 'http://127.0.0.1:5000/' : 'https://purple-politics.herokuapp.com'

export default config