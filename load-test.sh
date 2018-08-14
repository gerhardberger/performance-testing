urls=(\
  'https://bsd9ocnpyk.execute-api.eu-central-1.amazonaws.com/dev/hello' \
  'https://us-central1-serverless-test-176319.cloudfunctions.net/hello' \
  'https://microsoft-azure-functions-hello-eu.azurewebsites.net/api/httpjs' \
)

levels=(\
  'low' \
  'medium' \
  # 'high'
)

names=(\
  'aws-lambda' \
  'google-cloud-functions' \
  'microsoft-azure-functions'
)

concurrents=(\
  10 \
  20 \
  30 \
)

totals=(\
  2000 \
  4000 \
  300 \
)

rm -rf results
mkdir results

docker-compose -f ./k6/docker-compose.yml up -d

level_index=0
for level in "${levels[@]}"
do
  outputdir=results/$level
  mkdir $outputdir

  concurrent=${concurrents[level_index]}
  total=${totals[level_index]}

  i=0
  echo "Level $level:"
  for url in "${urls[@]}"
  do
    docker exec -it k6_influxdb_1 influx -database 'k6' -execute 'drop series from http_req_duration;'

    echo "Measuring $url..."

    docker-compose -f ./k6/docker-compose.yml run \
      -v $PWD/tests:/tests \
      k6 run \
        -e TEST_URL=$url \
        -e CONCURRENT=$concurrent \
        -e TOTAL=$total \
        /tests/latency-test.js

    name=${names[i]}

    docker exec -it k6_influxdb_1 influx -database 'k6' -execute 'select * from http_req_duration;' -format json | \
      jq '[.results[0].series[0].values[] | { url: .[6], latency: .[7] }] | .[0].url as $url | { url: $url, latencies: [.[] | .latency] }' > $outputdir/$name.json

    i=$((i+1))
  done

  level_index=$((level_index+1))
done

docker-compose -f ./k6/docker-compose.yml down
