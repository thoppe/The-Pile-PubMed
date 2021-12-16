import time
import os
import gzip
import hashlib
import json
import requests

from pathlib import Path
from wasabi import msg


def days_since_modified(f):
    """
    Return the number of days since the file was modified.
    """

    dt = time.time() - os.path.getmtime(f)
    seconds_per_day = 60 * 60 * 24

    return dt / seconds_per_day


def mkdir(dest):
    """
    Safely creates a nested directory. Ignores if exists.
    """
    Path(dest).mkdir(parents=True, exist_ok=True)


def file_md5sum(f, chunksize=4096):
    """
    Returns the md5sum for an input file.
    Chunks the data so it's non-blocking.
    """
    hash_md5 = hashlib.md5()

    with open(f, "rb") as FIN:
        for chunk in iter(lambda: FIN.read(chunksize), b""):
            hash_md5.update(chunk)

    return hash_md5.hexdigest()


def iterate_pubmed_xml(f0):
    """
    Iterator that returns a list of lines of XML
    broken up by the PubmedArticle.
    """

    article_start = "<PubmedArticle>"
    article_end = "</PubmedArticle>"
    pmid = None

    with gzip.GzipFile(f0, "rb") as FIN:

        raw_article_xml = []

        # Advance to the first article
        for line in FIN:
            line = line.decode("utf-8")
            if article_start in line:
                break

        xml = [line]

        for line in FIN:

            line = line.decode("utf-8")

            # Match the first instance of PMID
            if pmid is None and "</PMID>" in line:
                pmid = int(line.split("<")[-2].split(">")[-1])

            xml.append(line)

            if article_end in line:

                # yield ''.join(xml)
                yield (pmid, "".join(xml))
                xml = list()
                pmid = None
