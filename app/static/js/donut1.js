var dom = document.getElementById("donut_traffic");
var myChart = new Chart(dom, {
    type: 'doughnut',
    data: {labels: [
    'HTTP',
    'FTP',
    'SSH',
    'SSL',
    'SMB'
],
  datasets: [{
    label: 'Data by service',
    data: [300, 50, 100, 200, 132],
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
    hoverOffset: 4
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