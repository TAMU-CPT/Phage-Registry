package main

import (
	"encoding/json"
	"fmt"

	"github.com/blevesearch/bleve"
)

type retVal struct {
	Id  string `json:"id"`
	Typ string `json:"typ"`
	Url string `json:"url"`
}

func getBleveDocsFromSearchResults(results *bleve.SearchResult, index bleve.Index) []byte {
	docs := make([]retVal, 0)

	for _, val := range results.Hits {
		doc, _ := index.Document(val.ID)
		fmt.Printf("Doc %#v\n", doc)

		rv := &retVal{}
		for _, field := range doc.Fields {
			switch field.Name() {
			case "id":
				rv.Id = string(field.Value())
			case "typ":
				rv.Typ = string(field.Value())
			case "url":
				rv.Url = string(field.Value())
			}
		}
		docs = append(docs, *rv)
	}

	j2, _ := json.Marshal(docs)
	return j2
}
