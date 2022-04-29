import sys
import gzip
import urllib.request
from collections import Counter

# Since only one mirror for now, url is constant
URL = "http://ftp.uk.debian.org/debian/dists/stable/main/"

def check_architecture(arch: str) -> bool:
    """Make sure the architecture is a valid option.

    Args:
    arch -- Architecture input
    """
    return True if arch in options else False

def download_contents_index(url: str, arch: str) -> list:
    """Download contents index.

    Args:
    url -- URL of Debian Mirror
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
                import pdb
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
    # Make sure valid number of arguments input
    if len(sys.argv) != 2:
        sys.exit("Usage: package_statistics.py <ARCH>")
    # Architecture Input Arg
    architecture = sys.argv[1]
    # TODO: Check if architecture is valid otherwise exit
    # Download the respective contents index for the architecture
    content = download_contents_index(URL, architecture)
    # TODO: Remove file after download
    # Parse the file output and count files per package
    pkg_count = count_pkgs(content)
    # Output top ten packages with most files associated with them
    for index, pkg in enumerate(pkg_count):
        print(f"{index+1}. {pkg[0]}  {pkg[1]}")
