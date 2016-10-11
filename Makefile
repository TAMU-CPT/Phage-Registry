run: phage-registry kill_cache  ## compile, re-index, and run the phage registry
	./phage-registry

kill_cache: ## Remove any cached bleve indexes
	rm -rf phage-search.bleve

download_data: kill_data ## Download fresh data
	python data/process.py

kill_data: ## Remove cached data
	rm -f data/*.json

phage-registry: http_util.go indexer.go main.go mapping.go search.go serialization.go util.go ## Compile the phage registry
	go build -o phage-registry .

gofmt: ## Reformat files
	goimports -w $$(find . -type f -name '*.go' -not -path "./vendor/*")
	gofmt -w $$(find . -type f -name '*.go' -not -path "./vendor/*")

qc_deps:
	go get github.com/alecthomas/gometalinter
	gometalinter --install --update

qc:
	gometalinter --cyclo-over=10 --deadline=30s  ./...

update_date: ## Update the date in the HTML file. Used mainly in deployments
	sed -i "s|<span id=\"date\">.*</span>|<span id=\"date\">$(shell date -Iseconds)</span>|" static/partials/overview.html

build_for_release: ## Build a release of the software
	$(MAKE) download_data
	$(MAKE) update_date
	$(MAKE) phage_registry
	tar cvfj release.tar.bz2 phage-registry data static

.PHONY: help

help:
	@egrep '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
