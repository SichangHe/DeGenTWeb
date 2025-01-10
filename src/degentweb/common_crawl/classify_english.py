import os
from typing import Final

from fastwarc.warc import ArchiveIterator, WarcRecord, WarcRecordType
from trafilatura import extract

from binoculars import Binoculars
from degentweb.logging import init_logger_w_env_level

# NOTE: We will use compressed file in the future.
# This is for easy checking of the WARC file.
WARC_FILE: Final = "CC-MAIN-20240224112548-20240224142548-00079.warc"
OUT_DIR: Final = "data/common_crawl/prelim_test/"
CONTEXT_WINDOW: Final = 2048
"""Falcon-7B context window size."""
MIN_PAGE_LEN: Final = 1000
"""To ignore pages shorter than around 200 words."""
TSV_HEADER: Final = ["id", "score", "bytes", "len", "url"]

logger = init_logger_w_env_level(__name__)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    bino = Binoculars(max_token_observed=CONTEXT_WINDOW)
    with open(f"{OUT_DIR}prelim_test_scores.tsv", "a") as out_f:
        record: WarcRecord
        for record in ArchiveIterator(
            open(WARC_FILE, "rb"),
            parse_http=True,  # Otherwise sometimes HTTP headers get returned.
            record_types=WarcRecordType.response,
        ):
            record_f_path = f"{OUT_DIR}{record.record_id}"
            if (
                not record.is_http
                # Comment the line below to skip if existing.
                or os.path.exists(record_f_path)
            ):
                continue
            url = record.headers["WARC-Target-URI"]
            record_bytes = record.reader.read()
            try:
                extraction = extract(
                    record_bytes,
                    output_format="txt",
                    include_links=False,
                    include_images=False,
                    favor_precision=True,
                    target_language="en",
                )
            except OverflowError as err:
                logger.error(
                    f"Extracting {record.record_id}\n{err}",
                    stack_info=True,
                    exc_info=True,
                )
                continue
            if (
                extraction is None  # Not English.
                or len(extraction) < MIN_PAGE_LEN
            ):
                continue
            # TODO: Split on long text and batching.
            score = bino.compute_score(extraction)
            assert type(score) is float
            with open(record_f_path, "w") as f:
                assert f.write(extraction) == len(extraction), extraction
            tsv_line = f"{record.record_id}\t{score}\t{len(record_bytes)}\t{len(extraction)}\t{url}\n"
            assert out_f.write(tsv_line) == len(tsv_line), tsv_line


main() if __name__ == "__main__" else None
