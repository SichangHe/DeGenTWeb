from typing import Final

from fastwarc.warc import ArchiveIterator, WarcRecord, WarcRecordType
from trafilatura import extract

from binoculars import Binoculars

# NOTE: We will use compressed file in the future.
# This is for easy checking of the WARC file.
WARC_FILE: Final = "CC-MAIN-20240224112548-20240224142548-00079.warc"
CONTEXT_WINDOW: Final = 2048
"""Falcon-7B context window size."""
MIN_PAGE_LEN: Final = 1000


def main():
    bino = Binoculars(max_token_observed=CONTEXT_WINDOW)
    record: WarcRecord
    for record in ArchiveIterator(
        open(WARC_FILE, "rb"),
        parse_http=False,
        record_types=WarcRecordType.response,
    ):
        if not record.is_http:
            continue
        url = record.headers["WARC-Target-URI"]
        record_bytes = record.reader.read()
        extraction = extract(
            record_bytes,
            output_format="txt",
            include_links=False,
            include_images=False,
            favor_precision=True,
            target_language="en",
        )
        if extraction is None:  # Not English.
            continue
        if len(extraction) < MIN_PAGE_LEN:
            continue
        score = bino.compute_score(extraction)
        assert type(score) is float
        print(f"""extraction={extraction}
score={score}, record_id={record.record_id}, url={url}""")
        input()


main() if __name__ == "__main__" else None
