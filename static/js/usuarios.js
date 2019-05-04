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