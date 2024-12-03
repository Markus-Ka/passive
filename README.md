# Passive

**Passive** is an OSINT (Open Source Intelligence) tool for searching usernames, full names, and IP addresses. The tool performs passive reconnaissance to gather relevant information from open sources based on the input. Results are stored in text files.

These tool is for educational purposes only.

---

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Methods](#methods)
- [File Output](#file-output)
- [License](#license)

---

## Introduction

Information gathering is a crucial part of penetration testing (pentesting) and OSINT investigations. Passive reconnaissance involves collecting publicly available data without directly interacting with the target. **Passive** automates this process by allowing users to search for full names, IP addresses, and usernames and retrieve useful details like location, ISP information, and social media presence.

## Features

- Search by full name (first, middle and last name) to retrieve address and phone number details.
- Search by IP address to retrieve city and ISP information.
- Search by username to check for the user's presence across multiple social media platforms.
- Automatically saves results in a new text file (`result.txt`, `result2.txt`, etc.) to prevent overwriting.

---

## Installation

Clone the repository, move into the repo.

If python is not installed:
```bash
$ sh install.sh
```

Then in project directory:
```bash
$ pip install -r requirements.txt
```

Then:
```bash
$ cd python
```
- IMPORTANT: You are going to need to either change the install location to a directory in your PATH or add this one into your PATH and actually make the directory.
```bash
~/customExec
```

You can change the install location here. "~/customExec", if you change "passive", you also need to run the program with the new name.
```bash
mv dist/main ~/customExec/passive
```

- This can be changed the mkExec.sh file

Finally:
```bash
$ sh mkExec.sh
```

---

## Usage

```bash
$ passive --help
```

The primary options are:

- `-fn` : Search by full name.
- Example:
```bash
$ passive -fn "Jean Dupont"
```

- `-ip` : Search by IP address.
- Example:
```bash
$ passive -ip 127.0.0.1
```

- `-u`  : Search by username.
- Example:
```bash
$ passive -u "@user01"
```


The results will be displayed and saved in a results file.

---

## Methods

This program primarily simulates normal user behavior searching for the inputed arguments like a human would, then parsing data directly from the HTML of web pages, as well as sending GET or POST requests to the APIs of various websites when one was available.

---

## File Output

Each time a search is performed, the results are saved in a `result.txt` file in the current directory you are in. If this file already exists, the program creates a new file (`result2.txt`, `result3.txt`, etc.).

---


## Disclaimer

These methods and tools are for educational purposes only, so that you have a better understanding of how to protect against similar vulnerabilities. You must ensure that you do not attempt any exploit-type activity without the explicit permission of the owner of the machine, system or application. Failure to obtain permission risks breaking the law.

## Author

Markus-Ka



