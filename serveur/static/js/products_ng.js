var ngApp = angular.module('ngApp', []);

ngApp.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('[{[');
  $interpolateProvider.endSymbol(']}]');
});

ngApp.controller('ngApp', ['$scope', '$http', function($scope, $http) {
  $scope.products = [];  // list of Product
  $scope.sendingData = false;

  $http.get("/api/v1/products/all")
    .success(function(jsonData, status, headers, config) {
      $scope.products = jsonData;
    })
    .error(function(data, status, headers, config) {
      alert('Could not load page. Check internet connection or contact us.');
    });


  $scope.savePermissions = function () {
    $scope.sendingData = true;
    $http.post("/api/v1/permissions?" + utils_getAccountQueryParam(), $scope.permissions)
        .success(function () {
          $scope.sendingData = false;
        })
        .error(function () {
          $scope.sendingData = false;
        });
  }
}]);