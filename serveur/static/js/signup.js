var signupApp = angular.module('signupApp', []);

signupApp.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('[{[');
    $interpolateProvider.endSymbol(']}]');
});

signupApp.controller('signupController', ['$scope', '$http', function ($scope, $http) {
    $scope.isBillingMonthly = false;

    $scope.countriesList = utils_getCountriesButAll();
    $scope.sectorList = utils_Sectors();
    $scope.numberList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    $scope.hardwareNumberList = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    $scope.monthList = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    $scope.yearList = [2015, 2016, 2017, 2018, 2019, 2020];
    $scope.utils_getCountryById = utils_getCountryById;

    $scope.signup = {
        user_info: {
            email: "",
            password: "",
            first_name: "",
            last_name: "",
            phone_number: "",
            "function": ""
        },
        account: {
            company_info: {
                company_name: "",
                sector: 0,
                address: "",
                zip_code: "",
                city: "",
                country: 1  // USA
            },
            plan: {
                billing: 0,  // 0: monthly, 1: annual
                hardware: 0,
                max_checkpoints_allowed: 1
            }
        },
    };
    $scope.card = {
        number: "",
        cvc: "",
        exp_month: 1,
        exp_year: 2015
    }

    $scope.subTotal = {
        licenses: 0,
        checkpoints: 0,
        discount: 0,
        total: 0
    };

    $scope.switchBilling = function (val) {
        $scope.signup.account.plan.billing = val;
    }

    $scope.selectCountry = function (countryId) {
      $scope.signup.account.company_info.country = countryId;
    }

    $scope.selectSector = function (index) {
        $scope.signup.account.company_info.sector = index;
    };

    $scope.selectMonth = function (index) {
        $scope.card.exp_month = index + 1;
    };

    $scope.selectYear = function (index) {
        $scope.card.exp_year = 2015 + index;
    };

    $scope.selectCheckpoints = function (val) {
        $scope.signup.account.plan.max_checkpoints_allowed = val;
    };

    $scope.$watch("signup.account.plan", function () {
        var checkpoints = $scope.signup.account.plan.hardware;
        var monthlyWithoutDiscount = checkpoints * 99;
        var hardwareWithoutDiscount = checkpoints * 250;
        var totalWithoutDiscount = monthlyWithoutDiscount + hardwareWithoutDiscount;
        if ($scope.signup.account.plan.billing === 0) {
            $scope.subTotal.discount = 0;
            $scope.subTotal.licenses = hardwareWithoutDiscount;
            $scope.subTotal.checkpoints = monthlyWithoutDiscount;
        } else {
            $scope.subTotal.licenses = hardwareWithoutDiscount;
            $scope.subTotal.checkpoints = monthlyWithoutDiscount * 0.82;
        }
        $scope.subTotal.total = $scope.subTotal.licenses + $scope.subTotal.checkpoints;
        if ($scope.signup.account.plan.billing === 1) {
            $scope.subTotal.discount = totalWithoutDiscount - $scope.subTotal.total;
        }
    }, true);

    $scope.trySignup = function () {
        // does email already exist ? if not, try create stripe token.
        $http.get("/api/v1/check-new-email?email=" + $scope.signup.user_info.email)
            .success(function (data, status, headers, config) {
                // get stripe single use token.
                // on success of stripe response : finalize signup, else say we have bad card number.
                Stripe.card.createToken($scope.card, $scope.stripeResponseHandler);
            })
            .error(function (data, status, headers, config) {
                alert('An account already exists for this email. If you have lost your password please contact us.');
            });
    }

    $scope.stripeResponseHandler = function (status, response) {
        // Stripe Token creation callback. If successful, tries to register on our
        // website. If registration successful, redirect to /functions.
        if (response.error) {
            alert(response.error.message);
        } else {
            $scope.signup.stripe_token = response.id;
            $http.post("/api/v1/register", $scope.signup)
                .success(function (jsonData, status, headers, config) {
                    // data is account_id
                    window.location.href = "/en/functions?account_id=" + jsonData;
                })
                .error(function (jsonData, status, headers, config) {
                    alert('Error in account creation. Please contact us if you have any problem : info@opinionazer.com');
                });
        }
    }

}]);