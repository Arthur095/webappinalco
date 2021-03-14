
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

    //Search by id on all only 
    if(id != "" && search == "" && field == "all"){
      var url = "/data/" + id;
    }

    //Search by id and field
    else if(id != "" && search == "" && field !="all"){
      var url = "/data/" + id + "/" + field;
    }

    //Search by text and field
    else if(id == "" && search != "" && field != "all"){
      var url = "/data/" + field + "/" + search;
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
    else if(id == "" && search !="" && field == "all"){
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
      var result = "<table class='table table-striped'><thead class='thead-dark'>";
 
      //If request maches only one object
      if(response instanceof Array){
        for(var k in response[0]){
          result += "<th scope='col'>" + k + "</th>";
        }
        result += "<th name='edit'>Editer</th><th name='delete'>Supprimer</th></thead><tbody>";
        response.forEach(function (dic, index) {
          console.log(dic, index);
          result += "<tr class='font-weight-bold'>";
          for(var key in dic){
              if(dic[key] == ""){
                result += "<td>" + "null" + "</td>";
              }
              else{
                result += "<td>" + dic[key] + "</td>";
              }
            }
          result += "<td><div id='post' name='put_" + dic["id"] +  "' class='form-group'><button onclick='editData(event)' class='btn btn-secondary px-4 align-self-stretch d-block' type='submit'><span>Editer</span></button></div></td>";
          result += "<td><div id='delete' name='del_" + dic["id"] + "' class='form-group'><button onclick='deleteData(event)' class='btn btn-secondary px-4 align-self-stretch d-block'><span>Supprimer</span></button></div></td>";
          result += "</tr>";
        });
        result += "</tbody></table>";
      }

      else{
        var body = "<tr class='font-weight-bold'>";
        for(var k in response){
          result += "<th scope='col'>" + k + "</th>";
          if(response[k] == ""){
            body += "<td>" + "null" + "</td>";
          }
          else{
            body += "<td>" + response[k] + "</td>";
          }
        }
        result += "<th name='edit'>Editer</th><th name='delete'>Supprimer</th></thead>";
        if(Object.keys(response).length != 1){
          body += "<td><div id='post' name='put_" + response["id"] +  "' class='form-group'><button onclick='editData(event)' class='btn btn-secondary px-4 align-self-stretch d-block' type='submit'><span>Editer</span></button></div></td>";
          body += "<td><div id='delete' name='del_" + response["id"] + "' class='form-group'><button onclick='deleteData(event)' class='btn btn-secondary px-4 align-self-stretch d-block'><span>Supprimer</span></button></div></td>";
        }
        else{
          body += "<td>Indisponible</td><td>Indisponible</td>"
        }
        body += "</tr>";
        result += body;
        result += "</tbody></table>";
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
  
  
   //Put form action button (PUT)
  $( "div[name=put] > button" ).click(function( event ) {
      event.preventDefault();
      
      var body = {}
      //Retrieving form to make the put body
      body["nom"] =  $("input[name='nom']").val();
      body["prenom"] =  $("input[name='prenom']").val();
      body["fonction"] =  $("input[name='fonction']").val();
      body["anciennete"] =  parseInt($("input[name='anciennete']").val());
      body["conge"] =  parseInt($("input[name='conge']").val());
      body["actif"] =  ($("select[name='actif']").val() == 'true');
      body["actionnaire"] = ($("select[name='actionnaire']").val() == 'true');
      body["missions"] = $("input[name='missions']").val().split(",");
      
      //If one field is empty : error message.
      for(k in body){
          if(body[k] === "" || body[k] === [] || body[k] == [""]){
              $("div[id=put_result]").html("<p>Veuillez remplir tous les champs du formulaire.</p>");
              $("div[id=put_result]").css("color", "red");
              $("div[id=put_result]").show();
              return;
          }
      }

      var settings = {
          "url": "/data",
          "method": "PUT",
          "timeout": 0,
          "headers": {
              "Content-Type": "application/json"
            },
          "data": JSON.stringify(body)
        };
        
        $.ajax(settings).done(function (response) {
          console.log(response);
          $("div[id=put_result]").html("<p>L'utilisateur a été ajouté à la base de données.</p>");
          $("div[id=put_result]").css("color", "green");
          $("div[id=put_result]").show();
        }).fail(function(jqXHR) {
          $("div[id=put_result]").html("<p>Une erreur est survenue lors de l'ajout.</p>");
          $("div[id=put_result]").css("color", "red");
          $("div[id=put_result]").show();
        });


  });//End Put form action button


});//End jquery doc parsing

//DELETE button action
function deleteData(event) {
  event.preventDefault();
  var target = event.target || event.srcElement;
  //event.preventDefault();
  //$("div[name=del1] > button").hide();

  var name = event.currentTarget.parentNode.getAttribute('name');
  id = name.split("_")[1];
 
  var settings = {
  "url": "/data/" + id,
  "method": "DELETE",
  "timeout": 0
  };

  $.ajax(settings).done(function (response) {
  console.log(response);
      $("div[id=get_result]").html("<p>L'utilisateur " + id + " a été supprimé de la base de données.</p>");
      $("div[id=get_result]").css("color", "green");
      $("div[id=get_result]").show();
  }).fail(function(jqXHR) {
      $("div[id=get_result]").html("<p>Une erreur est survenue lors de la supression.</p>");
      $("div[id=get_result]").css("color", "red");
      $("div[id=get_result]").show();
    });

};//End delete button action


//POST button action
function editData(event) {
  event.preventDefault();
  var target = event.target || event.srcElement;
  //event.preventDefault();
  //$("div[name=del1] > button").hide();

  var name = event.currentTarget.parentNode.getAttribute('name');
  id = name.split("_")[1];

  var tr = $("div[name=put_" + id + "]").parent().parent().children();




  var placeholder = ["id", "nom", "prenom", "fonction", "anciennete", "conge", "actif", "actionnaire", "missions"];
  var count = 0;
  var result = "<div><p><hr class='my-4'><p><h4 class='title-job text-center mb-4'>Edition de l'utilisateur " + id + "</h4></div><form class='booking-form'><div class='row'>";
  $.each($(tr), function(){
      if(count == 6 || count == 7){
          result += "<div class='col-md mb-md-0 mb-1'><div class='form-group'><div class='form-field'><div class='select-wrap'><select name='" + placeholder[count] + "2' id='post' class='form-control'><option value='vide'>Inchangé</option><option value='true'>Oui</option><option value='false'>Non</option></select></div></div></div></div>";
      }
      else if (count == 4 || count == 5) {
          result += "<div class='col-md mb-md-0 mb-1'><div class='form-group'><div class='form-field'><input type='number' name='" + placeholder[count] + "2' class='form-control' placeholder='" + $(this).text() + "'></div></div></div>";
      }
      else if (count == 1 || count == 2 || count == 3 || count == 8 ){
          result += "<div class='col-md mb-md-0 mb-1'><div class='form-group'><div class='form-field'><input type='text' name='" + placeholder[count] + "2' class='form-control' placeholder='" + $(this).text() + "'></div></div></div>";
      }
      if (count == 4){
        result += "</div><div class='row'>";
      }
      count += 1;
  });

  result += "<div class='col-md-12'><div class='row'><div class='col-md d-flex align-items-end mb-md-0 mb-1'><div id='valider' name='post' class='form-group'><button onclick='validData(event," + id + ")' class='btn btn-secondary px-4 align-self-stretch d-block' type='submit'><span>Valider</span></button></div></div><div class='col-md mb-md-0 mb-1'></div><div class='col-md mb-md-0 mb-1'></div><div class='col-md mb-md-0 mb-1'></div></div></div></div>";
  result += "</div></form>";
  $( "div[id=get_result]").html(result);
};//end POST button action

//Validate POST button action
function validData(event, id) {
event.preventDefault();
var body = {}
//Retrieving form to make the put body
body["nom"] =  $("input[name='nom2']").val();
body["prenom"] =  $("input[name='prenom2']").val();
body["fonction"] =  $("input[name='fonction2']").val();
body["anciennete"] =  parseInt($("input[name='anciennete2']").val());
body["conge"] =  parseInt($("input[name='conge2']").val());

if($("select[name='actif2']").val() == 'true' || $("select[name='actif2']").val() == 'false'){
  body["actif"] =  ($("select[name='actif2']").val() == 'true');
}
if($("select[name='actionnaire2']").val() == 'true' || $("select[name='actionnaire2']").val() == 'false'){
  body["actionnaire"] = ($("select[name='actionnaire2']").val() == 'true');
}

body["missions"] = $("input[name='missions2']").val().split(",");

for(k in body){
  if(body[k] === "" || body[k][0] === '' || body[k] == "vide" || Number.isNaN(body[k])){
    delete body[k];
  }
}

if(Object.keys(body).length == 0){
  $("div[id=get_result]").html("<p>Aucun champ n'a été modifié, l'utilisateur reste inchangé.</p>");
  $("div[id=get_result]").css("color", "red");
  $("div[id=put_result]").show();
  return;
}

var settings = {
  "url": "/data/" + id,
  "method": "POST",
  "timeout": 0,
  "headers": {
    "Content-Type": "application/json"
  },
  "data": JSON.stringify(body),
};

$.ajax(settings).done(function (response) {
  console.log(response);
  $("div[id=get_result]").html("<p>L'utilisateur " + id + " a bien été modifié.</p>");
  $("div[id=get_result]").css("color", "green");
  $("div[id=put_result]").show();
}).fail(function(jqXHR) {
  $("div[id=get_result]").html("<p>Une erreur est survenue lors de l'édition.</p>");
  $("div[id=get_result]").css("color", "red");
  $("div[id=get_result]").show();
});

};//end validate post