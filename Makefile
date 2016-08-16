run: phage-registry kill_cache
	./phage-registry

kill_cache:
	rm -rf phage-search.bleve

download_data: kill_data
	python data/process.py

kill_data:
	rm -f data/*.json

phage-registry: http_util.go indexer.go main.go mapping.go search.go serialization.go util.go
	go build .

gofmt:
	goimports -w $$(find . -type f -name '*.go' -not -path "./vendor/*")
	gofmt -w $$(find . -type f -name '*.go' -not -path "./vendor/*")

qc_deps:
	go get github.com/alecthomas/gometalinter
	gometalinter --install --update

qc:
	gometalinter --cyclo-over=10 --deadline=30s  ./...


update_date:
	sed -i "s|<span id=\"date\">.*</span>|<span id=\"date\">$(shell date --rfc-3339=seconds)</span>|" static/partials/overview.html

build_for_release:
	$(MAKE) download_data
	$(MAKE) update_date
	$(MAKE) phage_registry
	tar cvfj release.tar.bz2 phage-registry data static
