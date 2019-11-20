if(document.readyState === "complete" || (document.readyState!== "loading" && !document.documentElement.doScroll)){
    main();
}else{
    document.addEventListener("DOMContentLoaded", main);
}

function main(){
    var button = document.getElementsByTagName("button");
    
    for(let i=0;i<button.length;i++){        
        button[i].addEventListener("click", function(e){
            sendAjax(e, button[i].name);
        })
    }
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
        // success: (d)=>{
        //     console.log("RESPONSE===", d);
        // },
        // failure:(d)=>{
        //     console.log("FAILURE===", d);
        // }
    });

}