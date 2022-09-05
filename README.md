# SABRmetrics

<div>
  <a href="https://github.com/JacobLee23/SABRmetrics/blob/master/LICENSE" target="_blank">
    <img src="https://img.shields.io/github/license/JacobLee23/SABRmetrics" alt="LICENSE">
  </a>
  <img src="https://img.shields.io/pypi/pyversions/SABRmetrics" alt="PyPI - Python Version">
  <a href="https://github.com/JacobLee23/SABRmetrics/blob/master/Pipfile" target="_blank">
    <img src="https://img.shields.io/github/pipenv/locked/python-version/JacobLee23/SABRmetrics" alt="GitHub Pipenv locked Python version">
  </a>
  <a href="https://pypi.org/project/sabrmetrics/" target="_blank">
    <img src="https://img.shields.io/pypi/v/sabrmetrics" alt="PyPI">
  </a>
  <a href="https://github.com/JacobLee23/SABRmetrics/releases/latest" target="_blank">
    <img src="https://img.shields.io/github/v/release/JacobLee23/SABRmetrics" alt="GitHub release (latest SemVer)">
  </a>
  <a href="https://github.com/JacobLee23/SABRmetrics/tags" target="_blank">
    <img src="https://img.shields.io/github/v/tag/JacobLee23/SABRmetrics" alt="GitHub tag (latest SemVer)">
  </a>
</div>
<div>
  <img src="https://img.shields.io/github/languages/code-size/JacobLee23/SABRmetrics" alt="GitHub code size in bytes">
  <a href="https://github.com/JacobLee23/SABRmetrics/find/master" target="_blank">
    <img src="https://img.shields.io/github/directory-file-count/JacobLee23/SABRmetrics" alt="GitHub repo file count">
  </a>
  <img src="https://img.shields.io/github/repo-size/JacobLee23/SABRmetrics" alt="GitHub repo size">
  <img src="https://img.shields.io/github/commit-activity/m/JacobLee23/SABRmetrics" alt="Commit Activity (Month)">
  <a href="https://github.com/JacobLee23/SABRmetrics/commits/master" target="_blank">
    <img src="https://img.shields.io/github/last-commit/JacobLee23/SABRmetrics" alt="Last Commit">
  </a>
</div>
<div>
  <a href="https://github.com/JacobLee23/SABRmetrics/issues" target="_blank">
    <img src="https://img.shields.io/github/issues-raw/JacobLee23/SABRmetrics" alt="GitHub issues">
  </a>
  <a href="https://github.com/JacobLee23/SABRmetrics/issues?q=is%3Aissue+is%3Aclosed" target="_blank">
    <img src="https://img.shields.io/github/issues-closed-raw/JacobLee23/SABRmetrics" alt="GitHub closed issues">
  </a>
  <a href="https://github.com/JacobLee23/SABRmetrics/pulls" target="_blank">
    <img src="https://img.shields.io/github/issues-pr-raw/JacobLee23/SABRmetrics" alt="GitHub pull requests">
  </a>
  <a href="https://github.com/JacobLee23/SABRmetrics/pulls?q=is%3Apr+is%3Aclosed" target="_blank">
    <img src="https://img.shields.io/github/issues-pr-closed-raw/JacobLee23/SABRmetrics" alt="GitHub closed pull requests">
  </a>
</div>

***

## Background

An open-source library of web-scraping software for popular SABRmetrics websites. 

> Sabermetrics (or originally as SABRmetrics) is the empirical analysis of baseball, especially baseball statistics that measure in-game activity. 

-- [Wikipedia](https://en.wikipedia.org/wiki/Sabermetrics)

> sabermetrics, the statistical analysis of baseball data. Sabermetrics aims to quantify baseball players’ performances based on objective statistical measurements, especially in opposition to many of the established statistics (such as, for example, runs batted in and pitching wins) that give less accurate approximations of individual efficacy.

-- [Britannica](https://www.britannica.com/sports/sabermetrics)

***

## Primary Features

- Easy scraping of various Internet Player ID databases

## Installation

From PyPI:

```cmd
python -m pip install sabrmetrics
```

Directly from GitHub:

```cmd
python -m pip install -e git+https://github.com/JacobLee23/SABRmetrics.git#egg=sabrmetrics
```

## Requirements

This project requires Python 3.6+.

*Note: Some of the packages listed in the project Pipfile under `dev-packages` are not compatible with Python 3.6.
This includes `pytest`, so project tests cannot be run using Python 3.6.
However, all primary dependencies (under `default`) are compatible with Python 3.6, so Python 3.6 supports most normal functionality.*

## Dependencies

- [`beautifulsoup4`](https://pypi.org/project/beautifulsoup4/) ([Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/))
- [`lxml`](https://pypi.org/project/lxml/) ([Documentation](https://lxml.de/))
- [`numpy`](https://pypi.org/project/numpy/) ([Documentation](https://numpy.org/doc/))
- [`pandas`](https://pypi.org/project/pandas/) ([Documentation](https://pandas.pydata.org/pandas-docs/stable/))
- [`python-dateutil`](https://pypi.org/project/python-dateutil/) ([Documentation](https://dateutil.readthedocs.io/))
- [`requests`](https://pypi.org/project/requests/) ([Documentation](https://requests.readthedocs.io/))

This project uses [`pipenv`](https://pypi.org/project/pipenv/) ([Documentation](https://pipenv.pypa.io/en/latest/)) for virtual environment dependency management.
See the [Pipfile](https://github.com/JacobLee23/SABRmetrics/blob/master/Pipfile) to see a full list of package dependencies, including development dependencies.

## Testing

The tests for this project are written using [`pytest`](https://pypi.org/project/pytest) ([Documentation](https://docs.pytest.org/)).
To run the project tests, run:

```cmd
pytest sabrmetrics/tests/
```

The `pipenv` command script shorthand defined in the project [Pipfile][Pipfile] can also be used to run the project tests; run:

```cmd
pipenv pytest
```

Another `pipenv` command script shorthand is defined in the project [Pipfile][Pipfile] can be used to output an HTML test report, using [`pytest-html`](https://pypi.org/project/pytest-html) ([Documentation](https://pytest-html.readthedocs.io/)); run:

```cmd
pipenv pytest-html
```

## License

This project is license under the [MIT License][LICENSE].

## Documentation

[![Documentation Status](https://readthedocs.org/projects/sabrmetrics/badge/?version=latest)][Documentation]

The documentation for this project is hosted by [Read the Docs](https://readthedocs.org/): [Official Documentation][Documentation]


[Documentation]: https://sabrmetrics.readthedocs.io/en/latest/
[LICENSE]: https://github.com/JacobLee23/SABRmetrics/blob/master/LICENSE
[Pipfile]: https://github.com/JacobLee23/SABRmetrics/blob/master/Pipfile
