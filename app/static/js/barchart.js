var dom = document.getElementById("PacketByTime");
var dataset = packetbytime_data;
var parsedData= [];
var parsedLabel = [];


for (var i = 0; i < Object.keys(dataset).length; i++) {
    parsedLabel.push(Object.keys(dataset)[i])
    parsedData.push(Object.values(dataset)[i])
}

var myChart = new Chart(dom, {
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