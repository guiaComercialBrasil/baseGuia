// Boosting
$(".boost").click(function(){
    var url = $(this).attr("data-boost-url");
    var slug = $(this).attr("data-estab");
    $.ajax({
        type: "GET",
        url: url,
        data: {
            "estabelecimento" : slug
        },
        success: function(response) {
            console.log(response);
            console.log("yes")

        },
        error: function (message) {
            console.log(message.statusText);
        },
        complete: function(){
            location.reload();
        }
    });
});

// Rating
$(".rating :input").click(function(){
    var url = $(this).parent().attr("data-rating-url");
    var slug = $(this).parent().attr("data-estab");
    var rate = $(this).val();

    $.ajax({
        type: "GET",
        url: url,
        data: {
            "estabelecimento" : slug,
            "nota" : rate
        },
        success: function(response){
            let data = JSON.parse(response)
            let successHTML = `
                <p><b>Avalie o estabelecimento</b></p>
                <legend>Nota:</legend>
                <fieldset 
                    class="starability-result" 
                    data-rating="${data.nota}"
                >
                    Nota: ${data.nota} Estrelas
                </fieldset>
                <p>Avaliação média: ${data.media} - ${data.count} avaliações</p>
            `
            $("#avalie_2").html(successHTML);
        },
        error: function(message){
            console.log(message.statusText);
        }
    });

});