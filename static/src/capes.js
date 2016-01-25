
angular.module('capes', ['ngMaterial',
                         'ngMdIcons',
                         'ngRoute',
                         'ngMessages',
                         'clients'])
    .config(function($mdThemingProvider, $mdIconProvider){

      $mdIconProvider
          .defaultIconSet("./static/assets/svg/avatars.svg", 128)
          .icon("menu"       , "./static/assets/svg/menu.svg"        , 24)
          .icon("share"      , "./static/assets/svg/share.svg"       , 24);

          $mdThemingProvider.theme('default')
              .primaryPalette('brown')
              .accentPalette('red');

    });
