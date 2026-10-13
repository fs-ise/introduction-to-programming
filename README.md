<p align="center">
  <img src="https://raw.githubusercontent.com/fs-ise/analytics-and-big-data/main/assets/fs_logo_blue.svg" alt="Frankfurt School logo" height="64">
</p>

<h1 align="center">Introduction to Programming</h1>

<p align="center">
  <img alt="Offered by Frankfurt School of Finance &amp; Management" src="https://img.shields.io/badge/Offered%20by-Frankfurt%20School%20of%20Finance%20%26%20Management-blue">
  <a href="https://github.com/fs-ise/introduction-to-programming/actions/workflows/publish.yml"><img alt="GitHub Actions: publish" src="https://github.com/fs-ise/introduction-to-programming/actions/workflows/publish.yml/badge.svg"></a>
  <a href="LICENSE"><img alt="License: CC BY 4.0" src="https://img.shields.io/badge/License-CC%20BY%204.0-green.svg"></a>
</p>

Welcome! **Introduction to Programming** is a 6 ECTS Bachelor course at Frankfurt School of Finance & Management. Through hands-on exercises, students learn to solve business and numerical problems using Excel and Python.

Visit the [course website](https://fs-ise.github.io/introduction-to-programming/), read the [syllabus](https://fs-ise.github.io/introduction-to-programming/syllabus.html), and browse the [teaching materials](https://fs-ise.github.io/introduction-to-programming/materials.html).

## For developers

Requires Python 3.11+ and [Quarto 1.8+](https://quarto.org/docs/get-started/). From the repository root:

```sh
python -m pip install -r requirements.txt
make site-fast  # render the website
make site       # render exercises and the website
```

See the [Quarto project guide](https://quarto.org/docs/projects/quarto-projects.html) and the available targets in the [Makefile](Makefile).
