function filter(){
    $.ajax({
        type:'POST',
        url:'/portcomm',
        data:{
          srcip:$("#srcip-select").val(),
          dstip:$("#dstip-select").val(),
          filterdata: $("#data-select").val()
        },
        success: function (html) {
          heatmap(JSON.parse(html));
        }
    })
};