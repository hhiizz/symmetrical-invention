// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Bar Chart Example
function bar(key,value,name,type){
  if(type == '%'){
    var ctx = document.getElementById("myBarChart");
    var myLineChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: key,
        datasets: [{
          label:name,
          borderColor: "rgba(2,117,216,1)",
          backgroundColor: "rgba(255, 255, 255, 0)",
          data: value,
        }],
      },
      options: {
        scales: {
          xAxes: [{
            time: {
              unit: 'month'
            },
            gridLines: {
              display: false
            },
          }],
          yAxes: [{
            ticks: {
              maxTicksLimit: 5,
              callback: function(value) {
                return value + "%"
              }
              ,
            },
            gridLines: {
              display: true
            }
          }],
        },
      }
    });
  }else{
    var ctx = document.getElementById("myBarChart");
    var myLineChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: key,
        datasets: [{
          label:name,
          borderColor: "rgba(2,117,216,1)",
          backgroundColor: "rgba(255, 255, 255, 0)",
          data: value,
        }],
      },
      options: {
        scales: {
          xAxes: [{
            time: {
              unit: 'month'
            },
            gridLines: {
              display: false
            },
          }],
          yAxes: [{
            ticks: {
              maxTicksLimit: 5,
              callback: function(value) {if (value % 1 === 0) {return value;}
              },
            },
            gridLines: {
              display: true
            }
          }],
        },
      }
    });

  }


}


function bar_admin(key,value,name){
    var ctx = document.getElementById("myBarChart");
    var myLineChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: key,
        datasets: [{
          label:name,
          borderColor: "rgba(12,117,216,0.6)",
          backgroundColor: "rgba(255, 255, 255, 0.7)",
          data: value,
        }],
      },
      options: {
        scales: {
          xAxes: [{
            time: {
              unit: 'month'
            },
            gridLines: {
              display: false
            },
          }],
          yAxes: [{
            ticks: {
              maxTicksLimit: 5,
              callback: function(value) {if (value % 1 === 0) {return value;}
              },
            },
            gridLines: {
              display: true
            }
          }],
        },
      }
    });

}


