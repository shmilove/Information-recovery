// Script that show the results of the movie search
$(document).ready(function(){

    // Regular search
    $('#searchBTN').click(function( event){
        event.preventDefault();
        searchResult();

    });
    // Stemming search
    $('#searchBTN2').click(function( event){
        event.preventDefault();
        searchResultWithStemming();
    });
});
list = [];

// Ajax call for the regular search
function searchResult()
{
    $(".gif-container").css("visibility", "visible");
    $(".search-results").empty();
    query = $("#query").val();
    $.ajax({
		url:'/searchResult',
		type:'GET',

		data:{query: query},
		success:function(data, status, xhr) {
			data = JSON.parse(data);
			list = data;
			$(".gif-container").css("visibility", "hidden");
			if(list.length > 0)
			    showList();
			else
			    showNotFoundMessage(query);
		},
		error:function(xhr, status, error) {
				$(".gif-container").css("visibility", "hidden");
				console.error(xhr, status, error);
		}
	});
    $("#show_summary").attr("src", '../static/js/showSummary.js');
}

// Ajax call for the stemming search
function searchResultWithStemming()
{
    $(".gif-container").css("visibility", "visible");
    $(".search-results").empty();
    query = $("#query").val();
    $.ajax({
		url:'/searchResultWithStemming',
		type:'GET',

		data:{query: query},
		success:function(data, status, xhr) {
			data = JSON.parse(data);
			list = data;
			$(".gif-container").css("visibility", "hidden");
			if(list.length > 0)
			    showList();
			else
			    showNotFoundMessage(query);

		},
		error:function(xhr, status, error) {
				$(".gif-container").css("visibility", "hidden");
				console.error(xhr, status, error);
		}
	});
    $("#show_summary").attr("src", '../static/js/showSummary.js');
}

// Display of the movie result list
function showList()
{
    clearScreen();
    $(".search-results").empty();
    if (list.length > 0)
	{
        for(var i = 0; i < list.length; ++i)
        {
            $(".search-results").append('<li><a id ="' + list[i][0] + '" onclick="showSummary('+list[i][0]+')">'
             + list[i][1] + '</a> <a href="'+ list[i][2]+'" target="_blank">קישור לסרט</a></li>');
        }
    }
}

function clearScreen()
{
    $(".search-results li").empty();
    if(document.getElementById("movie_summary_div") !== null)
    {
        $("#movie_summary_div").remove();

    }
    if(document.getElementById("return") !== null)
    {
        $("#return").remove();
    }
    if(document.getElementById("not_found_message") !== null)
    {
        $("#not_found_message").remove();
    }
    if(document.getElementById("return") !== null)
    {
        $("#return").empty();
    }
    if(document.getElementById("query_msg") !== null)
    {
        $("#query_msg").empty();
    }

}

function showNotFoundMessage(query)
{
    clearScreen();
    $(".body").append('<div id="not_found_message">לא נמצאו תוצאות עבור <span id="query_msg">'+query+'</span></div>')
    $("#query_msg").css("color","blue");

}