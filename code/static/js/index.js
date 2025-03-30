// 柱状图1模块
(function () {

  $.ajax({
                                            url: '/comment_analysis/',
                                            type: 'GET',
                                            success: function (result) {
                                                  // 实例化对象
                                                var myChart = echarts.init(document.querySelector(".bar .chart"));
                                                // 指定配置和数据
                                                var option = {
                                                  color: ["#2f89cf"],
                                                  tooltip: {
                                                    trigger: "axis",
                                                    axisPointer: {
                                                      // 坐标轴指示器，坐标轴触发有效
                                                      type: "shadow" // 默认为直线，可选为：'line' | 'shadow'
                                                    }
                                                  },
                                                  grid: {
                                                    left: "0%",
                                                    top: "10px",
                                                    right: "0%",
                                                    bottom: "4%",
                                                    height: '130px'
                                                  },
                                                  xAxis: [
                                                    {
                                                      type: "category",
                                                      data: result.map(data => data.key),
                                                      axisTick: {
                                                        alignWithLabel: true
                                                      },
                                                      axisLabel: {
                                                        textStyle: {
                                                          color: "rgba(255,255,255,.6)",
                                                          fontSize: "12"
                                                        },
                                                          interval: 0, // 显示所有刻度
                                                          rotate: 90
                                                      },
                                                    }
                                                  ],
                                                  yAxis: [
                                                    {
                                                      type: "value",
                                                      axisLabel: {
                                                        textStyle: {
                                                          color: "rgba(255,255,255,.6)",
                                                          fontSize: "12"
                                                        }
                                                      },
                                                      axisLine: {
                                                        lineStyle: {
                                                          color: "rgba(255,255,255,.1)"
                                                        }
                                                      },
                                                      splitLine: {
                                                        lineStyle: {
                                                          color: "rgba(255,255,255,.1)"
                                                        }
                                                      }
                                                    }
                                                  ],
                                                  series: [
                                                    {
                                                      name: "直接访问",
                                                      type: "bar",
                                                      barWidth: "35%",
                                                      data: result.map(data => data.value),
                                                      itemStyle: {
                                                        barBorderRadius: 5
                                                      }
                                                    }
                                                  ]
                                                };

                                                  myChart.setOption(option);
                                            },
                                            fail: function (xhr, textStatus, errorThrown) {
                                                alert('request failed');
                                            },
                                            error: function (jqXHR, exception) {
                                                console.log(jqXHR.status);
                                                console.log(exception);
                                            }
                                        });

})();

// 折线图定制
(function () {

  $.ajax({
                                            url: '/years_analysis_dash/',
                                            type: 'GET',
                                            success: function (result) {
                                                   // 基于准备好的dom，初始化echarts实例
                                                  var myChart = echarts.init(document.querySelector(".line .chart"));

                                                  // 2. 指定配置和数据
                                                  var option = {
                                                    color: ["#00f2f1"],
                                                    tooltip: {
                                                      trigger: "axis",
                                                      formatter: "{a} <br/>{b} : {c}"
                                                    },
                                                    grid: {
                                                      top: "20%",
                                                      left: "3%",
                                                      right: "4%",
                                                      bottom: "3%",
                                                      containLabel: true
                                                    },

                                                    xAxis: {
                                                      type: "category",
                                                      boundaryGap: false,
                                                      data: result.map(item => item.key),
                                                      axisLabel: {
                                                        color: "rgba(255,255,255,.7)"
                                                      }
                                                    },
                                                    yAxis: {
                                                      type: "value",
                                                      axisLabel: {
                                                        color: "rgba(255,255,255,.7)"
                                                      },
                                                      splitLine: {
                                                        lineStyle: {
                                                          color: "#012f4a"
                                                        }
                                                      }
                                                    },
                                                    series: [
                                                      {
                                                        name: "平均评价数",
                                                        type: "line",
                                                        smooth: true,
                                                        data: result.map(item => item.value)
                                                      }
                                                    ]
                                                  };

                                                  myChart.setOption(option);
                                            },
                                            fail: function (xhr, textStatus, errorThrown) {
                                                alert('request failed');
                                            },
                                            error: function (jqXHR, exception) {
                                                console.log(jqXHR.status);
                                                console.log(exception);
                                            }
                                        });

})();

