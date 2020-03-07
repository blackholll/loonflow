
$( document ).ready(function() {
    $.ajax({
      type: "GET",
      url: "/api/v1.0/tickets/num_statistics",
      cache: false,  //禁用缓存
      dataType: "json",
      success: function (result) {
        if (result.code === 0) {
          var data = result.data
          var chart = new G2.Chart({
          container: 'mountNode',
          forceFit: true,
          height: 600
        });
        chart.source(data, {
          day: {
            range: [0, 1]
          }
        });
        chart.tooltip({
          crosshairs: {
            type: 'line'
          }
        });
        chart.axis('count', {
          label: {
            formatter: function formatter(val) {
              return val + '个';
            }
          }
        });
        chart.line().position('day*count').color('type');
        chart.point().position('day*count').color('type').size(4).shape('circle').style({
          stroke: '#fff',
          lineWidth: 1
        });
        chart.render();

        }
      }

    })
  })


