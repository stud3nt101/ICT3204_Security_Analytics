var dom = document.getElementById("bubblechart");
var myChart = new Chart(dom, {
    type: 'bubble',
    data: {
        datasets: [{
            label: '192.10.3.2',
            data: [{x: 5, y: 4, r: 3}],
            backgroundColor: "#2E2D4D"
        }, {
            label: '172.10.3.1',
            data: [{x: 5, y: 4, r: 3}],
            backgroundColor: '#227C9D'
        }, {
            label: '172.10.3.2',
            data: [{x: 5, y: 4, r: 3}],
            backgroundColor: '#EB5160'
        }, {
            label: '172.10.3.3',
            data: [{x: 5, y: 4, r: 3}],
            backgroundColor: '#F6BD60'
        }, {
            label: '172.10.3.10',
            data: [{x: 5, y: 4, r: 3}],
            backgroundColor: '#17C3B2'
        }, {
            label: '172.10.3.11',
            data: [{x: 5, y: 4, r: 3}],
            backgroundColor: '#83B692'
        }, {
            label: '172.10.5.0',
            data: [{x: 5, y: 4, r: 3}],
            backgroundColor: '#A6B1E1'
        }, {
            label: '172.10.5.1',
            data: [{x: 5, y: 4, r: 3}],
            backgroundColor: '#EEC8E0'
        }],
    },
    options: {
        aspectRatio: 3,
    }
})