
$(document).ready(function(){

    //Search form
    $("div[id=get_result]").hide();
    //Put form
    $("div[id=put_result").hide();
  
    //Search form action button (GET)
    $("div[name=get] > button").click(function( event ) {
      event.preventDefault();
  
      var id = $("input[name='id']").val();
      var search = $("input[name='search']").val();
      var field = $("select[name='field']").val();
  
      //Get all users
      if(field == "all"){
        var url = "/users/all";
      }
      //Search by id on all only 
      else if(id != "" && search == "" && field == "one"){
        var url = "/users/" + id;
      }
  
      //Search by id and field
      else if(id != "" && search == "" && field !="one"){
        var url = "/users/" + id + "/" + field;
      }
  
      //Search by text and field
      else if(id == "" && search != "" && field != "one"){
        var url = "/users/" + field + "/" + search;
      }
  
      //If no id and no text in form
      else if(id != "" && search != ""){
        $("div[id=get_result]").html("<p>Vous ne pouvez pas spécifier un id et une recherche en même temps.</p>");
        $("div[id=get_result]").css("color", "red");
        $("div[id=get_result]").show();
        return;
      }
  
      //If both id and text in form
      else if(id == "" && search == ""){
        $("div[id=get_result]").html("<p>Veuillez remplir un des deux champs du formulaire.</p>");
        $("div[id=get_result]").css("color", "red");
        $("div[id=get_result]").show();
        return;
      }
  
      //If text only in form but field set on all
      else if(id == "" && search !="" && field == "one"){
        $("div[id=get_result]").html("<p>Veuillez sélectionner un champ valide sur lequel effectuer votre recherche.</p>");
        $("div[id=get_result]").css("color", "red");
        $("div[id=get_result]").show();
        return;
      }
  
      //GET Request
      var settings = {
        "url": url,
        "method": "GET",
        "timeout": 0,
      };
    
      
      $.ajax(settings).done(function (response) {
        console.log(response);
        
  
        //Start rendered table as string
        var result = "<table><thead><th>";
   
        //If request maches only one object
        if(response instanceof Array){
          for(var k in response[0]){
            result += "<td>" + k + "</td>";
          }
          result += "</th></thead>";
          response.forEach(function (dic, index) {
            console.log(dic, index);
            result += "<tr>";
            for(var key in dic){
                if(dic[key] == ""){
                  result += "<td>" + "null" + "</td>";
                }
                else{
                  result += "<td>" + dic[key] + "</td>";
                }
              }
            result += "</tr>";
          });
        }
        else{
          var body = "<tr>";
          for(var k in response){
            result += "<td>" + k + "</td>";
            if(response[k] == ""){
              body += "<td>" + "null" + "</td>";
            }
            else{
              body += "<td>" + response[k] + "</td>";
            }
          }
          result += "</th></thead>";
          body += "</tr>";
          result += body;
        }
  
        //Fulfils the div
        $("div[id=get_result]").html(result);
        //Colors in black in case of having red message before
        $("div[id=get_result]").css("color", "black");
        //Shows the div
        $("div[id=get_result]").show();
  
      }).fail(function(jqXHR) {
        if(jqXHR.status==400){
          $("div[id=get_result]").html("<p>Aucun élément ne correspond à votre recherche.</p>");
        }
        else if(jqXHR.status==404){
          $("div[id=get_result]").html("<p>L'identifiant n'existe pas dans la base de données.</p>");
        }
        $("div[id=get_result]").css("color", "red");
        $("div[id=get_result]").show();
      });
  
    });//End Search form action button
    
    
     //Search form action button (GET)
    $("div[name=put] > button").click(function( event ) {
        event.preventDefault();
        
        var body = {}
        //Retrieving form to make the put body
        body["nom"] =  $("input[name='nom']").val();
        body["prenom"] =  $("input[name='prenom']").val();
        body["fonction"] =  $("input[name='fonction']").val();
        body["anciennete"] =  $("input[name='anciennete']").val();
        body["conge"] =  $("input[name='conge']").val();
        body["actif"] =  $("input[name='actif']").val();
        body["actionnaire"] =  $("input[name='actionnaire']").val();
        body["missions"] =  $("input[name='missions']").val();
        
        //If one field is empty : error message.
        for(k in body){
            if(body[k] == ""){
                $("div[id=put_result]").html("<p>Veuillez remplir tous les champs du formulaire.</p>");
                $("div[id=put_result]").css("color", "red");
                $("div[id=put_result]").show();
                return;
            }
        }





    });//End Search form action button

  }) ;