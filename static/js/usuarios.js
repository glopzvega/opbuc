function bloquear_usuario (id){
    $.getJSON(`/usuarios/bloquear/${id}/`, function(res){
        if (res.success)
        {
            alert("El registro ha sido actualizado");
            location.reload();
        }
        else
        {
            alert("Ocurrio un problema al actualizar el registro")
        }
    })
}

function update_usuario (id){
    $.getJSON(`/usuarios/update/${id}/`, function(res){
        if (res.success)
        {
            alert("El registro ha sido actualizado");
            location.reload();
        }
        else
        {
            alert("Ocurrio un problema al actualizar el registro")
        }
    })
}

function suggest_usuario (id){
    $.getJSON(`/usuarios/suggest/${id}/`, function(res){
        if (res.success)
        {
            alert("El registro ha sido actualizado");
            location.reload();
        }
        else
        {
            alert("Ocurrio un problema al actualizar el registro")
        }
    })
}

function send_mail(data)
{
    $.post("/usuarios/email/", data, function(res){
        console.log(res)
        alert("Se han enviado los mensajes");
        $(".modal-email-usuarios").modal("hide");
    }, "json")
}

$("#form-email-usuarios").on("submit", function(e){
    e.preventDefault();
    let data = $(this).serialize();
    console.log(data)
    send_mail(data);
});

$("a.send-mail").on("click", function(e){
    e.preventDefault();
    var selected = []
    $(".table-usuarios .select").each(function(index, value){        
        if ($(value).is(":checked"))
        {            
            selected.push($(value).attr("user_id"));
        }
    });
    if(selected)
    {
        $("#form-email-usuarios").find("[name='usuarios']").val(selected);
    }
    $(".modal-email-usuarios").modal("show");
})

$(".checkall").on("click", function(){
    var all_selected = true
    $(".table-usuarios .select").each(function(index, value){        
        if (!$(value).is(":checked"))
        {
            all_selected = false;
            return false;
        }
    });
    if (all_selected)
    {
        $(".checkall").prop("checked", false);
        $(".table-usuarios .select").prop("checked", false);
        $("a.send-mail").hide();
    }
    else
    {
        $(".checkall").prop("checked", true);
        $(".table-usuarios .select").prop("checked", true);
        $("a.send-mail").show();
    }

});

$(".table-usuarios .select").on("click", function(){
    var selected = false;
    $(".table-usuarios .select").each(function(index, value){        
        if ($(value).is(":checked"))
        {
            selected = true;
            return false;
        }
    });
    if(selected)
    {
        $("a.send-mail").show();
    }
    else{
        $("a.send-mail").hide();
    }

})

$("a.update").on("click", function(e){
    e.preventDefault();
    let id = $(this).attr("data-id");
    update_usuario(id);
})

$("a.suggest").on("click", function(e){
    e.preventDefault();
    let id = $(this).attr("data-id");
    suggest_usuario(id);
})

$("a.btn-bloquear").on("click", function(e){
    e.preventDefault();
    let id = $(this).attr("data-id");
    bloquear_usuario(id);
})