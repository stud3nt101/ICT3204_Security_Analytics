var chartDom = document.getElementById('heatmap');
var myChart = echarts.init(chartDom);
var option;

dataset = bubblechart_data;

function heatmap(datas){
    var keys = Object.keys(datas);
    var dataset = [];
    var duration = [];
    var bytes = [];
    var series = [];
    var value;

    for (let i = 0; i < keys.length; i++) {
      value = datas[keys[i]]
      duration.push(value["dur"])
      bytes.push(value["byte"])
    }

    bytes_list = (bytes.filter(onlyUnique)).sort(function(a, b){return a-b})
    duration_list = (duration.filter(onlyUnique)).sort(function(a, b){return a-b})

    for (let i = 0; i < keys.length; i++) {
      value = datas[keys[i]]
      series.push({
          name: keys[i],
          type: 'heatmap',
          data: [[duration_list.indexOf(value["dur"]), bytes_list.indexOf(value["byte"]), value["packet"]]],
          label: {
            show: true
          }
      })
    }

    option = {
      tooltip: {
        trigger : 'item',
        formatter: function(params) {
          return (
            '<b>Port number:</b> ' + params.seriesName +
            '<br><b>Total no. of packets:</b> ' + params.data[2] +
            '<br><b>Total no. of bytes:</b> ' + bytes_list[params.data[1]] +
            '<br><b>Total duration:</b> ' + duration_list[params.data[0]] +' ms'
          );
        }
      },
      grid: {
        height: '50%'
      },
      xAxis: {
        type: 'category',
        data: duration_list,
        name: 'Duration (ms)',
        splitArea: {
          show: true
        }
      },
      yAxis: {
        type: 'category',
        data: bytes_list,
        name: 'Byte size',
        splitArea: {
          show: true
        }
      },
      visualMap: {
            min: 0,
            max: 500,
            show: false
      },
      series: series,
    };

    option && myChart.setOption(option);
}

function onlyUnique(value, index, self) {
  return self.indexOf(value) === index;
}

heatmap(dataset)