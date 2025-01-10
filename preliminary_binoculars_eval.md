# Preliminary Binoculars Evaluation

- [x] dump English HTTP response from random Common Crawl WARC file
- [x] extract main text; if longer than 2000 character, feed into Binoculars
- [ ] split long page down to Falcon-7B context window 2048 token
    - currently, simply truncate
    - [ ] average score weighted on token count

script: `degentweb.common_crawl.classify_english `

result dumped to `data/common_crawl/prelim_test/`; 5961 page; used 1h 20m

## manual inspection of 1010 page

low-score page:

- ~19 seem indeed generate article, mostly blog & product
- 3 simply table-like listing
- 7 short listing/interaction page (scoreboard, links;
    only 2 are > 2000 character)
- boilerplate text: 7 cookie banner (< 2000 character); 1 legal notice
- 1 seem false positive
    <https://catalyticconvertersolutions.com/writer/nicolas-will/>

lower-score page (above FPR-threshold but around F1-threshold):

- many also seem generated, some not
    - 1 page error message (MySQL)
    - boilerplate text (legal)
