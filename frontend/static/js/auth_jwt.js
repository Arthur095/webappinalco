$(document).ready(function(){

    $("div[name=connect] > button").click(function( event ) {
        event.preventDefault();
        $("div[id=get_connect]").hide();
        var body = {};
        body["username"] = $("input[name=username]").val();
        body["password"] = $("input[name=password]").val();
        
        if(body["username"] == "" || body["password"] == ""){
            $("div[id=get_connect]").html("<p>Veuillez renseigner identifiant et mot de passe.</p>");
            $("div[id=get_connect]").css("color", "red");
            $("div[id=get_connect]").show();
            return;
        }

        var settings = {
            "url": "/auth",
            "method": "POST",
            "timeout": 0,
            "headers": {
              "Content-Type": "application/json"
            },
            "data": JSON.stringify(body),
          };
          
          $.ajax(settings).done(function (response) {
            console.log(response);

           
            var token = response["access_token"];
            sessionStorage.setItem('jwt', token);
            window.location.replace("/search_data");


          }).fail(function(jqXHR) {
            $("div[id=get_connect]").html("<p>Echec de la connexion : mauvais identifiants</p>");
            $("div[id=get_connect]").css("color", "red");
            $("div[id=get_connect]").show();
          });


    });

});

function logout(event) {
  
    sessionStorage.clear();
    window.location.replace("/");
  
  };