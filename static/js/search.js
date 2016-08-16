function SearchCtrl($scope, $http, $routeParams, $log, $sce) {

    $scope.field = 'id';
    $scope.prefix_length = "0";
    $scope.fuzziness = "0";
    $scope.queried = false;

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
        $http.post('/phage-registry/api/search', {
            "size": 60,
            "explain": true,
            "highlight":{},
            "query": {
                "match": $scope.term,
                "field": $scope.field,
                "prefix_length": 20,
                "fuzziness": 20,
            }
        }).
        success(function(data) {
            $scope.queried = true;
            $scope.errorMessage = null;
            $scope.results = [];

            if(data && data !== "null"){
                $scope.results = data.map(function (x){
                    x.url = JSON.parse(x.url)
                    return x;
                });
            }
        }).
        error(function(data, code) {

        });
    };
}
