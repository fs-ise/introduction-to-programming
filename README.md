# Introduction to Programming

This repository contains the Quarto website and teaching-support files for **Introduction to Programming** at Frankfurt School of Finance & Management.

The course is configured for the **2026-WiSe** semester as a **6 ECTS Bachelor-level** course taught in **English**.

## Key files

- `course.yml` defines course metadata such as title, semester, credits, language, instructor, repository URL, and schedule settings.
- `index.qmd` defines the course homepage, session table, group schedule, and links to notes.
- `teaching_notes.qmd` lists instructor notes for each session.
- `assets/styles.css` contains website-level styling, including the session color chips used in the group schedule.
- `data/sessions.generated.yml` is generated schedule data and should not be edited manually.
- `materials.qmd` is the automatically generated student-facing index of files in `materials/`.
- `data/materials.generated.md` is the generated Materials page content and should not be edited manually.
- `template/sources.yml` records reviewed source repositories and the template update process.

## Common commands

Run commands from the repository root:

- `make site` renders exercises and the website.
- `make pdfs` creates slide PDFs with Decktape.
- `make exercises` creates assignment and solution variants.
- `make sync-events` regenerates generated schedule data when handbook schedule data are configured.
- `make clean` removes generated build artifacts.
- `python scripts/generate_materials_overview.py` manually refreshes the Materials page index (Quarto also runs it before every render or preview).
- `PYTHONPATH=. pytest -q` runs the Python test suite in this environment.

## Maintenance notes

- Update `index.qmd` first when the session overview, group dates, or group times change.
- Keep each `notes/session_XX.qmd` aligned with the matching row in the session table.
- If a session number appears multiple times in the group schedule, reuse the same `session-XX` CSS class so the color remains consistent.
- Update this README when course-level details, file organization, or local commands change.

## Materials page

The website's Materials page is built automatically by recursively scanning
`materials/`. Quarto runs `scripts/generate_materials_overview.py` before rendering
and includes the resulting `data/materials.generated.md` fragment in `materials.qmd`.
The generator only rewrites that fragment when its contents change.

Hidden files and directories, cache and build directories, Quarto fragments whose
names start with `_`, Office temporary files beginning with `~$`, solution files,
`.DS_Store`, and generated HTML files that have a matching QMD source are excluded.
To update the overview without rendering the site, run
`python scripts/generate_materials_overview.py` from the repository root.

## Licensing

Teaching content defaults to CC BY 4.0 unless noted otherwise.

Helper scripts are template infrastructure and intentionally do not declare a separate software-license decision.
