var dom = document.getElementById("PacketBySrcip");
var dataset = packetbysrcip_data;
var parsedData= [];
var parsedLabel = [];

var datas = []

for (var i = 0; i < Object.keys(dataset).length; i++) {
    datas.push({
        label: Object.keys(dataset)[i],
        data: [Object.values(dataset)[i]],
        backgroundColor: "#EB5160",
        borderWidth: 1,
        barPercentage: 0.5
    })
}


var myChart = new Chart(dom, {
    type: 'bar',
    data: {
        labels: ['IP Address'],
        datasets: datas,
    },
    options: {
        aspectRatio: 3,
        indexAxis: 'y',
    }
})