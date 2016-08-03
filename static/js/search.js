function SearchCtrl($scope, $http, $routeParams, $log, $sce) {

    $scope.field = 'id';
    $scope.prefix_length = "0";
    $scope.fuzziness = "0";

    $scope.minShouldOptions = [];
    for (var i = 0; i <= 50; i++) {
            $scope.minShouldOptions[i] = i;
    }

    var resetSchema = function() {
        $scope.phraseTerm = "";
        $scope.clauseTerm = "";
        $scope.clauseOccur = "MUST";
        $scope.clauseBoost = 1.0;
    };

    $scope.searchTerm = function() {
        $http.post('/api/search', {
			"size": 20,
			"explain": true,
			"highlight":{},
			"query": {
				"term": $scope.term,
				"field": $scope.field,
			}
        }).
        success(function(data) {
            $scope.processResults(data);
        }).
        error(function(data, code) {

        });
    };

    $scope.expl = function(explanation) {
            rv = "" + $scope.roundScore(explanation.value) + " - " + explanation.message;
            rv = rv + "<ul>";
            for(var i in explanation.children) {
                    child = explanation.children[i];
                    rv = rv + "<li>" + $scope.expl(child) + "</li>";
            }
            rv = rv + "</ul>";
            return rv;
    };

    $scope.roundScore = function(score) {
            return Math.round(score*1000)/1000;
    };

    $scope.roundTook = function(took) {
        if (took < 1000 * 1000) {
            return "less than 1ms";
        } else if (took < 1000 * 1000 * 1000) {
            return "" + Math.round(took / (1000*1000)) + "ms";
        } else {
            roundMs = Math.round(took / (1000*1000));
            return "" + roundMs/1000 + "s";
        }
	};

    $scope.removePhraseTerm = function(index) {
        $scope.phraseTerms.splice(index, 1);
    };

    $scope.addPhraseTerm = function() {
        if($scope.phraseTerm === "") {
                //$scope.errorMessage = "Phrase term cannot be empty";
                //return;
                $scope.phraseTerms.push(null);
        }else {

        $scope.phraseTerms.push($scope.phraseTerm);
    }

        // reset form
        delete $scope.errorMessage;
        resetSchema();
    };

    $scope.processResults = function(data) {
        $scope.errorMessage = null;
        $scope.results = data;
        for(var i in $scope.results.hits) {
                hit = $scope.results.hits[i];
                hit.roundedScore = $scope.roundScore(hit.score);
                hit.explanationString = $scope.expl(hit.explanation);
                hit.explanationStringSafe = $sce.trustAsHtml(hit.explanationString);
                for(var ff in hit.fragments) {
                    fragments = hit.fragments[ff];
                    newFragments = [];
                    for(var ffi in fragments) {
                        fragment = fragments[ffi];
                        safeFragment = $sce.trustAsHtml(fragment);
                        newFragments.push(safeFragment);
                    }
                    hit.fragments[ff] = newFragments;
                }
        }
        $scope.results.roundTook = $scope.roundTook(data.took);
    };

    $scope.searchPhrase = function() {
        delete $scope.results;
        if($scope.phraseTerms.length < 1) {
                $scope.errorMessage = "Query requires at least one term";
                return;
        }
        var requestBody = {
                "query": {
                        "terms": [],
                        "boost": 1.0,
                },
                "highlight":{},
                explain: true,
                size: parseInt($scope.size, 10)
        };
        for(var i in $scope.phraseTerms) {
                var term = $scope.phraseTerms[i];
                if (term !== null) {
                    var termQuery = {
                        "term": term,
                        "field": $scope.phraseField,
                        "boost": 1.0,
                    };
                    requestBody.query.terms.push(termQuery);
                } else {
                    requestBody.query.terms.push(null);
                }

        }

        $http.post('/api/search', requestBody).
        success(function(data) {
            $scope.processResults(data);
        }).
        error(function(data, code) {
                $scope.errorMessage = data;
                return;
        });
    };


}
