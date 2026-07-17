#!/usr/bin/env python3
"""Produce the public, redacted CV from the private source PDF.

Truly removes matched text (not just visually covers it) and drops the last
page (the personal 'work week' chart). Redaction terms are passed on the
command line so no private values (hourly rate, phone number, availability
date) ever live in this repo.

Requires PyMuPDF (`pip install pymupdf`).

Usage:
  python build/redact-cv.py SOURCE.pdf pooya-shahryari-cv.pdf \
      --redact "<hourly rate>" "<phone number>" "FÖREDRAGET TIMPRIS" \
               "TILLGÄNGLIGHET" "<availability date>" \
      --drop-last-page

The published pooya-shahryari-cv.pdf was generated this way; the private
source PDF is kept locally and is not committed.
"""
import argparse, fitz

ap = argparse.ArgumentParser()
ap.add_argument("source")
ap.add_argument("out")
ap.add_argument("--redact", nargs="*", default=[], help="exact strings to remove")
ap.add_argument("--drop-last-page", action="store_true")
a = ap.parse_args()

doc = fitz.open(a.source)
for page in doc:
    for term in a.redact:
        for rect in page.search_for(term):
            page.add_redact_annot(rect, fill=(1, 1, 1))
    page.apply_redactions()
if a.drop_last_page:
    doc.delete_page(doc.page_count - 1)
doc.save(a.out, garbage=4, deflate=True)

# verify nothing matched survives
v = fitz.open(a.out)
text = "\n".join(v[p].get_text() for p in range(v.page_count))
leftover = [t for t in a.redact if t in text]
print(f"pages: {v.page_count} | redaction verified: {'FAILED ' + str(leftover) if leftover else 'clean'}")
