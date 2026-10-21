# Kali NetHunter Handbook — Companion Labs v1.0

Companion scripts and synthetic datasets for Sercan Akyuz's Kali NetHunter Handbook. This download does not contain the ebook or manuscript.

## Download the companion files

[Download Companion Labs v1.0 (ZIP)](https://github.com/menuvision1/nethunter-handbook-labs/releases/download/v1.0.0/NetHunter_Handbook_Labs_v1.0.zip)

No GitHub account, email signup or purchase verification is needed. Use the tagged release matching the book, rather than an unversioned development copy.

## Start here

Download and extract the versioned ZIP. Keep its folder structure. In Kali or a Linux host, open a Bash terminal in the extracted directory containing labs/ and run:

```bash
export BOOK="$PWD"
test -f "$BOOK/labs/course_server.py" && echo companion_ready
mkdir -p "$HOME/nethunter-practice"
```

Use the chapter instructions for your exercise. Set BOOK again to this same directory when opening another terminal. These are Bash commands, not PowerShell commands. Python scripts use the standard library. Depending on the chapter, install Python 3, curl, Nmap, TShark/capinfos, Git or unzip in the environment where you will run the commands. Wireshark's GUI is optional for saved-file analysis.

## Files

- course_server.py: connected-course API on 127.0.0.1:8765, with explicitly selected vulnerable or fixed mode.
- webapp.py: web teaching service on 127.0.0.1:8000.
- apiapp.py: API teaching service on 127.0.0.1:8001.
- synthetic-http.pcap and course-reference.pcap: authored packet fixtures, not recordings from a phone.
- inventory.py and sample-scan.xml: inventory parsing exercise.
- wireless_audit.py and wireless-before/after.csv: synthetic wireless configuration review.
- signal_lab.py: synthetic signal exercise, without radio transmission or reception.
- make_training_archive.py: generates a non-installable teaching archive.
- envcheck.sh: environment inspection.
- hands-on/: fictional device record and synthetic login events.

All these files are inside labs/. Read course-reference.README.md for that packet fixture's provenance.

## Boundaries and cleanup

The teaching services contain deliberate flaws. They bind only to loopback and use fictional accounts. Keep clients and servers in the same environment; a phone and a desktop have different loopback targets. Do not expose the services publicly or use real credentials. Stop a foreground server with Ctrl+C when finished. Do not run two exercises on port 8765 simultaneously. Hardware capabilities are not established by these exercises.

## Version and integrity

Use this v1.0 release with the revised learning edition. SHA256SUMS.txt records file hashes. From this extracted directory, `sha256sum -c SHA256SUMS.txt` checks the downloaded files. Keep versioned releases available so older book instructions remain reproducible.

## Author's website

Explore preconfigured Android cybersecurity lab phones and kits at [DVN Cyber Labs](https://www.dvncyberlabs.com/), the author's website. Compare each listing's environment and accessories with your intended exercises. Buying a device is not required to use these companion files or complete the core userland labs.
