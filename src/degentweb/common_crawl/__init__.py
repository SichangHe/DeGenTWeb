from typing import Final

MIN_PAGE_LEN: Final = 1000
"""To ignore pages shorter than around 200 words."""
# NOTE: We will use compressed file in the future.
# This is for easy checking of the WARC file.
WARC_FILE: Final = "CC-MAIN-20240224112548-20240224142548-00079.warc"
OUT_DIR: Final = "data/common_crawl/prelim_test/"
TSV_DIR: Final = f"{OUT_DIR}prelim_test_scores.tsv"
TSV_HEADER: Final = ["id", "english", "score", "bytes", "leng", "tokens", "url"]
