/*jslint nomen: true*/
/*global d3, angular, _, console*/


_.mixin({
  sum: function(obj, iterator, context) {
    if (!iterator && _.isEmpty(obj)) return 0;
    var result = 0;
    if (!iterator && _.isArray(obj)) {
      for (var i = obj.length - 1; i > -1; i -= 1) {
        result += obj[i];
      }
      return result;
    }
    _.each(obj, function (value, index, list) {
      var computed = iterator ? iterator.call(context, value, index, list) : value;
      result += computed;
    });
    return result;
  }
});


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

  function baseColorMultiplier(singleComboList) {
    return _.chain(singleComboList)
      .map(function(c) {return 1 + (c-3) * 0.25})
      .sum()
      .value();
  }

  function baseComboMultiplier(combos) {
    var count = _.chain(combos)
      .values()
      .map(function(c) {return c.length})
      .sum()
      .value();
    return 1 + (count - 1) * 0.25;
  }

  $scope.calculateDamage = function(solution) {
    var comboX = baseComboMultiplier(solution.combos);

    var dmg = _.chain(['1', '2',' 3', '4', '5'])
      .map(function(c) {return solution.combos[c];})  // have the combo count
      .map(baseColorMultiplier)
      .map(function(x, i) {
        return $scope.team[$scope.indexToAbbr(i+1)] * x * comboX;
      })
      .sum()
      .value();

    if(dmg === 0) {
      return '-'
    } else {
      return Math.floor(dmg);
    }
  };

  $scope.calculateRecovery = function(solution) {
    var baseX = baseColorMultiplier(solution.combos['6']);
    var comboX = baseComboMultiplier(solution.combos);
    var multiplier = (baseX * comboX);
    if(multiplier == 0) return '-';
    if($scope.team.hl) {
      return Math.floor($scope.team.hl * multiplier);
    } else {
      return +(baseX * comboX).toFixed(1) + "x";
    }

    return baseX * comboX;
  };

  $scope.indexToGlyphicon = function(index) {
    switch (index) {
      case "1": return "glyphicon-fire";
      case "2": return "glyphicon-tint";
      case "3": return "glyphicon-leaf";
      case "4": return "glyphicon-asterisk";
      case "5": return "glyphicon-adjust";
      case "6": return "glyphicon-heart";
    }
  };

  $scope.indexToAbbr = function(index) {
    switch(index + "") {
      case '1': return 'fr';
      case '2': return 'wt';
      case '3': return 'wd';
      case '4': return 'lt';
      case '5': return 'dk';
      case '6': return 'hl';
    }
  };

});