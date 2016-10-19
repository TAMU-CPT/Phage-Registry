// Copyright (c) 2014 Couchbase, Inc.
// Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file
// except in compliance with the License. You may obtain a copy of the License at
//   http://www.apache.org/licenses/LICENSE-2.0
// Unless required by applicable law or agreed to in writing, software distributed under the
// License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
// either express or implied. See the License for the specific language governing permissions
// and limitations under the License.
package main

import (
	"flag"
	"log"
	"net/http"
	"runtime"

	"github.com/gorilla/mux"
	"github.com/blevesearch/bleve"
	bleveHttp "github.com/blevesearch/bleve/http"
)

var batchSize = flag.Int("batchSize", 100, "batch size for indexing")
var bindAddr = flag.String("addr", ":8094", "http listen address")
var jsonDir = flag.String("jsonDir", "data/", "json directory")
var indexPath = flag.String("index", "phage-search.bleve", "index path")
var staticEtag = flag.String("staticEtag", "", "A static etag value.")
var staticPath = flag.String("static", "static/", "Path to the static content")

func main() {

	flag.Parse()

	log.Printf("GOMAXPROCS: %d", runtime.GOMAXPROCS(-1))

	// open the index
	phageIndex, err := bleve.Open(*indexPath)
	if err == bleve.ErrorIndexPathDoesNotExist {
		log.Printf("Creating new index...")
		// create a mapping
		indexMapping, err2 := buildIndexMapping()
		if err2 != nil {
			log.Fatal(err2)
		}
		phageIndex, err2 = bleve.New(*indexPath, indexMapping)
		if err2 != nil {
			log.Fatal(err2)
		}

		// index data in the background
		go func() {
			err = indexphage(phageIndex)
			if err != nil {
				log.Fatal(err)
			}
		}()
	} else if err != nil {
		log.Fatal(err)
	} else {
		log.Printf("Opening existing index...")
	}

	// create a router to serve static files
	router := mux.NewRouter()
	router.StrictSlash(true)


	// add the API
	bleveHttp.RegisterIndexName("phage", phageIndex)
	searchHandler := NewSearchHandler("phage")
	router.Handle("/phage-registry/api/search", searchHandler).Methods("POST")

	// static
	router.PathPrefix("/phage-registry/").Handler(http.StripPrefix("/phage-registry/",
		myFileHandler{http.FileServer(http.Dir(*staticPath))}))
	router.Handle("/", http.RedirectHandler("/phage-registry/index.html", 302))

	//start the HTTP server
	http.Handle("/phage-registry/", router)
	log.Printf("Listening on %v", *bindAddr)
	log.Fatal(http.ListenAndServe(*bindAddr, nil))
}
