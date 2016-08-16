package main

import (
	"encoding/json"

	"github.com/blevesearch/bleve"
)

type retVal struct {
	Id  string `json:"id"`
	Phage string `json:"phage"`
	Host string `json:"host"`
	Url string `json:"url"`
}

func getBleveDocsFromSearchResults(results *bleve.SearchResult, index bleve.Index) []byte {
	docs := make([]retVal, 0)

	for _, val := range results.Hits {
		doc, _ := index.Document(val.ID)
		rv := &retVal{}
		for _, field := range doc.Fields {
			switch field.Name() {
			case "id":
				rv.Id = string(field.Value())
			case "phage":
				rv.Phage = string(field.Value())
			case "host":
				rv.Host = string(field.Value())
			case "urls":
				rv.Url = string(field.Value())
			}
		}
		docs = append(docs, *rv)
	}

	j2, _ := json.Marshal(docs)
	return j2
}
