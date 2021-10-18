# Crawly - website change tracker

## Description

This repo contains a small script that sends email notifications when it detects a change on a given website. It requires a gmail account credentials and allows you to specify interval frequency (how often the website is checked in hours) and the total number of checks that it will perform.

Disclaimer: the script does not work on dynamic websites as the comparison is based on HTML content hashes.

## Usage

First, in the top level directory create `.env` with your gmail account details as shown in the section below and install required libraries with

```shell
pip install -r requirements.txt
```

Then you can use the script by invoking it with

```shell
python main.py <email> <link> <frequency> <number of checks> <frequency of reminder>
```

where `<frequency>`, `<number of checks>` and `<frequency of reminder>` are optional arguments.

- Frequency is a float expressing hour interval at which the website should be checked, by default it is 12h.
- Number of checks specifies total number of times the website will be checked, by default it is 4 times.
- Frequency of reminder is an float expressing hour interval at which a reminder that crawly is still working will be sent, by default it is 168h (7 days).

## Example `.env`

```env
FROM=your_email@gmail.com
PASS=your_email_password
```
