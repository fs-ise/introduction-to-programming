# Introduction to Programming

This repository contains the Quarto website and teaching-support files for **Introduction to Programming** at Frankfurt School of Finance & Management.

The course is configured for the **2026-WiSe** semester as a **6 ECTS Bachelor-level** course taught in **English**.

## Key files

- `course.yml` defines course metadata such as title, semester, credits, language, instructor, repository URL, and schedule settings.
- `index.qmd` defines the course homepage, session table, group schedule, and links to notes.
- `teaching_notes.qmd` lists instructor notes for each session.
- `assets/styles.css` contains website-level styling, including the session color chips used in the group schedule.
- `data/sessions.generated.yml` is generated schedule data and should not be edited manually.
- `template/sources.yml` records reviewed source repositories and the template update process.

## Common commands

Run commands from the repository root:

- `make site` renders exercises and the website.
- `make pdfs` creates slide PDFs with Decktape.
- `make exercises` creates assignment and solution variants.
- `make sync-events` regenerates generated schedule data when handbook schedule data are configured.
- `make clean` removes generated build artifacts.
- `PYTHONPATH=. pytest -q` runs the Python test suite in this environment.

## Maintenance notes

- Update `index.qmd` first when the session overview, group dates, or group times change.
- Keep each `notes/session_XX.qmd` aligned with the matching row in the session table.
- If a session number appears multiple times in the group schedule, reuse the same `session-XX` CSS class so the color remains consistent.
- Update this README when course-level details, file organization, or local commands change.

## Licensing

Teaching content defaults to CC BY 4.0 unless noted otherwise.

Helper scripts are template infrastructure and intentionally do not declare a separate software-license decision.
