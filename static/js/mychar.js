

function change_img(type_img){
    var ctx = document.getElementById('myChart');
    console.log(values)
    console.log(keys)
    ctx.remove()
    $('.analysis_inner_image').append('<canvas id="myChart" width="200px" height="80%"></canvas>');
    var ctx = document.getElementById('myChart');
    if(type_img=='bar'){
        myChart = new Chart(ctx, {
            type: 'bar', //長條圖
            data: {
            //標題
            labels:  keys,
            datasets: [{
                label: '技能分析圖', //標籤
                data: values, //資料
                //圖表背景色
                backgroundColor: [
                  'rgba(255, 99, 132, 1)',
                  'rgba(54, 162, 235, 1)',
                  'rgba(255, 206, 86, 1)',
                  'rgba(75, 192, 192, 1)',
                  'rgba(153, 102, 255, 1)',
                  'rgba(255, 159, 64, 1)',
                  'rgba(250, 206, 86, 1)',
                  'rgba(175, 92, 192, 1)',
                  'rgba(153, 102, 55, 1)',
                  'rgba(255, 59, 64, 1)',
                ],
                //圖表外框線色
                borderColor: [
                  'rgba(255, 99, 132, 1)',
                  'rgba(54, 162, 235, 1)',
                  'rgba(255, 206, 86, 1)',
                  'rgba(75, 192, 192, 1)',
                  'rgba(153, 102, 255, 1)',
                  'rgba(255, 159, 64, 1)',
                  'rgba(250, 206, 86, 1)',
                  'rgba(175, 92, 192, 1)',
                  'rgba(153, 102, 55, 1)',
                  'rgba(255, 59, 64, 1)',
                ],
                //外框線寬度
                borderWidth: 1
            }]
            },
            options: {
              // maintainAspectRatio: true,
            scales: {
                yAxes: [{
                ticks: {
                    beginAtZero: true,
                    responsive: false //符合響應式
                },
                legend: {
                  display: true,
                  position:'bottom',
                  labels: {
                    fontSize:15,
                    boxWidth:40,
                    boxHeight:20,
                    padding:10,
                }
              },tooltips:{
                  bodyFontSize:15,
              }
                }]
            }
            }
        });
    }else if(type_img=='line'){
        myChart = new Chart(ctx, {
            type: 'line', //圖表類型
            data: {
            //標題
            labels: keys,
            datasets: [{
              label: '技能分析圖', //標籤
                data:  values, //資料
                //圖表背景色
                backgroundColor: [
                  'rgba(255, 99, 132, 0.2)',
                  'rgba(54, 162, 235, 1)',
                  'rgba(255, 206, 86, 1)',
                  'rgba(75, 192, 192, 1)',
                  'rgba(153, 102, 255, 1)',
                  'rgba(255, 159, 64, 1)',
                  'rgba(250, 206, 86, 1)',
                  'rgba(175, 92, 192, 1)',
                  'rgba(153, 102, 55, 1)',
                  'rgba(255, 59, 64, 1)',
                ],
                //圖表外框線色
                borderColor: [
                  'rgba(255, 99, 132, 1)',
                  'rgba(54, 162, 235, 1)',
                  'rgba(255, 206, 86, 1)',
                  'rgba(75, 192, 192, 1)',
                  'rgba(153, 102, 255, 1)',
                  'rgba(255, 159, 64, 1)',
                  'rgba(250, 206, 86, 1)',
                  'rgba(175, 92, 192, 1)',
                  'rgba(153, 102, 55, 1)',
                  'rgba(255, 59, 64, 1)',
                ],
                //外框線寬度
                borderWidth: 1
            }]
            },
            options: {
              // maintainAspectRatio: true,
            scales: {
                yAxes: [{
                ticks: {
                    beginAtZero: true,
                    responsive: false //符合響應式
                },
                legend: {
                  display: true,
                  position:'bottom',
                  labels: {
                    fontSize:15,
                    boxWidth:40,
                    boxHeight:20,
                    padding:10,
                }
              },tooltips:{
                  bodyFontSize:15,
              }
                }]
            }
            }
        });
    }else if(type_img=='radar'){
        myChart = new Chart(ctx, {
            type: 'radar', //圖表類型
            data: {
            //標題
            labels:  keys,
            datasets: [{
              label: '技能分析圖', //標籤
                data: values, //資料
                //圖表背景色
                backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
                ],
                //圖表外框線色
                borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
                ],
                //外框線寬度
                borderWidth: 1
            }]
            },
            options: {
              // maintainAspectRatio: true,
            scales: {
                yAxes: [{
                ticks: {
                    beginAtZero: true,
                    responsive: false //符合響應式
                },
                legend: {
                  display: true,
                  position:'bottom',
                  labels: {
                    fontSize:15,
                    boxWidth:40,
                    boxHeight:20,
                    padding:10,
                }
              },tooltips:{
                  bodyFontSize:15,
              }
                }]
            }
            }
        });
    }else if(type_img=='polarArea'){
         myChart = new Chart(ctx, {
            type: 'polarArea', //圖表類型
            data: {
            //標題
            labels:  keys,
            datasets: [{
              label: '技能分析圖', //標籤
                data: values, //資料
                //圖表背景色
                backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
                ],
                //圖表外框線色
                borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
                ],
                //外框線寬度
                borderWidth: 1
            }]
            },
            options: {
              // maintainAspectRatio: true,
            scales: {
                yAxes: [{
                ticks: {
                    beginAtZero: true,
                    responsive: false //符合響應式
                },
                legend: {
                  display: true,
                  position:'bottom',
                  labels: {
                    fontSize:15,
                    boxWidth:40,
                    boxHeight:20,
                    padding:10,
                }
              },tooltips:{
                  bodyFontSize:15,
              }
                }]
            }
            }
        });
    }else if(type_img=='pie'){
        var ctx = document.getElementById('myChart');
      myChart = new Chart(ctx, {
      type: 'pie', //圖表類型
      data: {
        //標題
        labels:  keys,
        datasets: [{
          label: '技能分析圖', //標籤
          data:  values, //資料
          //圖表背景色
          backgroundColor: [
            'rgba(255, 80, 80, 1)',
            'rgba(255, 80, 80, 0.9)',
            'rgba(255, 80, 80, 0.8)',
            'rgba(255, 80, 80,0.7)',
            'rgba(255, 80, 80, 0.6)',
            'rgba(255, 80, 80, 0.5)',
            'rgba(255, 80, 80, 0.4)',
            'rgba(255, 80, 80,0.3)',
            'rgba(255, 80, 80,0.2)',
            'rgba(255, 80, 80,0.1)',
          ],
          //圖表外框線色
          borderColor: [
            'rgba(255, 80, 80, 1)',
            'rgba(255, 80, 80, 0.9)',
            'rgba(255, 80, 80, 0.8)',
            'rgba(255, 80, 80,0.7)',
            'rgba(255, 80, 80, 0.6)',
            'rgba(255, 80, 80, 0.5)',
            'rgba(255, 80, 80, 0.4)',
            'rgba(255, 80, 80,0.3)',
            'rgba(255, 80, 80,0.2)',
            'rgba(255, 80, 80,0.1)',
          ],
          //外框線寬度
          borderWidth: 1
        }]
      },
      options: {
        maintainAspectRatio: true,
        scales: {
          yAxes: [{
            gridLines: {
                    display:false
            },
            ticks: {
              beginAtZero: true,
              responsive: true, //符合響應式
              display: false,
            }
          }]
        },
        legend: {
            display: true,
            position:'bottom',
            labels: {
              fontSize:15,
              boxWidth:40,
              boxHeight:20,
              padding:10,
          }
        },tooltips:{
            bodyFontSize:15,
        }
      }
    });
    }else if(type_img=='doughnut'){
        var ctx = document.getElementById('myChart');
       myChart = new Chart(ctx, {
      type: 'doughnut', //圖表類型
      data: {
        //標題
        labels: keys,
        datasets: [{
          label: '技能分析圖', //標籤
          data:  values, //資料
          //圖表背景色
          backgroundColor: [
            'rgba(255, 80, 80, 1)',
            'rgba(255, 80, 80, 0.9)',
            'rgba(255, 80, 80, 0.8)',
            'rgba(255, 80, 80,0.7)',
            'rgba(255, 80, 80, 0.6)',
            'rgba(255, 80, 80, 0.5)',
            'rgba(255, 80, 80, 0.4)',
            'rgba(255, 80, 80,0.3)',
            'rgba(255, 80, 80,0.2)',
            'rgba(255, 80, 80,0.1)',
          ],
          //圖表外框線色
          borderColor: [
            'rgba(255, 80, 80, 1)',
            'rgba(255, 80, 80, 0.9)',
            'rgba(255, 80, 80, 0.8)',
            'rgba(255, 80, 80,0.7)',
            'rgba(255, 80, 80, 0.6)',
            'rgba(255, 80, 80, 0.5)',
            'rgba(255, 80, 80, 0.4)',
            'rgba(255, 80, 80,0.3)',
            'rgba(255, 80, 80,0.2)',
            'rgba(255, 80, 80,0.1)',
          ],
          //外框線寬度
          borderWidth: 1
        }]
      },
      options: {
        maintainAspectRatio: true,
        scales: {
          yAxes: [{
            gridLines: {
                    display:false
            },
            ticks: {
              beginAtZero: true,
              responsive: true, //符合響應式
              display: false,
            }
          }]
        },
        legend: {
            display: true,
            position:'bottom',
            labels: {
              fontSize:15,
              boxWidth:40,
              boxHeight:20,
              padding:10,
          }
        },tooltips:{
            bodyFontSize:15,
        }
      }
    });

    }
}