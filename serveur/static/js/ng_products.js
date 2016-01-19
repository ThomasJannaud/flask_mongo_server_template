var ngApp = angular.module('ngApp', []);

ngApp.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[{[');
    $interpolateProvider.endSymbol(']}]');
});

ngApp.controller('ngController', ['$scope', '$http', function($scope, $http) {
    $scope.products = [];  // list of Product
    $scope.sendingData = false;
    $scope.new_product = {name: "", quantity: 0};

    $http.get("/api/v1/products/all")
        .success(function(jsonData, status, headers, config) {
            $scope.products = jsonData;
        })
        .error(function(data, status, headers, config) {
            alert('Could not load page. Check internet connection or contact us.');
        });

    $scope.addProduct = function() {
        $scope.products.push($scope.new_product);
        $scope.new_product = {name: "", quantity: 0};
    }

    $scope.deleteProduct = function($index) {
        $scope.products.splice($index, 1);
    }

    $scope.save = function() {
        $scope.sendingData = true;
        $http.post("/api/v1/products/save", $scope.products)
            .success(function () {
                $scope.sendingData = false;
            })
            .error(function () {
                $scope.sendingData = false;
            });
    }        
}]);