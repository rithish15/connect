function addtask(userid){

    var title=$("#titleinp").val();
    var date=$("#dateinp").val();
    var priority=$("#priorityinp").val();
    var description=$("#descinp").val();

    farmid = getCookie("farm_id");
    console.log(farmid);
    console.log('http://127.0.0.1:5010/newtask')
    var jsonstr = "{\"seton\":"   + date + "," + "\"about\":" + description  + "," + "\"priority\":" + priority + "," + "\"title\":" + title +"}"
    console.log(jsonstr);
    $.ajax({
        url : 'http://127.0.0.1:5010/newtask?farmid=' + farmid + '&userid=' + userid,
        type : 'POST',
        cors : true,
        headers: {
        'Access-Control-Allow-Origin': '*',
        },
        contentType: 'application/json',
        data : jsonstr,
        success : function(data)
        {
            console.log(data.result);
        }
     });



}