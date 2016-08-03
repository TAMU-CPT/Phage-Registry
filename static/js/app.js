'use strict';


// Declare app level module which depends on filters, and services
angular.module('myApp', [
  'ngRoute',
]).config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {

    $routeProvider.when('/overview', {
        templateUrl: '/static/partials/overview.html',
        controller: 'SearchCtrl'
    });

    $routeProvider.otherwise({redirectTo: '/overview'});
    $locationProvider.html5Mode(true);
}]);
