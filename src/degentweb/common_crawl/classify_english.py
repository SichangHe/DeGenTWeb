import os
from typing import Final

from fastwarc.warc import ArchiveIterator, WarcRecord, WarcRecordType
from trafilatura import extract

from binoculars import Binoculars
from degentweb.common_crawl import OUT_DIR, TSV_DIR, WARC_FILE
from degentweb.logging import init_logger_w_env_level

CONTEXT_WINDOW: Final = 2048
"""Falcon-7B context window size."""

logger = init_logger_w_env_level(__name__)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    bino = Binoculars(max_token_observed=CONTEXT_WINDOW)
    with open(TSV_DIR, "a") as out_f:
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
            english, score, leng, tokens = False, -1, -1, -1
            if extraction is not None:  # English.
                english, leng = True, len(extraction)
                with open(record_f_path, "w") as f:
                    assert f.write(extraction) == len(extraction), extraction
                # TODO: Split on long text and batching.
                encodings = bino._tokenize([extraction])
                tokens = len(encodings)
                score = bino.compute_encodings_score(encodings)[0]
            tsv_line = f"{record.record_id}\t{int(english)}\t{score}\
\t{len(record_bytes)}\t{leng}\t{tokens}\t{url}\n"
            assert out_f.write(tsv_line) == len(tsv_line), tsv_line


main() if __name__ == "__main__" else None
