MARP    := uvx --from marp-cli marp
SRC     := rhiza-intro.md
OUT_DIR := dist

.PHONY: html pdf watch clean

html: $(OUT_DIR)/rhiza-intro.html  ## Build self-contained HTML slide deck

pdf: $(OUT_DIR)/rhiza-intro.pdf    ## Build PDF slide deck

$(OUT_DIR)/rhiza-intro.html: $(SRC)
	mkdir -p $(OUT_DIR)
	$(MARP) --html --output $(OUT_DIR)/rhiza-intro.html $(SRC)

$(OUT_DIR)/rhiza-intro.pdf: $(SRC)
	mkdir -p $(OUT_DIR)
	$(MARP) --pdf --output $(OUT_DIR)/rhiza-intro.pdf $(SRC)

watch:  ## Live-preview in the browser while editing
	$(MARP) --watch --html $(SRC)

clean:  ## Remove built artefacts
	rm -rf $(OUT_DIR)
