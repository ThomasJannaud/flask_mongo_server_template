var ngApp = angular.module('ngApp', []);
ngApp.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[{[');
    $interpolateProvider.endSymbol(']}]');
});

ngApp.controller('ngHomeController', ['$scope', '$http', function($scope, $http) {
    // cannot submit more than 1 request at a time.
    $scope.isLoading = false;
    $scope.signup = {
        user_info: {
            email: "",
            password: "",
        }
    };
    $scope.login = {
        email: "",
        password: "",
        remember: false        
    };
    // ="" if anonymous, else user mail address if logged in.
    // This is passed in from html
    $scope.logged_in_as = "";

    $scope.init = function(logged_in_as) {
        $scope.logged_in_as = logged_in_as;
    }

    $scope.trySignup = function() {
        // does email already exist ? if not, register
        $scope.isLoading = true;
        $http.get("/api/v1/check-new-email?email=" + $scope.signup.user_info.email)
            .error(function(data, status, headers, config) {
                $scope.isLoading = false;
                alert('An account already exists for this email.');
            })
            .success(function(data, status, headers, config) {
                $http.post("/api/v1/register", $scope.signup)
                    .success(function(jsonData, status, headers, config) {
                        $scope.isLoading = false;
                        $scope.logged_in_as = $scope.signup.user_info.email;
                        alert('Sign up successful');
                    })
                    .error(function(jsonData, status, headers, config) {
                        $scope.isLoading = false;
                        alert('Error in account creation. Please contact us if you have any problem');
                    });
            });
    }

    $scope.logout = function() {
        $http.get("/api/v1/logout")
            .success(function(jsonData, status, headers, config) {
                $scope.isLoading = false;
                $scope.logged_in_as = "";
                alert('Logged out ok!');
            })
            .error(function(jsonData, status, headers, config) {
                $scope.isLoading = false;
                alert('Cant log out.');
            });
    }

    $scope.tryLogin = function() {
        $scope.isLoading = true;
        $http.post("/api/v1/login", $scope.login)
            .success(function(jsonData, status, headers, config) {
                $scope.isLoading = false;
                $scope.logged_in_as = $scope.login.email;
                alert('Login ok!');
            })
            .error(function(jsonData, status, headers, config) {
                $scope.isLoading = false;
                alert('Cant login. Sign up, use the forget your password functionality or contact us if you have any problem.');
            });
    }
}]);