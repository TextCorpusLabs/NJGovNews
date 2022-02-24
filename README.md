# New Jersey Government News

![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![MIT license](https://img.shields.io/badge/License-MIT-green.svg)

Scrape news feeds from the New Jersey government

# Operation

## Install

You can install the package using the following steps:

1. `pip` install using an _admin_ prompt
   ```{ps1}
   pip uninstall NJGovNews
   pip install -v git+https://github.com/TextCorpusLabs/NJGovNews.git
   ```

## Run

You can run the package as follows:

```{ps1}
 NJGovNews SITE -out FILE_OUT
```

The scraper currently supports the following `SITE`s:

1. The [Department of the Treasury](https://nj.gov/treasury).
   I.E. ` NJGovNews treasury -out "c:/data/news/nj_treasury.csv"`

## Cache

This scraper uses `requests-cache` to improve performance.
If you want to _force_ a full reload of all the data, delete the file called 'SITE.cache.sqlite'.
It will be in the same folder as the _.csv_ the scraper created.

# Development

## Prerequisites

You can install the package _for development_ using the following steps:

**Note**: You can replace steps 1-3 using the [VSCode](https://code.visualstudio.com/Download) Git:Clone command

1. Download the project from [GitHub](https://github.com/TextCorpusLabs/NJGovNews)
   * Click the green "Code" button on the right.
     Select "Download Zip"
2. Remove zip protections by right-clicking on the file, selecting properties, and checking "security: unblock"
3. Unzip the folder.
   I recommend using the folder _c:/repos/TextCorpusLabs/NJGovNews_
4. Run `pip`'s edit install using an _admin_ prompt
   ```{ps1}   
   pip uninstall NJGovNews
   pip install -v -e c:/repos/TextCorpusLabs/NJGovNews
   ```
5. Install the `nltk` add-ons using an _admin_ prompt
   ```{ps1}   
   python -c "import nltk;nltk.download('punkt')"
   ```
