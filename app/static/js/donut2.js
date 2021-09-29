var dom = document.getElementById("donut_ip");
var myChart = new Chart(dom, {
    type: 'doughnut',
    data: { labels: [
        '192.168.1.2',
        '172.10.3.1',
        '172.10.3.2',
        '172.10.2.5',
        '172.10.3.8',
        '172.10.3.10'
    ],
    datasets: [{
        label: 'Data by service',
        data: [50, 25, 18, 20, 13],
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