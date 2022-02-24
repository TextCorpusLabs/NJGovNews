from setuptools import setup
from scripts.install import InstallOverride

with open('README.md', 'r') as fp:
    long_description = fp.read()
with open('requirements.txt', 'r') as fp:
    requires = [req.strip() for req in fp.readlines()]

setup(
    name = "NJGovNews",
    version = "0.0.1",
    author = '@markanewman',
    author_email = 'NJGovNews@trinetteandmark.com',
    description = "Scrape the news feed from the New Jersey government",
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = "https://github.com/TextCorpusLabs/NJGovNews",
    project_urls = {
        'Bug Reports': 'https://github.com/TextCorpusLabs/NJGovNews/issues',
        'Source': 'https://github.com/TextCorpusLabs/NJGovNews',
    },
    packages = ['NJGovNews'],
    entry_points = {
        'console_scripts': [
            'NJGovNews = NJGovNews.__main__:main'
        ],
    },
    classifiers = [        
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Linguistic'
    ],
    python_requires = '>=3.10, <4',
    install_requires = requires,
    cmdclass = { 'install': InstallOverride }
)
