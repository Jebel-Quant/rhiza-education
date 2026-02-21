MARP      := npx --yes @marp-team/marp-cli
SRC       := rhiza-intro.md
SRC_DD    := rhiza-deep-dive.md
SRC_CICD  := cicd-intro.md
OUT_DIR   := dist

.PHONY: html pdf watch watch-deep-dive watch-cicd clean

html: $(OUT_DIR)/rhiza-intro.html $(OUT_DIR)/rhiza-deep-dive.html $(OUT_DIR)/cicd-intro.html  ## Build all HTML slide decks

pdf: $(OUT_DIR)/rhiza-intro.pdf $(OUT_DIR)/rhiza-deep-dive.pdf $(OUT_DIR)/cicd-intro.pdf      ## Build all PDF slide decks

$(OUT_DIR)/rhiza-intro.html: $(SRC)
	mkdir -p $(OUT_DIR)
	$(MARP) --html --output $(OUT_DIR)/rhiza-intro.html $(SRC)

$(OUT_DIR)/rhiza-deep-dive.html: $(SRC_DD)
	mkdir -p $(OUT_DIR)
	$(MARP) --html --output $(OUT_DIR)/rhiza-deep-dive.html $(SRC_DD)

$(OUT_DIR)/cicd-intro.html: $(SRC_CICD)
	mkdir -p $(OUT_DIR)
	$(MARP) --html --output $(OUT_DIR)/cicd-intro.html $(SRC_CICD)

$(OUT_DIR)/rhiza-intro.pdf: $(SRC)
	mkdir -p $(OUT_DIR)
	$(MARP) --pdf --output $(OUT_DIR)/rhiza-intro.pdf $(SRC)

$(OUT_DIR)/rhiza-deep-dive.pdf: $(SRC_DD)
	mkdir -p $(OUT_DIR)
	$(MARP) --pdf --output $(OUT_DIR)/rhiza-deep-dive.pdf $(SRC_DD)

$(OUT_DIR)/cicd-intro.pdf: $(SRC_CICD)
	mkdir -p $(OUT_DIR)
	$(MARP) --pdf --output $(OUT_DIR)/cicd-intro.pdf $(SRC_CICD)

watch:  ## Live-preview rhiza-intro in the browser while editing
	$(MARP) --watch --html $(SRC)

watch-deep-dive:  ## Live-preview rhiza-deep-dive in the browser while editing
	$(MARP) --watch --html $(SRC_DD)

watch-cicd:  ## Live-preview cicd-intro in the browser while editing
	$(MARP) --watch --html $(SRC_CICD)

clean:  ## Remove built artefacts
	rm -rf $(OUT_DIR)
