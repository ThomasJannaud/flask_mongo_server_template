var ngApp = angular.module('ngApp', []);
ngApp.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[{[');
    $interpolateProvider.endSymbol(']}]');
});

ngApp.controller('ngController', ['$scope', '$http', function($scope, $http) {
    // These 2 bools control wether the signup/login panels are shown.
    // At any time, at most one of them is true.
    $scope.isLogin = false;
    $scope.isSignup = false;

    // ------------- Signup controller ---------------
    $scope.signup = {
        user_info: {
            email: "",
            password: "",
            first_name: "",
            last_name: "",
            phone_number: ""
        }
    };
    $scope.card = {
        number: "",
        cvc: "",
        exp_month: 1,
        exp_year: 2015
    }

    $scope.selectMonth = function(index) {
        $scope.card.exp_month = index + 1;
    };

    $scope.selectYear = function(index) {
        $scope.card.exp_year = 2015 + index;
    };

    $scope.trySignup = function() {
        // does email already exist ? if not, try create stripe token.
        $http.get("/api/v1/check-new-email?email=" + $scope.signup.user_info.email)
            .error(function(data, status, headers, config) {
                alert('An account already exists for this email.');
            })
            .success(function(data, status, headers, config) {
                // get stripe single use token.
                // on success of stripe response : finalize signup, else say we have bad card number.
                Stripe.card.createToken($scope.card, 
                    function(status, response) {
                        // Stripe Token creation callback. If successful, tries to register on our
                        // website. If registration successful, redirect to /products.
                        if (response.error) {
                            alert(response.error.message);
                        } else {
                            $scope.signup.stripe_token = response.id;
                            $http.post("/api/v1/register", $scope.signup)
                                .success(function(jsonData, status, headers, config) {
                                    window.location.href = "/products";
                                })
                                .error(function(jsonData, status, headers, config) {
                                    alert('Error in account creation. Please contact us if you have any problem : info@opinionazer.com');
                                });
                        }
                    }
                );
            });
    }

    // ------------- Login controller ---------------
    $scope.login = {
        email: "",
        password: "",
        remember: false        
    }

    $scope.tryLogin = function() {
        $http.post("/api/v1/login", $scope.login)
            .success(function(jsonData, status, headers, config) {
                window.location.href = "/products";
            })
            .error(function(jsonData, status, headers, config) {
                alert('Cant connect. Sign up, use the forget your password functionality or contact us if you have any problem.');
            });
    }


    $scope.forgotPassword = function() {
        if (!$scope.login.email) {
            alert('Email missing');
            return;
        }
        $http.get("/api/v1/forgot_password?email=" + $scope.login.email)
            .success(function(jsonData, status, headers, config) {
                alert('Email succesfully sent');
            })
            .error(function(jsonData, status, headers, config) {
                alert('Could not send the password to the specified email. Account may not exist.');
            });
    }
}]);