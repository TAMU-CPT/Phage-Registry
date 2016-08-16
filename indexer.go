package main

import (
	"encoding/json"
	_ "expvar"
	"io/ioutil"
    "os"
	"log"
	"path/filepath"
	"strings"
	"time"

	"github.com/blevesearch/bleve"
)

func processDirEnt(dirEntry os.FileInfo, batchObj *bleve.Batch) (string, interface{}, error) {
    // read the bytes
    jsonBytes, err := ioutil.ReadFile(*jsonDir + "/" + dirEntry.Name())
    if err != nil {
        return "", nil, err
    }
    // parse bytes as json
    var jsonDoc interface{}
    err = json.Unmarshal(jsonBytes, &jsonDoc)
    if err != nil {
        return "", nil, err
    }

    filename := dirEntry.Name()
    ext := filepath.Ext(filename)
    docID := filename[:(len(filename) - len(ext))]
    return docID, jsonDoc, nil
}



func indexphage(i bleve.Index) error {

	// open the directory
	dirEntries, err := ioutil.ReadDir(*jsonDir)
	if err != nil {
		return err
	}

	// walk the directory entries for indexing
	log.Printf("Indexing...")
	count := 0
	startTime := time.Now()
	batch := i.NewBatch()
	batchCount := 0
	for _, dirEntry := range dirEntries {
		filename := dirEntry.Name()
		if !strings.HasSuffix(filename, ".json") {
			continue
		}

        docID, jsonDoc, err2 := processDirEnt(dirEntry, batch)
        if err2 != nil {
            return err2
        }

        batch.Index(docID, jsonDoc)
        batchCount++

        if batchCount >= *batchSize {
            err2 = i.Batch(batch)
            if err2 != nil {
                return err2
            }
            batch = i.NewBatch()
            batchCount = 0
        }

        count++
        if count%1000 == 0 {
            indexDuration := time.Since(startTime)
            indexDurationSeconds := float64(indexDuration) / float64(time.Second)
            timePerDoc := float64(indexDuration) / float64(count)
            log.Printf("Indexed %d documents, in %.2fs (average %.2fms/doc)", count, indexDurationSeconds, timePerDoc/float64(time.Millisecond))
        }
	}
	// flush the last batch
	if batchCount > 0 {
		err = i.Batch(batch)
		if err != nil {
			log.Fatal(err)
		}
	}
	indexDuration := time.Since(startTime)
	indexDurationSeconds := float64(indexDuration) / float64(time.Second)
	timePerDoc := float64(indexDuration) / float64(count)
	log.Printf("Indexed %d documents, in %.2fs (average %.2fms/doc)", count, indexDurationSeconds, timePerDoc/float64(time.Millisecond))
	return nil
}
