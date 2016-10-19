//  Copyright (c) 2014 Couchbase, Inc.
//  Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file
//  except in compliance with the License. You may obtain a copy of the License at
//    http://www.apache.org/licenses/LICENSE-2.0
//  Unless required by applicable law or agreed to in writing, software distributed under the
//  License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
//  either express or implied. See the License for the specific language governing permissions
//  and limitations under the License.

package main

import (
	"io/ioutil"
	"log"
	"net/http"
)

func showError(w http.ResponseWriter, r *http.Request,
	msg string, code int) {
	logger.Printf("Reporting error %v/%v", code, msg)
	http.Error(w, msg, code)
}

type varLookupFunc func(req *http.Request) string

var logger = log.New(ioutil.Discard, "bleve.http", log.LstdFlags)

