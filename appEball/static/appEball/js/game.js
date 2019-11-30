if(document.readyState === "complete" || (document.readyState!== "loading" && !document.documentElement.doScroll)){
    main();
}else{
    document.addEventListener("DOMContentLoaded", main);
}

function main(){
    var minusTeam1 = document.getElementById('minus1');
    var plusTeam1 = document.getElementById('plus1');
    var minusTeam2 = document.getElementById('minus2');
    var plusTeam2 = document.getElementById('plus2');
    var inputTeam1 = document.getElementById('team1Input');
    var inputTeam2 = document.getElementById('team2Input');

    minusTeam1.addEventListener('click', function(e) {
        minus(e, inputTeam1);
    });
    plusTeam1.addEventListener('click', function(e) {
        plus(e, inputTeam1);
    });
    minusTeam2.addEventListener('click', function(e) {
        minus(e, inputTeam2);
    });
    plusTeam2.addEventListener('click', function(e) {
        plus(e, inputTeam2);
    });
}

function minus(e, inputTeam) {
    var teamResult = inputTeam.value;
    if (teamResult>0) {
        inputTeam.value = parseInt(teamResult) -1;
    }
}

function plus(e, inputTeam) {
    var teamResult = inputTeam.value;
    inputTeam.value = parseInt(teamResult) +1;
}