var dataset = packetbyip_data;
var ipChart;

function destroyChart(){
    ipChart.destroy()
}

function sort(obj){
    items = Object.keys(obj).map(function(key) {
        return [key, obj[key]];
    });
    items.sort(function(first, second) {
        return second[1] - first[1];
    });
    sorted_obj={}
    $.each(items, function(k, v) {
        use_key = v[0]
        use_value = v[1]
        sorted_obj[use_key] = use_value
    })
    return(sorted_obj)
}

function PacketbyIp(data_input){
    if(typeof ipChart !== "undefined"){
        destroyChart()
    }

    var dom = document.getElementById("PacketByIp");
    var parsedData= [];
    var parsedLabel = [];
    var datas = [];
    var color = [
          '#2E2D4D',
          '#227C9D',
          '#EB5160',
          '#F6BD60',
          '#17C3B2',
          '#83B692',
          '#A6B1E1',
          '#EEC8E0',
          '#CC2936',
          '#136F63',
          '#CAE7B9',
          '#E7EB90',
          '#826251',
          '#FF7F11'
    ]

    data_input = sort(data_input)

    for (var i = 0; i < Object.keys(data_input).length; i++) {
        parsedLabel.push(Object.keys(data_input)[i])
        datas.push({
            label: Object.keys(data_input)[i],
            data: [Object.values(data_input)[i]],
            backgroundColor: color[i],
            borderWidth: 1,
            barPercentage: 0.5
        })
    }

    ipChart = new Chart(dom, {
        type: 'bar',
        data: {
            labels: " ",
            datasets: datas,
        },
        options: {
            aspectRatio: 3,
            indexAxis: 'y',
        }
    })
}

PacketbyIp(dataset)
