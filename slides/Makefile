MARP    := npx --yes @marp-team/marp-cli
SRC     := rhiza-intro.md
SRC_DD  := rhiza-deep-dive.md
OUT_DIR := dist

.PHONY: html pdf watch watch-deep-dive clean

html: $(OUT_DIR)/rhiza-intro.html $(OUT_DIR)/rhiza-deep-dive.html  ## Build all HTML slide decks

pdf: $(OUT_DIR)/rhiza-intro.pdf $(OUT_DIR)/rhiza-deep-dive.pdf     ## Build all PDF slide decks

$(OUT_DIR)/rhiza-intro.html: $(SRC)
	mkdir -p $(OUT_DIR)
	$(MARP) --html --output $(OUT_DIR)/rhiza-intro.html $(SRC)

$(OUT_DIR)/rhiza-deep-dive.html: $(SRC_DD)
	mkdir -p $(OUT_DIR)
	$(MARP) --html --output $(OUT_DIR)/rhiza-deep-dive.html $(SRC_DD)

$(OUT_DIR)/rhiza-intro.pdf: $(SRC)
	mkdir -p $(OUT_DIR)
	$(MARP) --pdf --output $(OUT_DIR)/rhiza-intro.pdf $(SRC)

$(OUT_DIR)/rhiza-deep-dive.pdf: $(SRC_DD)
	mkdir -p $(OUT_DIR)
	$(MARP) --pdf --output $(OUT_DIR)/rhiza-deep-dive.pdf $(SRC_DD)

watch:  ## Live-preview rhiza-intro in the browser while editing
	$(MARP) --watch --html $(SRC)

watch-deep-dive:  ## Live-preview rhiza-deep-dive in the browser while editing
	$(MARP) --watch --html $(SRC_DD)

clean:  ## Remove built artefacts
	rm -rf $(OUT_DIR)
