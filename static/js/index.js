let urlparams = getUrlVars();
let zone_id = "";
let category_id = "";
let tiempounidad = 0;

if(urlparams["zone"] != "" && urlparams["zone"] != undefined)
{
  zone_id = urlparams["zone"];
}
if(urlparams["category"] != "" && urlparams["category"] != undefined)
{
  category_id = urlparams["category"];
}
// let actualizar_parametros = function(zone_id, category_id)
// {
//   // debugger
//   location.href = "?zone="+zone_id+"&category="+category_id;
// }

$(".buscar-btn").on("click", function(){
  $("#lugares_encontrados").html("").hide();
    buscarlugares(zone_id, category_id);
});

$("#busqueda").on("keyup", function(){
  $(".linear-progress-material").addClass("active")
  clearTimeout(tiempounidad);
    
  if($(this).val() == "")
  {
    $(".linear-progress-material").removeClass("active");
    $("#categorias").show();
  }

  $("#lugares_encontrados").html("").hide();
  tiempounidad = setTimeout(buscarlugares, 900);
  
});


let buscarlugares = function(zone_id, category_id)
{
  let busqueda = $("#busqueda").val()
  let zone_res = {};
  let category_res = {};
  console.log(busqueda)
  $.getJSON("/buscarlugar/", {"busqueda" : busqueda, "zone" : zone_id, "category" : category_id}, function(res){
    $("#lugares_encontrados").html("");
    $(".linear-progress-material").removeClass("active")
    // if (zone_id != "")
    //   $("a.zona[zone_id="+zone_id+"]").addClass("selected");
    // if(category_id != "")
    //   $("a.categoria[category_id="+category_id+"]").addClass("selected");
    zone_res = res.zone_id;
    if (zone_res)
    {
      console.log(zone_res)
      $("a.zona").each(function(index, value){
        if($(this).attr("zone_id") == zone_res.id)
        {
          $(this).addClass("selected");
          $("#dropdownMenuButtonZona").text(zone_res.name.substr(0, 10));
        }
      });
    }
    else
    {
      $("a.zona").each(function(index, value){
        if($(this).attr("zone_id") == "")
        {
          $(this).addClass("selected");
          $("#dropdownMenuButtonZona").text("Todas");
        }
      });
    }

    category_res = res.category_id;
    if (category_res)
    {
      console.log(category_res)
      $("a.categoria").each(function(index, value){
        if($(this).attr("category_id") == category_res.id)
        {
          $(this).addClass("selected");
          $("#dropdownMenuButtonCategoria").text(category_res.name.substr(0, 10));
        }
      });
    }
    else
    {
      $("a.categoria").each(function(index, value){
        if($(this).attr("category_id") == "")
        {
          $(this).addClass("selected");
          $("#dropdownMenuButtonCategoria").text("Todas");
        }
      });
    }

    if (res.data != undefined && res.data.length > 0)
    {      
      var cards = "";
      $.each(res.data, function(index, lugar){        
        let photo = lugar.photo;
        if (photo == "")
          photo = "/static/img/default.png"
        console.log(photo)
        let card = [
          '<div class="col-12 col-lg-4">',
          '<div class="caja">',
            '<a href="/lugar/'+lugar.id+'">',
              '<img src="' + photo + '"/>',
            '</a>',
            '<div class="detail">',
              '<div class="item-name">',
                '<b><a href="/lugar/'+lugar.id+'" class="text-danger">' + lugar.name + '</a></b>',
              '</div>',
              '<div class="item-zone">',
                '<p>',
                  '<small class="text-muted">' + lugar.zone_id[1] + '</small>',
                  '<br>',
                  '<small>',
                    '<i class="fa fa-phone-square"></i> ',
                     lugar.phone,
                  '</small>',
                '</p>',
              '</div>',
            '</div>',
          '</div><br>',
        '</div>'].join("")
        cards += card;
      })
      $("#lugares_encontrados").append(cards)
      $("#lugares_encontrados").show()

      $("#categorias").hide();
    }
  });
}
  // $('body').scrollspy({ target: '.navbar' , offset : 300})      

$("a.categoria").on("click", function(e){  
  e.preventDefault();   
  $("a.categoria").removeClass("selected");
  $(this).addClass("selected");
  $("a.zona").removeClass("selected");
  $("a.nav-link.inicio").addClass("selected");
  category_id = $(this).attr("category_id");  
  buscarlugares("", category_id);  
});
// 
$("a.zona").on("click", function(e){  
  e.preventDefault();   
  $(".navbar-nav > .nav-item > .nav-link").removeClass("selected");
  // $("a.zona").removeClass("selected");
  $(this).addClass("selected");
  zone_id = $(this).attr("zone_id");  
  buscarlugares(zone_id, category_id);     
});

buscarlugares(zone_id, category_id);