// 饼形图定制


// 折线图定制
(function () {

  $.ajax({
                                            url: '/tags_analysis/',
                                            type: 'GET',
                                            success: function (result) {
                                                   // 基于准备好的dom，初始化echarts实例
                                                var myChart = echarts.init(document.querySelector(".pie .chart"));

                                                option = {
                                                  tooltip: {
                                                    trigger: "item",
                                                    formatter: "{a} <br/>{b}: {c} ({d}%)",
                                                    position: function (p) {
                                                      //其中p为当前鼠标的位置
                                                      return [p[0] + 10, p[1] - 10];
                                                    }
                                                  },
                                                  legend: {
                                                    top: "90%",
                                                    itemWidth: 10,
                                                    itemHeight: 10,
                                                    data: result.map(data => data.name),
                                                    textStyle: {
                                                      color: "rgba(255,255,255,.5)",
                                                      fontSize: "12"
                                                    }
                                                  },
                                                  series: [
                                                    {
                                                      name: "电商产品数量",
                                                      type: "pie",
                                                      center: ["50%", "42%"],
                                                      radius: ["40%", "60%"],
                                                      color: [
                                                        "#065aab",
                                                        "#066eab",
                                                        "#0682ab",
                                                        "#0696ab",
                                                        "#06a0ab",
                                                        "#06b4ab",
                                                        "#06c8ab",
                                                        "#06dcab",
                                                        "#06f0ab"
                                                      ],
                                                      label: { show: false },
                                                      labelLine: { show: false },
                                                      data: result
                                                    }
                                                  ]
                                                };
                                               // 使用刚指定的配置项和数据显示图表。
                                                myChart.setOption(option);
                                            },
                                            fail: function (xhr, textStatus, errorThrown) {
                                                alert('request failed');
                                            },
                                            error: function (jqXHR, exception) {
                                                console.log(jqXHR.status);
                                                console.log(exception);
                                            }
                                        });
})();


//获取电商产品总量、标签总量
(function () {

  $.ajax({
                                            url: '/total_data/',
                                            type: 'GET',
                                            success: function (result) {
                                                $('#totalMovie').text(result.total_products);
                                                $('#totalTag').text(result.total_tags);
                                                $('#totalSelf').text(result.total_self);
                                                $('#totalNotSelf').text(result.total_notself);
                                            },
                                            fail: function (xhr, textStatus, errorThrown) {
                                                alert('request failed');
                                            },
                                            error: function (jqXHR, exception) {
                                                console.log(jqXHR.status);
                                                console.log(exception);
                                            }
                                        });

})();


//不同电商产品标签的平均价格
(function () {

   $.ajax({
                                            url: '/years_analysis/',
                                            type: 'GET',
                                            success: function (result) {
                                                  var myChart = echarts.init(document.querySelector(".line1 .chart"));

                                                  option = {
                                                      title: {
                                                          left: 'center',
                                                         textStyle: {
                                                            color: 'white', // 标题文字颜色

                                                         },
                                                         top: '10%', // 标题距离容器顶部的距离
                                                      },
                                                      tooltip: {
                                                        trigger: 'axis',
                                                        axisPointer: {
                                                          type: 'shadow'
                                                        }
                                                      },
                                                      legend: {},
                                                      grid: {
                                                        left: '3%',
                                                        right: '4%',
                                                        bottom: '3%',
                                                          top:'20%',
                                                        containLabel: true
                                                      },
                                                      xAxis: {
                                                        type: 'value',
                                                        boundaryGap: [0, 0.01],
                                                          axisLabel: {
                                                                textStyle: {
                                                                    color: 'white' // 设置文字颜色为红色
                                                                }
                                                            }
                                                      },
                                                      yAxis: {
                                                        type: 'category',
                                                        data: result.map(data => data.key),
                                                         axisLabel: {
                                                              textStyle: {
                                                                  color: 'white', // 设置x轴文字颜色为白色
                                                                  fontSize: 10
                                                              }
                                                        }
                                                      },
                                                      series: [
                                                        {
                                                          type: 'bar',
                                                          data: result.map(data => data.value),
                                                          barCategoryGap: '30%', // 设置柱子之间的间距
                                                          itemStyle: {
                                                            color: function() {
                                                                return 'rgb(' + Math.round(Math.random() * 255) + ',' + Math.round(Math.random() * 255) + ',' + Math.round(Math.random() * 255) + ')';
                                                            }
                                                        }
                                                        }
                                                      ]
                                                    };

                                                  myChart.setOption(option);
                                            },
                                            fail: function (xhr, textStatus, errorThrown) {
                                                alert('request failed');
                                            },
                                            error: function (jqXHR, exception) {
                                                console.log(jqXHR.status);
                                                console.log(exception);
                                            }
                                        });
})();


