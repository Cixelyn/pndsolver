/*jslint nomen: true*/
/*global d3, angular, _, console*/

var app = angular.module('app', []);
var board = [2, 1, 4, 3, 4, 1, 1, 1, 3, 3, 3, 5, 2, 5, 3, 4, 3, 4, 1, 4, 4, 3, 4, 3, 1, 5, 3, 1, 3, 5];

function randomBoard() {
  "use strict";
  var b = [],
    i = 0;
  for (i; i < 30; i += 1) {
    b.push(_.random(1, 6));
  }
  return b;
}

app.directive('pndgrid', function () {
  "use strict";
  return {
    restrict: 'E',
    scope: {
      board: '='
    },
    link: function (scope, element, attrs) {

      var orbsize = 15,
        width = orbsize * 6,
        height = orbsize * 5,

        svg = d3.select(element[0]).append("svg")
          .attr('width', "100%")
          .attr('height', "100%")
          .style('max-height', '600px')
          .attr('viewBox', '0 0 ' + Math.max(width, height) + ' ' + Math.max(width, height))
          .attr('preserveAspectRatio', 'xMinYMin');

      scope.$watch('board', function (newVal, oldVal) {
        console.log('update!');

        var orbs = svg.selectAll('circle')
          .data(newVal);

        orbs.enter()
          .append('circle')
          .attr('cx', function (d, i) {return (i % 6) * orbsize + orbsize / 2; })
          .attr('cy', function (d, i) {return Math.floor(i / 6) * orbsize + orbsize / 2; })
          .attr('r', 0);

        orbs
          .attr('class', function (d) {return 'orb-' + d; });

        orbs.transition()
          .attr('r', orbsize / 2)
          .duration(function () {return _.random(500, 1000); });
        orbs.exit().transition()
          .remove();
      });
    }
  };
});

app.controller('PndCtrl', function PndCtrl($scope) {
  "use strict";

  $scope.board = randomBoard();
  $scope.solutions = [
    {damage: 2, combos: 2},
    {damage: 3, combos: 1},
    {damage: 6, combos: 1}
  ];

  $scope.capture = function () {
    $scope.board = randomBoard();
  };

});