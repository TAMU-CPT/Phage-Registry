run: phage-registry
	./phage-registry


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
