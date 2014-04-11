/*jslint nomen: true*/
/*global d3, angular, _, console*/

var app = angular.module('app', ['ngAnimate', 'chieffancypants.loadingBar']);

function randomBoard() {
  "use strict";
  var b = [],
    i = 0;
  for (i; i < 30; i += 1) {
    b.push(_.random(1, 6));
  }
  return b;
}

function emptyBoard() {
  "use strict";
  var b = [],
    i = 0;
  for (i; i < 30; i += 1) {b.push(0);}
  return b;
}

app.directive('pndgrid', function () {
  "use strict";
  return {
    restrict: 'E',
    scope: {
      board: '=',
      paths: '='
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
          .attr('preserveAspectRatio', 'xMinYMin'),

        orblayer = svg.append('g').attr('class', 'orbslayer'),
        pathlayer = svg.append('g').attr('class', 'pathlayer');

      svg.append('marker')
        .attr({
          id: 'arrow',
          markerWidth: 4,
          markerHeight: 4,
          orient: "auto",
          viewBox: "-3 -3 6 6"
          }).append('polygon').attr('points', '-1,0 -3,3 3,0 -3,-3');


      var line = d3.svg.line()
        .x(function (d) {
          return d[0] * orbsize + orbsize/2;
        })
        .y(function (d) {
          return d[1] * orbsize + orbsize/2;
        })
        .interpolate("linear");

      scope.$watch('paths', function(newVal, oldVal) {

        var paths = pathlayer.selectAll('path')
          .data(newVal);

        paths.enter()
          .append('path');

        paths
          .attr('d', line)
          .attr('marker-end', "url(#arrow)");

        paths.exit()
          .remove();
      });

      scope.$watch('board', function (newVal, oldVal) {
        console.log('update!');

        var orbs = orblayer.selectAll('circle')
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
          .duration(function () {return _.random(300, 700); });
        orbs.exit().transition()
          .remove();
      });
    }
  };
});


app.controller('PndCtrl', function PndCtrl($scope, $http) {
  "use strict";

  $scope.board = emptyBoard();
  $scope.paths = [];
  $scope.frame = "";

  $scope.parameters = {
    depth: 6
  };

  $scope.team = {
    hl: null,
    fr: null,
    wd: null,
    wt: null,
    dk: null,
    lt: null
  }

  $scope.solutions = [];

  $scope.capture = function () {
    $scope.board = [];
    $scope.paths = [];
    $http.get('/capture').success(function(data) {
      $scope.frame = data.frame;
      $scope.board = data.board;
    });
  };

  $scope.solve = function() {
    $scope.solutions = [];
    $http.post('/solve', {board: $scope.board}).success(function(data) {
      $scope.solutions = data;
    });
  };

  $scope.run = function(path) {
    console.log("running solution" + path);
  };

  $scope.show = function(path) {
    console.log("showing solution" + path);
    $scope.paths = [path];
  };

  $scope.hasSolutions = function() {
    return $scope.solutions.length > 0;
  };

  $scope.calculateDamage = function(solution) {
    return $scope.team.hl + 1;
  }

});