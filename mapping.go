//  Copyright (c) 2014 Couchbase, Inc.
//  Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file
//  except in compliance with the License. You may obtain a copy of the License at
//    http://www.apache.org/licenses/LICENSE-2.0
//  Unless required by applicable law or agreed to in writing, software distributed under the
//  License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
//  either express or implied. See the License for the specific language governing permissions
//  and limitations under the License.

// +build !example1
// +build !example2

package main

import (
	"github.com/blevesearch/bleve"
	"github.com/blevesearch/bleve/analysis/lang/en"
)

func buildIndexMapping() (*bleve.IndexMapping, error) {
	phageMapping := bleve.NewDocumentMapping()

	// a generic reusable mapping for english text
	englishTextFieldMapping := bleve.NewTextFieldMapping()
	englishTextFieldMapping.Analyzer = en.AnalyzerName

    // RO
    storeFieldOnlyMapping := bleve.NewTextFieldMapping()
    storeFieldOnlyMapping.Index = false
    storeFieldOnlyMapping.IncludeTermVectors = false
    storeFieldOnlyMapping.IncludeInAll = false

	phageMapping.AddFieldMappingsAt("id", englishTextFieldMapping)
	phageMapping.AddFieldMappingsAt("phage", englishTextFieldMapping)
	phageMapping.AddFieldMappingsAt("host", englishTextFieldMapping)
	phageMapping.AddFieldMappingsAt("urls", storeFieldOnlyMapping)

	indexMapping := bleve.NewIndexMapping()
	indexMapping.AddDocumentMapping("phage", phageMapping)

	indexMapping.TypeField = "type"
	indexMapping.DefaultAnalyzer = "en"

	return indexMapping, nil
}
