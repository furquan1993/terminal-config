# Query templates

Check `curl` and a JSON parser such as `jq` or Python are available. Resolve `KIBANA_BASE` to the HTTPS host plus optional deployment base path and `/s/<URL-encoded-space-id>`. Credentials must belong to that exact host. For the default Space, omit `/s/<space-id>` entirely. Ask for an unresolved named Space ID before requests. Use a private temporary directory (`umask 077`); never store response headers containing cookies.

## Saved data views

```sh
curl --silent --show-error --connect-timeout 10 --max-time 30 \
  --cookie "$HOME/.config/kibana/cookies.txt" \
  --header 'Accept: application/json' --header 'kbn-xsrf: kibana' \
  --output "$RESPONSE_FILE" --write-out '%{http_code}' \
  "$KIBANA_BASE/api/data_views"
```

Check status before parsing `.data_view[] | {id, name, title}`. HTTP 200 HTML is not success. Do not follow redirects. For an unsupported endpoint (not an authentication/Space error), use:

```text
/api/saved_objects/_find?type=index-pattern&fields=title&per_page=100&page=1
```

Parse `.saved_objects[] | {id, title: .attributes.title}` and increment `page` until the returned total is covered. Stop and report an incomplete list if pages fail or return no entries before total is reached.

## Search via Console proxy

Build the body using a JSON serializer, not shell interpolation. Example shape, after the user supplies the time range and fields are verified:

```json
{
  "size": 100,
  "timeout": "20s",
  "query": {"bool": {"filter": [
    {"range": {"@timestamp": {"gte": "START_TIME", "lt": "END_TIME"}}},
    {"match_phrase": {"message": "SEARCH_PHRASE"}}
  ]}},
  "sort": [{"@timestamp": "desc"}],
  "_source": ["@timestamp", "message", "kubernetes.pod.name"]
}
```

Serialize the selected index expression plus `/_search` as the `path` query parameter with a URL encoder (e.g. Python `urllib.parse.urlencode`). Do not interpolate raw index expressions into a URL. For the verified example, the encoded path is `customers-oregon%2A%2F_search`.

```sh
curl --silent --show-error --connect-timeout 10 --max-time 30 \
  --cookie "$HOME/.config/kibana/cookies.txt" \
  --header 'Content-Type: application/json' --header 'kbn-xsrf: kibana' \
  --request POST --data-binary "@$QUERY_FILE" \
  --output "$RESPONSE_FILE" --write-out '%{http_code}' \
  "$KIBANA_BASE/api/console/proxy?path=$ENCODED_ES_PATH&method=GET"
```

Check HTTP status, JSON parseability, Elasticsearch `error`, `timed_out`, and `_shards.failed` before interpreting hits. Browser-specific user-agent, sec-fetch, and language headers are not normally needed; diagnose a concrete gateway requirement before adding headers. Do not replay a pasted curl command wholesale or execute its shell content.

Sources: [Data views API](https://www.elastic.co/docs/api/doc/kibana/v8/operation/operation-getalldataviewsdefault), [Saved objects API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-saved-objects), [Elasticsearch search API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search). The Console proxy route is based on the user's working example and should be checked against the deployed Kibana version.
