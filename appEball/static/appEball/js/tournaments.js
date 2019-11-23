if(document.readyState === "complete" || (document.readyState!== "loading" && !document.documentElement.doScroll)){
    main();
}else{
    document.addEventListener("DOMContentLoaded", main);
}

function main(){
    var success_helper = function(response_data){
        window.location.href = "/tournaments/";
    }
    $("form").submit(function e){
        e.preventDefault();
        var type = this.id;
        var data = {
            "name":document.getElementById('input_${type}').value
        };
        console.log("DATA====",data);
        $.ajax({
            url: '${window.location.origin}/${type}/rest/list',
            data: data,
            dataType: "json",
            contentType: "application/json; charser=utf-8",
            success: (d) =>{
                success_helper(d)
            },
            // failure
        })
    }
}