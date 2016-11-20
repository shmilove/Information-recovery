/// reference path ="angular.min.js"/>
//$(document).ready(function(){
////    searchEngine = angular.module("searchEngine", []);
//    $('.search-results li a').click(function( event){
//        showSummary(event.target.id);
//    });
//});
////
////var searchEngine;
//function showSummary(summary_id)
//{
//        clearBody();
//        $(".gif-container").css("visibility", "visible");
//        $.ajax({
//		url:'/getSummary',
//		type:'GET',
//		dataType:'text',
//		data:{summary_id: summary_id},
//		success:function(data, status, xhr) {
//		    $(".gif-container").css("visibility", "hidden");
//			if(status == "success")
//			{
//
//			    movie_data = JSON.parse(data);
//
//
////                searchEngine.controller("movieController", function($scope){
////	                $scope.movie_name = movie_data.movie_name;
////	                $scope.movie_summary = movie_data.movie_summary;
////                });
//			    $(".search-results").empty()
//			    $(".body").append('<div id="movie_summary_div">' +
//			    '<h2>'+ movie_data.movie_name + '</h2>' + '<p>' + movie_data.movie_summary + '</p>' +
//			    '</div><div id="return"><a onclick="showList()" >חזור לרשימה</a></div>');
//
//			}
//
//
//		},
//		error:function(xhr, status, error) {
//				alert(status);
//				console.error(xhr, status, error);
//		}
//	});
//
//}
//
//function encode_utf8(s) {
//  return unescape(encodeURIComponent(s));
//}
//
//function decode_utf8(s) {
//  return decodeURIComponent(escape(s));
//}
//
//function clearBody()
//{
//    $(".search-results").empty();
//    if(document.getElementById("movie_summary_div") !== null)
//    {
//        $("#movie_summary_div").empty();
//    }
//    if(document.getElementById("return") !== null)
//    {
//        $("#return").empty();
//    }
//
//}
//function movieController($scope){
//
//     $scope.movie_name = movie_data.movie_name;
//	 $scope.movie_summary = movie_data.movie_summary;
//
//
//}