import os
import sys
import gzip
import argparse
import urllib.request
from collections import Counter

# Since only one mirror for now, url is constant
URL = "http://ftp.uk.debian.org/debian/dists/stable/main/"

def download_contents_index(url: str, arch: str) -> list:
    """Download contents index.

    Args:
    url -- URL of Debian Mirror
    arch -- Input architecture selected
    """
    # Try and download contents index, exit if download fails
    try:
        output = []
        urllib.request.urlretrieve(f"{url}Contents-{arch}.gz", "contents_index.gz")
        # Open downloaded .gz file and read
        with gzip.open("contents_index.gz", "rb") as fp:
            # Store package column of each line
            for line in fp:
                # Convert from bytes to string and skip filename column
                line = line.decode("utf-8").split()[1:]
                # Check if multiple packages per file
                if "," in line[0]:
                    # Split comma separated packages line
                    line = line[0].split(",")
                    for pkg in line:
                        # package name is last in path
                        output.append(pkg.split("/")[-1])
                else:
                    # Only 1 package for file case
                    output.append(line[0].split("/")[-1])
        return output
    except:
        sys.exit("Unable to download contents index!")
        
def count_pkgs(pkgs: list) -> list:
    """Count how many times a package was associated with a file in list

    Args:
    content -- Content index package list per file
    """
    # Return list of top ten packages with most files
    return Counter(pkgs).most_common(10)


if __name__ == "__main__":
    # Argument Parse
    parser = argparse.ArgumentParser(description = "Package Statistics Tool")
    # Only allow one architecture to be passed in
    arch_arg = parser.add_mutually_exclusive_group()
    # Ensures only valid architecture is selected/input
    arch_arg.add_argument("--amd64", help = "amd64 architecture", action = "store_true")
    arch_arg.add_argument("--arm64", help = "arm64 architecture", action = "store_true")
    arch_arg.add_argument("--armel", help = "armel architecture", action = "store_true")
    arch_arg.add_argument("--armhf", help = "armhf architecture", action = "store_true")
    arch_arg.add_argument("--i386", help = "i386 architecture", action = "store_true")
    arch_arg.add_argument("--mips64el", help = "mips64el architecture", action = "store_true")
    arch_arg.add_argument("--mipsel", help = "mipsel architecture", action = "store_true")
    arch_arg.add_argument("--ppc64el", help = "ppc64el architecture", action = "store_true")
    arch_arg.add_argument("--s390x", help = "s390x architecture", action = "store_true")
    args = parser.parse_args()
    if args.amd64:
        architecture = "amd64"
    elif args.arm64:
        architecture = "arm64"
    elif args.armel:
        architecture = "armel"
    elif args.armhf:
        architecture = "armhf"
    elif args.i386:
        architecture = "i386"
    elif args.mips64el:
        architecture = "mips64el"
    elif args.mipsel:
        architecture = "ppc64el"
    elif args.s390x:
        architecture = "s390x"
    else:
        sys.exit("No architecture selected, exiting!")
    # Download the respective contents index for the architecture
    content = download_contents_index(URL, architecture)
    # Check if file exists before removing
    if os.path.isfile("contents_index.gz"):
        # Remove file after download
        os.remove("contents_index.gz")
    # Parse the file output and count files per package
    pkg_count = count_pkgs(content)
    # Output top ten packages with most files associated with them
    for index, pkg in enumerate(pkg_count):
        print(f"{index+1}. {pkg[0]}  {pkg[1]}")
