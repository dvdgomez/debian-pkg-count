# debian-pkg-count
Given a debian mirror and architecture, counts the number of files associated with each package and returns the top 10 packages with file counts.

# Usage

Only one architecture is allowed to be selected at a time. Each possible architecture is a flag to be used in the format "--ARCH".

python3 package_statistics.py <--ARCH>

ie 

python3 package_statistics.py --amd64
