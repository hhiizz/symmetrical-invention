// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Pie Chart Example
function doughnutchartjs(key,value){
  var ctx = document.getElementById("mydoughnutChart");
  if(value.length==1){
    var myPieChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels:key,
        datasets: [{
          data: value,
          backgroundColor: [ '#32CD32'],
        }],
      },
    });
  }else{
    var myPieChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels:key,
        datasets: [{
          data: value,
          backgroundColor: [ '#dc3545','#007bff', '#ffc107'],
        }],
      },
    });
  }


}