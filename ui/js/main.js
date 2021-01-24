window.chartColors = {
  pink: 'hsla(340, 82%, 52%, 0.75)',
  red: 'rgba(255, 99, 132, 0.75)',
  orange: 'rgba(255, 159, 64, 0.75)',
  yellow: 'rgba(255, 205, 86, 0.75)',
  green: 'rgba(75, 192, 192, 0.75)',
  blue: 'rgba(54, 162, 235, 0.75)',
  purple: 'rgba(153, 102, 255, 0.75)',
  grey: 'rgba(201, 203, 207, 0.75)'
};

const backgroundColors = [
  window.chartColors.pink,
  window.chartColors.blue,
  window.chartColors.orange,
  window.chartColors.purple,
  window.chartColors.red,
  window.chartColors.blue,
  window.chartColors.green,
]


function graph(element, title, data, unitf=x => x) {
  var ctx = document.getElementById(element).getContext('2d');

  var dates = data.map(x => x['date']);

  var datasets = [];

  var dataset_keys = Object.keys(data[0]).filter(x => x != 'date');

  for (i in dataset_keys) {
    datasets.push({
      'label': dataset_keys[i],
      'borderWidth': 1,
      'data': data.map(x => unitf(x[dataset_keys[i]])),
      'backgroundColor': backgroundColors[i % backgroundColors.length]
    })
  }


  console.log(datasets);
  var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: dates,
      datasets: datasets
    },
    options: {
      title: {
        display: true,
        text: title
      },
      responsive: true,
      tooltips: {
        mode: 'index',
        intersect: false
      },
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: true
          },
          stacked: true
        }],
        xAxes: [{
          stacked: true
        }]
      }
    }
  });
}


function getData() {
  fetch('./data.json')
    .then(response => response.json())
    .then(data => setupGraphs(data));
}

function bytesToMB(x) {
  return x/(1e6)
}

function setupGraphs(data) {
  console.log(data)
  graph('pageViewsChart', 'Page Views', data['views']);
  graph('requestsChart', 'Requests', data['requests']);
  graph('bytesChart', 'Bytes Transfered (in MB)', data['bytes'], bytesToMB);
  graph('cachedBytesChart', 'Cached Bytes Ratio', data['bytes_ratio']);
  graph('cachedRequestsChart', 'Cached Requests Ratio', data['requests_ratio']);
}

function main() {
  getData();
}


window.addEventListener('load', function () {
  main();
})

