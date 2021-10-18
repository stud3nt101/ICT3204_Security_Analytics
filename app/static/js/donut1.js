var dom = document.getElementById("donut_traffic");

var dataset = donut1_data;
var parsedData= [];
var parsedLabel = [];

var data;

for (var i = 0; i < Object.keys(dataset).length; i++) {
    parsedLabel.push(Object.keys(dataset)[i])
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
          '#EEC8E0',
          '#CC2936',
          '#136F63',
          '#CAE7B9',
          '#E7EB90',
          '#826251',
          '#FF7F11'
    ],
    hoverOffset: 4,
    borderWidth: 0,
  }]},
    options: {
        aspectRatio: 2,
        plugins: {
            legend: {
                position: 'right'
            }

        }
    }
})