var dom = document.getElementById("barchart");
var myChart = new Chart(dom, {
    type: 'bar',
    data: {
        labels: ['IP Address'],
        datasets: [{
            label: '192.10.3.2',
            data: [543],
            backgroundColor: "#2E2D4D",
            borderWidth: 1,
            barPercentage: 0.5
        }, {
            label: '172.10.3.1',
            data: [542],
            backgroundColor: '#227C9D',
            borderWidth: 1,
            barPercentage: 0.5
        }, {
            label: '172.10.3.2',
            data: [284],
            backgroundColor: '#EB5160',
            borderWidth: 1,
            barPercentage: 0.5
        }, {
            label: '172.10.3.3',
            data: [196],
            backgroundColor: '#F6BD60',
            borderWidth: 1,
            barPercentage: 0.5
        }, {
            label: '172.10.3.10',
            data: [163],
            backgroundColor: '#17C3B2',
            borderWidth: 1,
            barPercentage: 0.5
        }, {
            label: '172.10.3.11',
            data: [483],
            backgroundColor: '#83B692',
            borderWidth: 1,
            barPercentage: 0.5
        }, {
            label: '172.10.5.0',
            data: [203],
            backgroundColor: '#A6B1E1',
            borderWidth: 1,
            barPercentage: 0.5
        }, {
            label: '172.10.5.1',
            data: [132],
            backgroundColor: '#EEC8E0',
            borderWidth: 1,
            barPercentage: 0.5
        }],
    },
    options: {
        aspectRatio: 3,
    }
})