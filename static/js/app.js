'use strict';


// Declare app level module which depends on filters, and services
angular.module('myApp', [
  'ngRoute',
]).config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {

    $routeProvider.when('/phage-registry/', {
        templateUrl: '/phage-registry/partials/overview.html',
        controller: 'SearchCtrl'
    });

    $routeProvider.otherwise({redirectTo: '/phage-registry/'});
    $locationProvider.html5Mode(true);
}]);
