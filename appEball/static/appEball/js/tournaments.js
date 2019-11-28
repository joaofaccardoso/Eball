if(document.readyState === "complete" || (document.readyState!== "loading" && !document.documentElement.doScroll)){
    main();
}else{
    document.addEventListener("DOMContentLoaded", main);
}

function main() {
    var inputTournament = document.getElementById('id_name');
    var inputStartDate = document.getElementById('begin');
    var inputEndDate = document.getElementById('end');
    inputTournament.addEventListener('change', function(e) {
        tournamentAjax(e, inputTournament);
    })
    inputStartDate.addEventListener('change', function(e) {
        dateAjax(e, inputStartDate, inputEndDate);
    })
    inputEndDate.addEventListener('change', function(e) {
        dateAjax(e, inputStartDate, inputEndDate);
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

function dateAjax(e, inputStartDate, inputEndDate) {
    const csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    var startDate = inputStartDate.value;
    var endDate = inputEndDate.value;
    console.log(startDate);
    console.log(endDate);

    $.ajaxSetup({
        headers:{
            "X-CSRFToken": csrf_token,
        }
    });

    $.ajax({
        url: 'checkDates/',
        data: JSON.stringify({'startDate':startDate, 'endDate':endDate}),
        type: 'PATCH',
        contentType: 'application/json',
        success: (response) => {
            if (response.is_complete==true && response.is_valid==false) {
                $('#end').val('');
                $('#messageDivParent').html(
                    "<div class='alert alert-warning'>The end date off the tournament must be after the start date.</div>"
                );
            }
        },
        failure: (response) => {
            console.log("FAILURE -> ", response);
        }
    })
}