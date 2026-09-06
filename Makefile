QUARTO ?= quarto
PYTHON ?= python
DOCKER_IMAGE ?= teaching-repository-template-decktape
SRC_SLIDES_DIR := slides
OUT_DIR := _site
SLIDES_DIR := $(OUT_DIR)/slides
SLIDES_QMD := $(shell find $(SRC_SLIDES_DIR) -type f -name '*.qmd' 2>/dev/null)
SLIDES_HTML := $(patsubst $(SRC_SLIDES_DIR)/%.qmd,$(SLIDES_DIR)/%.html,$(SLIDES_QMD))
SLIDES_PDF := $(SLIDES_HTML:.html=.pdf)
NOTES_QMD := $(addprefix notes/session_,$(addsuffix .qmd,01 02 03 04 05 06 07 08 09 10 11))
NOTES_PDF := $(OUT_DIR)/notes.pdf
NOTES_COMBINED := _pdf-tmp/notes.qmd
.PHONY: help site site-fast pdfs notes exercises exercises-assign exercises-solution all sync-events clean
help:
	@echo "Targets: site, pdfs, notes, exercises, all, sync-events, clean"
site-fast:
	$(QUARTO) render --no-clean
site: exercises site-fast
all: site pdfs notes
exercises-assign:
	$(QUARTO) render exercises --profile assign --to ipynb --no-clean
	$(QUARTO) render exercises --profile assign --to html --no-clean
	@for f in _site/exercises/*.ipynb _site/exercises/*.html; do [ -e "$$f" ] && mv "$$f" "$${f%.*}_assign.$${f##*.}" || true; done
exercises-solution:
	$(QUARTO) render exercises --profile solution --to ipynb --no-clean
	$(QUARTO) render exercises --profile solution --to html --no-clean
	@for f in _site/exercises/*.ipynb _site/exercises/*.html; do case "$$f" in *_assign.*|*_solution.*) continue;; esac; [ -e "$$f" ] && mv "$$f" "$${f%.*}_solution.$${f##*.}" || true; done
exercises: exercises-assign exercises-solution
pdfs: $(SLIDES_PDF)

notes: $(NOTES_PDF)

$(NOTES_PDF): $(NOTES_QMD) scripts/combine_notes.py
	@mkdir -p $(OUT_DIR) _pdf-tmp
	@$(PYTHON) scripts/combine_notes.py $(NOTES_COMBINED) $(NOTES_QMD)
	@$(QUARTO) render $(NOTES_COMBINED) --to pdf --output notes.pdf
	@mv _pdf-tmp/notes.pdf $(NOTES_PDF)
	@rm -f $(NOTES_COMBINED)
$(SLIDES_DIR)/%.pdf: $(SRC_SLIDES_DIR)/%.qmd _quarto.yml scripts/decktape.sh
	@mkdir -p $(SLIDES_DIR)
	$(QUARTO) render $< --profile pdf --output-dir $(abspath _pdf-tmp)
	@mv _pdf-tmp/slides/$*.html $(SLIDES_DIR)/$*-pdf.html
	@python3 -m http.server 8000 --directory _site >/tmp/quarto-template-http.log 2>&1 & echo $$! > .server.pid
	@sleep 2; ./scripts/decktape.sh "http://localhost:8000/slides/$*-pdf.html" "$@"; status=$$?; kill $$(cat .server.pid); rm -f .server.pid $(SLIDES_DIR)/$*-pdf.html; rm -rf _pdf-tmp; exit $$status
sync-events:
	$(PYTHON) scripts/sync_events.py
clean:
	rm -rf _site _freeze _pdf-tmp .quarto $(NOTES_COMBINED)
