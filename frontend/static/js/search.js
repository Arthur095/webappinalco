
$(document).ready(function(){

  $("div[id=result]").hide();

  $("div[id=valider] > button").click(function( event ) {
    event.preventDefault();

    var id = $("input[name='id']").val();

    var settings = {
      "url": "/users/1",
      "method": "GET",
      "timeout": 0,
    };
    
    $.ajax(settings).done(function (response) {
      console.log(response);

    alert(response);
    });
   

    // on remplie la div par la string formée précédemment
    //$("div[id=result]").html(result);

    // on affiche la division
    //$("div[id=result]").show();
    

  });
  
}) ;