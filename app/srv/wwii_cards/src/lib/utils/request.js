import { dev } from '$app/environment';

let domain = 'http://api.wwii-trading-cards.com'; // NOTE: ensure your /etc/hosts file on your local machine has {sub-domain}.wwii-trading-cards.com pointing at to 127.0.0.1
if (!dev) { domain = 'https://api.wwii-trading-cards.com'; }

async function handleRequest(url, opts) {
  return fetch(url, opts)
  .then((rsp) => {
    if (rsp.status == 401) {
      return rsp.status
    }

    if (!rsp.ok) {
      return // some sort of error that we can handle in the UI if request fails
    }

    return rsp.json()
  })
  .then((data) => {
    return data
  })
  .catch((error) => {
    return // some sort of error that the client can use in the UI that signifies bigger problems as bay
  })
}

export async function makeRequest(url, method, data=null) {
  let headers = {'Content-Type': 'application/json'};
  let opts = {method: method, headers: headers};
  if (data) opts['body'] = JSON.stringify(data);

  let rsp = await handleRequest(domain+url, opts);
  return rsp
}