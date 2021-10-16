var form = document.getElementById('hm_filter');

function filter(){
    $.ajax({
        type:'POST',
        url:'/dashboard',
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