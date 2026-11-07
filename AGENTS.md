# Repository guidance

## Project structure

- This repository contains a Quarto course website and teaching materials.
- Most course content is authored in `.qmd` files, including content in
  `notes/`, `slides/`, `exercises/`, `materials/`, and `student_guide/`.
- Student Python examples are mainly in `materials/session_*` and in Python
  code cells in course documents. Build helpers are in `scripts/`; tests are
  in `tests/`.
- The project requires Python 3.11 or newer and Quarto 1.8 or newer.

## Student-facing Python conventions

These conventions apply to Python examples and instructional code in course
materials. They do not apply to maintainer scripts in `scripts/` or automated
tests in `tests/`.

- Keep examples beginner-friendly and use standard Python syntax and concepts
  that students have already been taught. For a given session, use only syntax
  introduced in that session or an earlier one. Check `index.qmd` for the
  session sequence and the corresponding `notes/session_NN.qmd` for what has
  been covered.
- Follow the course progression: Sessions 04–07 introduce Python basics,
  strings and I/O, and Pandas; Session 08 covers sequences and conditionals;
  Session 09 covers loops; Session 10 covers loop control, functions, and
  dictionaries; Session 11 covers Pandas automation and web APIs.
- **Never use f-strings** (including raw f-strings) in student-facing Python
  examples.
- When building output strings, prefer the patterns taught in class: combine
  strings with `+`, convert non-string values with `str()` before combining,
  or pass separate values to `print()` when its spacing is appropriate. Do not
  use `.format()` as a general-purpose replacement unless string formatting is
  explicitly taught; its use in a specific Pandas display option does not make
  it the default way to build strings.
- Do not add docstrings or type hints to student-facing examples.
- Do not use `pathlib.Path` in student-facing examples. Prefer the simpler
  path-handling techniques taught in the course.
- Do not specify an explicit file encoding in student-facing examples unless
  the instructor requests it or correctness requires it.
- Prefer brief comments and clear variable names to explain examples.

## Formatting, tests, and builds

- The pre-commit configuration runs Ruff's Python formatter and checks LF line
  endings in Python, Quarto, Markdown, YAML, and shell files. It does not run
  Ruff lint checks.
- Python tests are in `tests/` and use both pytest and `unittest` patterns.
  Run them with `python -m pytest` when pytest is available; pytest is not
  currently listed in the project dependencies.
- `make site-fast` renders the website.
- `make site` renders exercise PDFs and then the website.
- `make pdfs` and `make notes` build printable slides and teaching notes and
  may require PDF/LaTeX tooling.
