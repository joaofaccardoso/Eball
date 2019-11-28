if(document.readyState === "complete" || (document.readyState!== "loading" && !document.documentElement.doScroll)){
    main();
}else{
    document.addEventListener("DOMContentLoaded", main);
}

function main() {
    var inputTeam = document.getElementById('id_name');
    var inputTournament = document.getElementById('seltournament');
    inputTeam.addEventListener('change', function(e) {
        sendAjax(e,inputTeam ,inputTournament);
    } );
}

function sendAjax(e,inputTeam ,inputTournament) {
    const csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value
    var teamName = inputTeam.value;
    var tournamentName = inputTournament.value;

    $.ajaxSetup({
        headers:{
            "X-CSRFToken": csrf_token,
        }
    });

    $.ajax({
        url: 'checkTeamName/',
        data: JSON.stringify({'teamName':teamName, 'tournamentName':tournamentName}),
        type: 'PATCH',
        contentType: "application/json",
        success: (response) => {
            if (response.is_taken) {
                $('#id_name').val('');
                $('#messageDivParent').html(
                    "<div class='alert alert-warning'>Team name already taken on this tournament! Try another one.</div>"
                );
            }
        },
        failure: (response) => {
            console.log("FAILURE -> ", response);
        }
    });
}