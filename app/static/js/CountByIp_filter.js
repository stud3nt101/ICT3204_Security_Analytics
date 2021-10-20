function filter(){
    $.ajax({
        type:'POST',
        url:'/dashboard',
        data:{
          packetc_ip:$("#top").val(),
          loc:$("#loc").val()
        },
        success: function (html) {
            PacketbyIp(html);
        }
    })
};