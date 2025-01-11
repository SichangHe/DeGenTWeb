"""This file is designed to be copied into a REPL."""

import pandas as pd

from degentweb.common_crawl import MIN_PAGE_LEN, OUT_DIR, TSV_FILE_URL, TSV_HEADER
from degentweb.plotting import Plot

TSV_FILE_URL.download()
df = pd.read_csv(TSV_FILE_URL.file, sep="\t", names=TSV_HEADER, engine="pyarrow")

df_eng = df[df["english"] == 1]
assert not (
    (df_eng["score"] == -1) | (df_eng["leng"] == -1) | (df_eng["tokens"] == -1)
).any()
df_long = df_eng[df_eng["leng"] > MIN_PAGE_LEN]
print(
    f"""
{len(df)} HTTP responses
{len(df_eng)} are English ({len(df_eng) * 100 / len(df):.2f}%)
{len(df_long)} out of English are longer than {MIN_PAGE_LEN} in text ({len(df_long) * 100 / len(df_eng):.2f}%)
""".strip()
)
"""
29935 HTTP responses
11743 are English (39.23%)
5070 out of English are longer than 1000 in text (43.17%)
"""

plot = Plot()
ax = plot.ax
ax.ecdf(df_eng["leng"], label="CDF of Length")
ax.axhline(
    y=(1 - len(df_long) / len(df_eng)),
    linewidth=2,
    color="k",
    alpha=0.7,
    label="Length Filter Threshold",
)
ax.set_xscale("log")
ax.set_xlabel("Length After Main Text Extraction", fontsize=36)
ax.set_ylabel(
    "Cumulative Fraction\nof English Responses",
    fontsize=36,
)
plot.save(f"{OUT_DIR}cdf_leng_eng")
