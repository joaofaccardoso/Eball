if(document.readyState === "complete" || (document.readyState!== "loading" && !document.documentElement.doScroll)){
    main();
}else{
    document.addEventListener("DOMContentLoaded", main);
}

function main(){
    var buttons = document.getElementsByTagName("button");
    btnEvents(buttons)
}

function sendAjax(e, pk){
    const csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value
    $.ajaxSetup({
        headers:{
            "X-CSRFToken": csrf_token
        }
    });

    $.ajax({
        
        url: window.location.origin + "/is_seen/"+ pk + "/",
        data:JSON.stringify({ isSeen: true}),
        type: "PATCH",
        contentType:"application/json",
        success: (response_data)=>{
            window.location = '';
        },
        failure:(response_data)=>{
            console.log("FAILURE===", response_data);
        }
    });

}

function btnEvents(buttons) {
    console.log('entrei');
    for(let i=0;i<buttons.length;i++){        
        buttons[i].addEventListener("click", function(e){
            sendAjax(e, buttons[i].name);
        })
    }
}