//自营店铺和非自营店铺比例
(function () {

   $.ajax({
                                            url: '/percent_analysis/',
                                            type: 'GET',
                                            success: function (result) {
                                                    // 1. 实例化对象
                                                  var myChart = echarts.init(document.querySelector(".pie1  .chart"));
                                                  // 2. 指定配置项和数据
                                                  var option = {
                                                    legend: {
                                                      top: "90%",
                                                      itemWidth: 10,
                                                      itemHeight: 10,
                                                      textStyle: {
                                                        color: "rgba(255,255,255,.5)",
                                                        fontSize: "12"
                                                      }
                                                    },
                                                    tooltip: {
                                                      trigger: "item",
                                                      formatter: "{a} <br/>{b} : {c} ({d}%)"
                                                    },
                                                    // 注意颜色写的位置
                                                    color: [
                                                      "#006cff",
                                                      "#60cda0",
                                                      "#ed8884",
                                                      "#ff9f7f",
                                                      "#0096ff",
                                                      "#9fe6b8",
                                                      "#32c5e9",
                                                      "#1d9dff"
                                                    ],
                                                    series: [
                                                      {
                                                        name: "点位统计",
                                                        type: "pie",
                                                        // 如果radius是百分比则必须加引号
                                                        radius: ["10%", "70%"],
                                                        center: ["50%", "42%"],
                                                        roseType: "radius",
                                                        data: result,
                                                        // 修饰饼形图文字相关的样式 label对象
                                                        label: {
                                                          fontSize: 10
                                                        },
                                                        // 修饰引导线样式
                                                        labelLine: {
                                                          // 连接到图形的线长度
                                                          length: 10,
                                                          // 连接到文字的线长度
                                                          length2: 10
                                                        }
                                                      }
                                                    ]
                                                  };

                                                  // 3. 配置项和数据给我们的实例化对象
                                                  myChart.setOption(option);
                                            },
                                            fail: function (xhr, textStatus, errorThrown) {
                                                alert('request failed');
                                            },
                                            error: function (jqXHR, exception) {
                                                console.log(jqXHR.status);
                                                console.log(exception);
                                            }
                                        });
})();

// 自动更新时间
function updateTime() {
    var now = new Date();
    document.querySelector(".showTime span").innerHTML = 
        now.getFullYear() + "-" + 
        (now.getMonth() + 1) + "-" +
        now.getDate() + " " +
        now.getHours() + ":" +
        now.getMinutes() + ":" +
        now.getSeconds();
}
setInterval(updateTime, 1000);

// 定时刷新数据
function refreshData() {
    $.get('/total_data/', function(data) {
        $('#totalMovie').text(data.total_products);
        $('#totalTag').text(data.total_tags);
        $('#totalSelf').text(data.total_self);
        $('#totalNotSelf').text(data.total_notself);
    });
    
    // 重新加载所有图表
    loadAllCharts();
}

// 每5分钟刷新一次数据
setInterval(refreshData, 300000);

// 初始加载
$(document).ready(function() {
    refreshData();
});