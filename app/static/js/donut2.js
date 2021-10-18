var dom = document.getElementById("donut_ip");
var dataset = donut2_data;
var parsedData= [];
var parsedLabel = [];

for (var i = 0; i < Object.keys(dataset).length; i++) {
    parsedLabel.push(Object.keys(dataset)[i],)
    parsedData.push(parseInt(Object.values(dataset)[i]))
}

var myChart = new Chart(dom, {
    type: 'doughnut',
    data: { labels: parsedLabel,
    datasets: [{
        label: 'Data by service',
        data: parsedData,
        backgroundColor: [
          '#2E2D4D',
          '#227C9D',
          '#EB5160',
          '#F6BD60',
          '#17C3B2',
          '#83B692',
          '#A6B1E1',
          '#EEC8E0'
    ],
    hoverOffset: 4,
    borderWidth: 0,
  }]},
    options: {
        aspectRatio: 2,
        plugins: {
            legend: {
                display: true,
                position: 'right',
                align: 'center',
            }

        }
    }
})