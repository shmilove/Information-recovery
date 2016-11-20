/// <reference path="anguler.min.js" />
var searchEngine = angular.module("searchEngine", []);

searchEngine.controller("movieController", function($scope, $http) {
//	var list = [
//	{	name: "מלך האריות", summary: " עלילות סימבה ומופסה"	},
//	{	name: "עידן הקרח", summary: " ממוטה נמר ומשהו לא ברור בהרפתקות"	},
//	{	name: "מלך האריות 2", summary: " עלילות בתו של סימבה קיארה וקובו"	}
//	];
//
//	$scope.searchQuery = function(){
//		query = $("#query").val();
//		$scope.results = list;
//		showResultUl($scope);
//
//	};
	$scope.searchQuery = function(){
        movieList = [];
        $(".gif-container").css("visibility", "visible");
        query = $("#query").val();
//        $http.get('/searchResult', {query: query}).
//            success(function(data, status){
//                $(".gif-container").css("visibility", "hidden");
//                alert(data);
//            }).
//            error(function(data, status){
//             $(".gif-container").css("visibility", "hidden");
//             alert(data);
//            //whatever you need to do if the data is not available
//      });
        $.ajax({
            url:'/searchResult',
            type:'GET',

            data:{query: query},
            success:function(data, status, xhr) {
                data = JSON.parse(data);
                list = data;
                $(".gif-container").css("visibility", "hidden");
                if(list.length > 0)
                {

                    for(var i = 0; i < list.length; ++i)
                    {
                        var temp = {id: list[i][0], name: list[i][1]};
                        movieList.push(temp);
                    }
                    $scope.results = movieList;
                    alert(movieList);

                }
            },
            error:function(xhr, status, error) {
                    alert(status);
                    console.error(xhr, status, error);
            }
	    });
	};
	$scope.showSummary = function(result){
		$scope.movie_name = result.name;
		$scope.summary = result.summary;
		showSummaryDiv($scope);
	};
	$scope.returnToResult = function(){
		$scope.results = list;
		showResultUl($scope);
	};
	$scope.hideList = true;
	$scope.hideSummary = true;
	$scope.backTolistDiv = false;
});

function showSummaryDiv($scope)
{
	$scope.hideList = true;
	$scope.hideSummary = false;
	$scope.summaryDiv = true;
	$scope.backTolistDiv = true;
}
function showResultUl($scope)
{
	$scope.hideList = false;
	$scope.summaryDiv = false;
	$scope.backTolistDiv = false;
}

