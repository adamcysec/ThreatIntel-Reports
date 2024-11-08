# ThreatIntel-Reports

A fork of [ThreatIntel-Reports](https://github.com/mthcht/ThreatIntel-Reports) from [mthcht](https://x.com/mthcht).

A repository of extracted content from thousands of threat intelligence reports, with an automatic extraction of reports from various feeds !

Be sure to download the most up to date Intel Reports directory from [ThreatIntel-Reports](https://github.com/mthcht/ThreatIntel-Reports)

## What's New?!

This fork uses multi-threading to read all 10,402+ reports very fast.

This tool uses Streamlit for interacting with the threat intel data.

##  Dependencies
search_keyword_streamlit.py requires the following dependencies:

- [streamlit](https://pypi.org/project/streamlit/)
  - `pip install streamlit`
- [pandas](https://pypi.org/project/pandas/)
  - `pip install pandas` 

## Installation

1. git clone repo:

```
git clone https://github.com/adamcysec/ThreatIntel-Reports.git
```

3. Pip install any missing dependencies 

## Usage

Run 

```
streamlit run search_keyword_streamlit.py
```

Note: if you have more than one version of python installed you may need to run streamlit like so:

```
python3 -m streamlit run search_keyword_streamlit.py
```

