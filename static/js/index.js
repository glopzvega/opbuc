let actualizar_parametros = function(zone_id, category_id)
{
  // debugger
  location.href = "?zone="+zone_id+"&category="+category_id;
}

$(".buscar-btn").on("click", function(){
  $("#lugares_encontrados").html("").hide();
    buscarlugares();
});

$("#busqueda").on("keyup", function(){
  $(".linear-progress-material").addClass("active")
  clearTimeout(tiempounidad);
    
  if($(this).val() == "")
  {
    $(".linear-progress-material").removeClass("active");
    $("#categorias").show();
  }

  if($(this).val().length >= 2)
  { 
    
      $("#lugares_encontrados").html("").hide();
      tiempounidad = setTimeout(buscarlugares, 900);
  }
  else
  {   
    this.activeLoader = ""        
      $("#lugares_encontrados").html("").hide();          
  }
});

// $("input").not("[type=checkbox]").addClass("form-control")
// $("select,textarea").addClass("form-control")
// $('[data-toggle="tooltip"]').tooltip();    

// $('.datetimepicker1').datetimepicker({
//   icons: {
//           time: "far fa-clock",
//           date: "far fa-calendar",
//           up: "fas fa-angle-up",
//           down: "fas fa-angle-down"
//       }
// });

let buscarlugares = function()
{
  let busqueda = $("#busqueda").val()
  console.log(busqueda)
  $.getJSON("/buscarlugar/", {"busqueda" : busqueda, "zone" : zone_id, "category" : category_id}, function(res){
    $(".linear-progress-material").removeClass("active")

    if (res.data != undefined && res.data.length > 0){

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
        $("#lugares_encontrados").append(card)
        $("#lugares_encontrados").show()
      })

      $("#categorias").hide();
    }
  });
}
  // $('body').scrollspy({ target: '.navbar' , offset : 300})      

$("a.categoria").on("click", function(e){  
  e.preventDefault();   
  category_id = $(this).attr("category_id");  
  actualizar_parametros(zone_id, category_id);  
});

$("a.zona").on("click", function(e){  
  e.preventDefault();   
  zone_id = $(this).attr("zone_id");  
  actualizar_parametros(zone_id, category_id);     
});

buscarlugares();