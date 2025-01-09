# Google Trends

- can get top overall/related topics & queries for
    given time range + location + category + topic/query
    - up to (and usually) 25 each
- can also get "rising" topics & queries
    - but unclear how to know their popularity
- can get name + relative interest + href to Google Trends page for
    each topic/query entry
- [ ] Google Trends block request from browser in incognito mode 💀
    - can use BigQuery to get data directly

plan:

1. get most top topics & queries for 2024 for each category
1. recursively get top related topics & queries for each topic
    - depth 3 would give ~16000 queries, resulting in
        $16000\times6\times5=480000$ search result pages if each of
        the 6 search engines returns 5 pages on average
        - which would take $480000\times5/3600/24=28$ days if
            each page takes 5 seconds to classify
    - Google Trends has ~1400 topics, w/ levels of subtopics
        - `google_trends_all_cat.json` from
            <https://github.com/pat310/google-trends-api/wiki/Google-Trends-Categories>
