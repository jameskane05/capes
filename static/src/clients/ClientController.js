(function(){

angular.module('clients')
    .controller('ClientController', [
        '$mdSidenav',
        '$mdBottomSheet',
        '$mdToast',
        '$mdDialog',
        '$log',
        '$q',
        'Restangular',
        ClientController
    ]);

    function ClientController( $mdSidenav, $mdBottomSheet, $mdToast, $mdDialog, $log, $q, Restangular) {
        var self = this;

        self.clients = [];
        self.selected = null;
        self.new_client = null;
        self.work = [];
        self.selected_work = null;
        self.new_work = null;
        self.clients.exp_date = new Date(self.clients.exp_date);
        self.addClientDialog = addClientDialog;
        self.addClientDialogController = addClientDialogController;
        self.addWorkDialog = addWorkDialog;
        self.addWorkDialogWontroller = addWorkDialogController;
        self.emailClientPanel = emailClientPanel;
        self.emailClientPanelController = emailClientPanelController;
        //self.minDate = new Date();

        self.reloadPage = function () {
            window.location.reload();
        };

        self.logout = function (data) {
            $.post({
                    url: '/api-auth/logout/',
                    data: data
                });
        }

        //  Loading all Clients through Restangular all() and getList() requests,
        //  then acting on the data received
        self.getClients = function() {
            Restangular.all('clients').getList().then(function (clients) {
                self.clients = [].concat(clients);
                self.selected = self.clients[0];
            });
        };

        self.getWork = function() {
            Restangular.all('work').getList().then(function (work) {
                self.work = [].concat(work);
                self.selected_work = self.work[0];
            })
        };

        self.getNewClient = function() {
            Restangular.all('clients').getList().then(function (clients) {
                self.clients = [].concat(clients);
                self.selected = self.clients[self.clients.length - 1];
            });
        };

        self.getNewWork = function() {
            Restangular.all('work').getList().then(function (work) {
                self.work = [].concat(work);
                self.selected_work = self.work[self.work.length - 1];
            });
        };

        // Select a client from the menu
        self.selectClient = function (client) {
            self.selected = angular.isNumber(client) ? $scope.clients[client] : client;
            self.toggleClientList();
        };

        // Select a work sample from the menu
        self.selectWork = function (work) {
            self.selected_work = angular.isNumber(work) ? $scope.work[work] : work;
            self.toggleClientList();
        };

        // First hide the bottomsheet IF visible, then hide or Show the 'left' sideNav area
        self.toggleClientList = function() {
            var pending = $mdBottomSheet.hide() || $q.when(true);

            pending.then(function () {
                $mdSidenav('left').toggle();
            });
        };

        // A function to delete the selected client
        self.deleteSelected = function () {
            self.selected.remove().then(function(){
                self.clients = self.getClients();
                $mdToast.show(
                    $mdToast.simple()
                        .content('Client deleted')
                        .hideDelay(3000)
                )
            });
        };

        self.deleteSelectedWork = function () {
            self.selected_work.remove().then(function(){
                self.work = self.getWork();
                $mdToast.show(
                    $mdToast.simple()
                        .content('Work sample deleted')
                        .hideDelay(3000)
                )
            });
        };

        self.setExpDate = function(data) {
            var new_exp_date = data.toISOString();
            self.selected.exp_date = new_exp_date;
            self.selected.put();
            $mdToast.show(
                    $mdToast.simple()
                        .content('Expiration date updated for ' + self.selected.name)
                        .hideDelay(3000)
                );
        };

        // Run getClients() to query the DRF endpoint and update the frontend
        self.getClients();
        self.getWork();

        /**
         * Show the form to add clients on a dialog sheet
         */
        function addClientDialog($event) {
            $mdBottomSheet.hide();
            $mdDialog.show({
                controller: addClientDialogController,
                templateUrl: './static/assets/addclient.tmpl.html',
                parent: angular.element(document.body),
                targetEvent: $event,
                clickOutsideToClose: true
            })
        }

        function addClientDialogController($scope, $mdDialog) {
            $scope.minDate = new Date();
            $scope.hide = function(){$mdDialog.hide();};
            $scope.cancel = function(){$mdDialog.cancel();};
            $scope.createClient = function (data) {
                /*  exp_date is a JS Date object by default thanks to md-datepicker.
                *   Check if the the user entered a date w/ this method - if so, change it
                *   to an ISO-compliant string, which Django REST Framework can understand.
                *   Otherwise submit the null value and the serializer will use the default. */
                if (data.exp_date != null) {
                    data.exp_date = data.exp_date.toISOString();
                };

                /*  Make a post requests to the Django REST Framework endpoint for client
                *   creation. On success, hide the dialog, update the client list and select the new user */
                $.post({
                    url: '/clients',
                    data: data,
                    success: function () {
                        $scope.hide();
                        self.getNewClient();
                        $mdToast.show(
                            $mdToast.simple()
                                .content('Client created')
                                .hideDelay(3000)
                        )
                    }
                });
            };
        };

        function addWorkDialog($event) {
            $mdDialog.show({
                controller: addWorkDialogController,
                templateUrl: './static/assets/addwork.tmpl.html',
                parent: angular.element(document.body),
                targetEvent: $event,
                clickOutsideToClose: true
            })
        };

        function addWorkDialogController($scope, $mdDialog, Upload) {
            $scope.hide = function(){$mdDialog.hide();};
            $scope.cancel = function(){$mdDialog.cancel();};
            $scope.createWork = function(data) {

                console.log(data);
                data['tags'] = data['tags'].split(/\s*,\s*/);
                console.log(data);
                var fd = new FormData();

                for (key in data) { fd.append(key, data[key]); }

                Restangular.all('work')
                    .withHttpConfig({transformRequest: angular.identity})
                    .customPOST(fd, undefined, undefined, {'Content-Type': undefined})
                    .then(function(){
                        $scope.hide();
                        self.getNewWork();
                        $mdToast.show(
                            $mdToast.simple()
                                .content('Work sample created')
                                .hideDelay(3000)
                        )
                    })
            }
        };

        /**
         * Show the email panel bottom sheet
         */
        function emailClientPanel(selected) {
            var client = self.selected;
            return $mdBottomSheet.show({
                parent: angular.element(document.getElementById('content')),
                templateUrl: './static/src/clients/view/emailPanel.html',
                controller: emailClientPanelController,
                bindToController : true,
                clickOutsideToClose: true
            })
        };

        function emailClientPanelController($scope, $mdBottomSheet) {

            $scope.selected = self.selected;
            $scope.emailData = {};
            $scope.emailData.email_subject = 'Lelander work samples';
            $scope.emailData.custom_email_text = '';
            $scope.hide = function () {
                $mdBottomSheet.hide();
            };

            $scope.emailClient = function(data) {
                var id = self.selected.id;
                $scope.hide();
                $.ajax({
                    type: "POST",
                    url: '/email_client',
                    data: {
                        'id': id,
                        'email_subject': data.email_subject,
                        'custom_email_text': data.custom_email_text
                    },
                    success: $mdToast.show(
                        $mdToast.simple()
                            .content('Email sent to ' + self.selected.email)
                            .hideDelay(3000)
                        )
                });
            };
        }
    }
})()


    // JUNK CODE JUNK CODE JUNK CODE
    // JUNK CODE JUNK CODE JUNK CODE
    // JUNK CODE JUNK CODE JUNK CODE

    /*  $mdDateLocaleProvider config settings - may or may not need. Saving.

    .config(function($mdDateLocaleProvider) {
        $mdDateLocaleProvider.parseDate = function(date) {
            return moment(date).format('MM-DD-YYYY HH:MM:SS');
        }
        $mdDateLocaleProvider.formatDate = function(date) {
            return moment(date).format('MM-DD-YYYY HH:MM:SS');
        }
    });
    */