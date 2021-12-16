from pathlib import Path
from ftplib import FTP
import io, sys, time
from utils import file_md5sum

from wasabi import msg
import pandas as pd
from dspipe import Pipe


# This does not check for the update files, and only downloads the yearly
# dump

base_url = "ftp.ncbi.nlm.nih.gov"

ftp_name = "baseline"
ftp_dest = f"/pubmed/{ftp_name}"


def download_ftp(f0, f1):

    msg.info(f"Starting {f0}")

    ftp = FTP(base_url, user="anonymous", passwd="")
    ftp.cwd(ftp_dest)

    # Download the file first, then save it if successful
    fp = io.BytesIO()
    ftp.retrbinary(f"RETR {f0}", fp.write)
    fp.seek(0)

    with open(f1, "wb") as FOUT:
        FOUT.write(fp.read())

    msg.good(f"Downloaded {f1}")
    time.sleep(2)


def check_hash(f0):
    key = f0.stem + ".xml.gz"

    if key not in md5:
        msg.fail(f"Can't find md5 hash for {key}, suspicious and should look into!")
        return

    if file_md5sum(f0) != md5[key]:
        msg.fail(f"Checksum failed {key}, should delete!")
        print(f0)
        return


if __name__ == "__main__":

    f0 = Path("data") / f"PUBMED_ftp_{ftp_name}.csv"
    df = pd.read_csv(f0)

    # Only look for the files
    df = df[df["type"] == "file"]

    # Download the md5 hash first
    F_MD5 = df[df.filename.str.endswith(".md5")].filename

    P = Pipe(
        source=F_MD5,
        dest=f"data/{ftp_name}/md5",
        output_suffix=".md5",
        shuffle=True,
    )(download_ftp, 16)

    # Download the files
    F_GZ = df[df.filename.str.endswith(".gz")].filename

    P = Pipe(
        source=F_GZ,
        dest=f"data/{ftp_name}/gz",
        output_suffix=".gz",
        shuffle=True,
    )(download_ftp, 2)

    # Read the expected hash
    md5 = dict()
    for f in Path(f"data/{ftp_name}/md5").glob("*.md5"):
        with open(f) as FIN:
            line = FIN.readline()
            name, hx = line.split()
            name = name[4:-2]
            md5[name] = hx

    # Check the hashes
    P = Pipe(source=f"data/{ftp_name}/gz", output_suffix=".gz", shuffle=False)(
        check_hash, -1
    )

    msg.good(f"Finished downloading and checking {ftp_dest}")
