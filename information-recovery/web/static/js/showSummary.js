// Script that show the summary of the chosen movie.
$(document).ready(function(){
    $('.search-results li a').click(function( event){
        showSummary(event.target.id);
    });
});

// Display the summary according the id of the movie
function showSummary(summary_id)
{
        clearBody();
        $(".gif-container").css("visibility", "visible");
        $.ajax({
		url:'/getSummary',
		type:'GET',
		dataType:'text',
		data:{summary_id: summary_id},
		success:function(data, status, xhr) {
		    $(".gif-container").css("visibility", "hidden");
			if(status == "success")
			{

			    movie_data = JSON.parse(data);

			    $(".search-results").empty()
			    $(".body").append('<div id="movie_summary_div">' +
			    '<h2>'+ movie_data.movie_name + '</h2>' + '<p>' + movie_data.movie_summary + '</p>' +
			    '</div><div id="return"><a onclick="showList()" >חזור לרשימה</a></div>');

			}


		},
		error:function(xhr, status, error) {
				$(".gif-container").css("visibility", "hidden");
				console.error(xhr, status, error);
		}
	});

}

function encode_utf8(s) {
  return unescape(encodeURIComponent(s));
}

function decode_utf8(s) {
  return decodeURIComponent(escape(s));
}

function clearBody()
{
    $(".search-results").empty();
    if(document.getElementById("movie_summary_div") !== null)
    {
        $("#movie_summary_div").empty();
    }
    if(document.getElementById("return") !== null)
    {
        $("#return").empty();
    }

}
function movieController($scope){

     $scope.movie_name = movie_data.movie_name;
	 $scope.movie_summary = movie_data.movie_summary;


}