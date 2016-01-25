/**
 * Created by James Kane on 10/31/2015.
 */

(function () {
  'use strict';

  angular
    .module('capes.authentication', [
      'capes.authentication.controllers',
      'capes.authentication.services'
    ]);

  angular
    .module('capes.authentication.controllers', []);

  angular
    .module('capes.authentication.services', ['ngCookies']);
})();