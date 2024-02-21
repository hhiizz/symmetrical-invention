// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Area Chart Example

function AreaChart2(key,value,name){
  var ctx = document.getElementById("myAreaChart");
var myLineChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: key,
    datasets: [{
      label: name,
      lineTension: 0.3,
      backgroundColor: "rgba(2,117,216,0.2)",
      borderColor: "rgba(2,117,216,1)",
      pointRadius: 5,
      pointBackgroundColor: "rgba(2,117,216,1)",
      pointBorderColor: "rgba(255,255,255,0.8)",
      pointHoverRadius: 5,
      pointHoverBackgroundColor: "rgba(2,117,216,1)",
      pointHitRadius: 50,
      pointBorderWidth: 2,
      data: value,
    }],
  },
  options: {
    scales: {
      xAxes: [{
        time: {
          unit: 'date'
        },
        gridLines: {
          display: false
        },
        ticks: {
        }
      }],
      yAxes: [{
        ticks: {
          min: 0,
        },
        gridLines: {
          color: "rgba(0, 0, 0, .125)",
        }
      }],
    },
  }
});

}

function AreaChart(key,value,value2){
  var ctx = document.getElementById("myAreaChart");
var myLineChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: key,
    datasets: [{
      label: "今年數量",
      lineTension: 0.3,
      backgroundColor: "rgba(2,117,216,0.2)",
      borderColor: "rgba(2,117,216,1)",
      pointRadius: 5,
      pointBackgroundColor: "rgba(2,117,216,1)",
      pointBorderColor: "rgba(255,255,255,0.8)",
      pointHoverRadius: 5,
      pointHoverBackgroundColor: "rgba(2,117,216,1)",
      pointHitRadius: 50,
      pointBorderWidth: 2,
      data: value,
    },{
      type: 'line',
      label: '去年數量',
      data: value2,
      borderColor: 'rgba(255, 99, 132, 1)',
      backgroundColor:'rgba(255, 99, 132, 0.05)'
    }],
  },
  options: {
    scales: {
      xAxes: [{
        time: {
          unit: 'date'
        },
        gridLines: {
          display: false
        },
        ticks: {
        }
      }],
      yAxes: [{
        ticks: {
          min: 0,
        },
        gridLines: {
          color: "rgba(0, 0, 0, .125)",
        }
      }],
    },
  }
});

}


function AreaChart_auto(key,value,name,id){
  var ctx = document.getElementById(id);
var myLineChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: key,
    datasets: [{
      label: name,
      lineTension: 0.3,
      backgroundColor: "rgba(2,117,216,0.2)",
      borderColor: "rgba(2,117,216,1)",
      pointRadius: 5,
      pointBackgroundColor: "rgba(2,117,216,1)",
      pointBorderColor: "rgba(255,255,255,0.8)",
      pointHoverRadius: 5,
      pointHoverBackgroundColor: "rgba(2,117,216,1)",
      pointHitRadius: 50,
      pointBorderWidth: 2,
      data: value,
    }],
  },
  options: {
    scales: {
      xAxes: [{
        time: {
          unit: 'date'
        },
        gridLines: {
          display: false
        },
        ticks: {
          stepSize:  30,
        }
      }],
      yAxes: [{
        ticks: {
          min: 0,
        },
        gridLines: {
          color: "rgba(0, 0, 0, .125)",
        }
      }],
    },
  }
});

}

function AreaChart_auto_recommend(key,value,name,id){
  var ctx = document.getElementById(id);
var myLineChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: key,
    datasets: [{
      label: name,
      lineTension: 0.3,
      backgroundColor: [ 'rgba(0,201,87,0.3)','rgba(255,0,0,0.3)'],
      borderColor: ['rgba(2,11,216,0.2)'],
      pointRadius: 5,
      pointBackgroundColor: "rgba(2,117,216,1)",
      pointBorderColor: "rgba(255,255,255,0.8)",
      pointHoverRadius: 5,
      pointHoverBackgroundColor: "rgba(2,117,216,1)",
      pointHitRadius: 50,
      pointBorderWidth: 2,
      data: value,
    }],
  },
  options: {
    scales: {
      xAxes: [{
        time: {
          unit: 'date'
        },
        gridLines: {
          display: false
        },
        ticks: {
          stepSize:  30,
        }
      }],
      yAxes: [{
        ticks: {
          min: 0,
        },
        gridLines: {
          color: "rgba(0, 0, 0, .125)",
        }
      }],
    },
  }
});

}
// function AreaChart(key,value,value2){
//   var ctx = document.getElementById("myAreaChart");
// var myLineChart = new Chart(ctx, {
//   type: 'bar',
//   data: {
//     labels: key,
//     datasets: [{
//       label: "今年",
//       lineTension: 0.3,
//       backgroundColor: "rgba(2,117,216,0.2)",
//       borderColor: "rgba(2,117,216,1)",
//       pointRadius: 5,
//       pointBackgroundColor: "rgba(2,117,216,1)",
//       pointBorderColor: "rgba(255,255,255,0.8)",
//       pointHoverRadius: 5,
//       pointHoverBackgroundColor: "rgba(2,117,216,1)",
//       pointHitRadius: 50,
//       pointBorderWidth: 2,
//       data: value,
//     },{
//       type: 'line',
//       label: '去年',
//       data: value2,
//       borderColor: 'rgba(255, 99, 132, 1)',
//       backgroundColor:'rgba(255, 99, 132, 0.05)'
//     }],
//   },
//   options: {
//     scales: {
//       xAxes: [{
//         time: {
//           unit: 'date'
//         },
//         gridLines: {
//           display: false
//         },
//         ticks: {
//         }
//       }],
//       yAxes: [{
//         ticks: {
//           min: 0,
//         },
//         gridLines: {
//           color: "rgba(0, 0, 0, .125)",
//         }
//       }],
//     },
//   }
// });

// }