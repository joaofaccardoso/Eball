if(document.readyState === "complete" || (document.readyState!== "loading" && !document.documentElement.doScroll)){
    main();
}else{
    document.addEventListener("DOMContentLoaded", main);
}

function main() {
    var inputTournament = document.getElementById('id_name');
    var inputStartDate = document.getElementById('begin');
    inputTournament.addEventListener('change', function(e) {
        tournamentAjax(e, inputTournament);
    })
    inputStartDate.addEventListener('change', function(e) {
        dateAjax(e, inputStartDate);
    })
}

function tournamentAjax(e, inputTournament) {
    const csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    var tournamentName = inputTournament.value;

    $.ajaxSetup({
        headers:{
            "X-CSRFToken": csrf_token,
        }
    });

    $.ajax({
        url: 'checkTournamentName/',
        data: JSON.stringify({'name':tournamentName}),
        type:'PATCH',
        contentType: 'application/json',
        success: (response) => {
            if (response.is_taken) {
                $('#id_name').val('');
                $('#messageDivParent').html(
                    "<div class='alert alert-warning'>Tournament name already taken! Try another one.</div>"
                );
            }
        },
        failure: response => {
            console.log('FAILURE -> ', response);
        }
    })
}

function dateAjax(e, inputStartDate) {
    const csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    var startDate = inputStartDate.value;
    console.log(startDate);

    $.ajaxSetup({
        headers:{
            "X-CSRFToken": csrf_token,
        }
    });

    $.ajax({
        url: 'checkDates/',
        data: JSON.stringify({'startDate':startDate}),
        type: 'PATCH',
        contentType: 'application/json',
        success: (response) => {
            console.log(response);
            if (response.is_valid==false) {
                $('#begin').val('');
                $('#messageDivParent').html(
                    "<div class='alert alert-warning'>The start date off the tournament must be after today!</div>"
                );
            }
            else {
                $('#messageDivParent').html("");
            }
        },
        failure: (response) => {
            console.log("FAILURE -> ", response);
        }
    })
}