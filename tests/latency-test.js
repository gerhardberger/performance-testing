import http from 'k6/http';

export let options = {
  vus: __ENV.CONCURRENT,
  iterations: __ENV.TOTAL
};

export default function() {
  http.get(__ENV.TEST_URL);
};
