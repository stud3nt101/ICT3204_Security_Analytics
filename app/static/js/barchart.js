var dom = document.getElementById("PacketByTime");
var dataset = packetbytime_data;
var iptimeChart;

function destroyChart(){
    iptimeChart.destroy()
}

function timeline(datas){
    if(typeof iptimeChart !== "undefined"){
        destroyChart()
    }

    var parsedData= [];
    var parsedLabel = [];

    for (var i = 0; i < Object.keys(datas).length; i++) {
        parsedLabel.push(Object.keys(datas)[i])
        parsedData.push(Object.values(datas)[i])
    }

    iptimeChart = new Chart(dom, {
        type: 'line',
        data: {
            labels: parsedLabel,
            datasets: [{
                data: parsedData,
                backgroundColor: "#EB5160",
                borderWidth: 1,
                barPercentage: 0.5
            }],
        },
        options: {
            aspectRatio: 3,
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    })
}

timeline(dataset)