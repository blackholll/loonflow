$('#search_workflow').select2({placeholderOption: "first", allowClear:true});

var table = $('#ticket_table').DataTable({
  ordering: false,
  searching : false,
  "processing": true,
  "serverSide":true,
  "bFilter":true,
  "lengthMenu": [10, 25, 50, 100 ],
  "language": {
    "searchPlaceholder": "名称或描述模糊搜索"
  },

  ajax: function (data, callback, settings) {
    var param = {};
    param.per_page = data.length;//页面显示记录条数，在页面显示每页显示多少项的时候
    param.page = (data.start / data.length)+1;//当前页码
    param.search_value=data.search.value;
    param.category='all';
    param.from_admin='1';
    var sn = $("#search_sn").val();
    var title = $("#search_title").val();
    var workflow_select = $("#search_workflow").val();
    var creator = $("#search_creator").val();
    var search_sn = $("#search_sn").val();
    if (sn) {
      param.sn=sn
    }
    if ($('#search_time_range').data('daterangepicker')) {
      param.create_start = $('#search_time_range').data('daterangepicker').startDate.format('YYYY-MM-DD HH:mm:ss')
    }
    if ($('#search_time_range').data('daterangepicker')) {
      param.create_end = $('#search_time_range').data('daterangepicker').endDate.format('YYYY-MM-DD HH:mm:ss');
    }
    if (creator) {
      param.creator=creator
    }
    if (title) {
      param.title=title
    }
    if(workflow_select){
      workflow_ids = workflow_select.join(',');
      param.workflow_ids=workflow_ids;
    }
    if(search_sn) {
      param.sn=search_sn
    }
    $.ajax({
      type: "GET",
      url: "/api/v1.0/tickets",
      cache: false,  //禁用缓存
      data: param,  //传入组装的参数
      dataType: "json",
      success: function (result) {
        if (result.code === -1){
          swal({
            title: "获取工单列表失败:" + result.msg,
            text: "2s自动关闭",
            icon: 'error',
            showConfirmButton: false,
            timer: 2000,
          })
        }
        var returnData = {};
        returnData.draw = data.draw;//这里直接自行返回了draw计数器,应该由后台返回
        returnData.recordsTotal = result.data.total;//返回数据全部记录
        returnData.recordsFiltered = result.data.total;//后台不实现过滤功能，每次查询均视作全部结果
        returnData.data = result.data.value;//返回的数据列表
        //console.log(returnData);
        //调用DataTables提供的callback方法，代表数据已封装完成并传回DataTables进行渲染
        //此时的数据需确保正确无误，异常判断应在执行此回调前自行处理完毕
        callback(returnData);
        },

    })

  },
  columns: [
      { "data": "id"},
      { "data": "sn" },
      { "data": "title" },
      {render: function(data, type, full){return full.workflow_info.workflow_name}},
      {render: function(data, type, full){return full.state.state_name}},
      {render: function(data, type, full){return full.participant_info.participant_alias}},
      {render: function(data, type, full){return full.creator_info.alias}},
      { "data": "gmt_created" },
      {render: function(data, type, full){
        var detail_link = '<a href ="/manage/ticket_manage/' + full.id + '"' +  '>详情</a>';
        var delDeptButton = '<a onclick="delTicket(' + full.id + ')' + '"' + '>删除</a>';
        return '<div>' + detail_link + '/' + delDeptButton + '</div>'}}

  ]

})
$('#search_time_range').daterangepicker({
  timePicker: true,
  startDate: moment().startOf('second').add(-1, 'year'),
  endDate: moment().startOf('second'),
  locale: {
      // format: 'M/DD hh:mm A'
      format: 'YYYY-MM-DD hh:mm:ss',
      cancelLabel: 'Clear'
    }
})
$('#search_time_range').on('apply.daterangepicker', function(ev, picker) {
      $(this).val(picker.startDate.format('YYYY-MM-DD HH:mm:ss') + ' - ' + picker.endDate.format('YYYY-MM-DD HH:mm:ss'));
  });

$('#search_time_range').on('cancel.daterangepicker', function(ev, picker) {
    newEndTime = moment().startOf('second');
    newStartTime = moment().startOf('second').add(-1, 'year');

    $('#search_time_range').val(newStartTime.format('YYYY-MM-DD HH:mm:ss') + '-' + newEndTime.format('YYYY-MM-DD HH:mm:ss') );

    $('#search_time_range').data('daterangepicker').setStartDate(newStartTime);
    $('#search_time_range').data('daterangepicker').setEndDate(newEndTime);
    // $(this).val('');
});


$( document ).ready(function() {
    // 获取用户有权限管理的工作流列表
    $.ajax({
      type: "GET",
      url: "/api/v1.0/workflows/user_admin",
      cache: false,  //禁用缓存
      dataType: "json",
      success: function (result) {
        if (result.code === 0) {
          result.data.map(function (currentValue, index, arr) {
            $("#search_workflow").append("<option value=" + "'" + currentValue.id + "'" + ">" + currentValue.name + "</option>");
          })
        }
      }

    })
  })

$('#search_creator').select2({
      placeholderOption: "first",
      allowClear:true,
      language: {
        searching: function() {
            return "输入创建人名称搜索...";
        }
    },
    ajax: {
      url: "/api/v1.0/accounts/users",
      delay: 300,
      dataType: 'json',
      data: function (params) {
        var query = {
          search_value: params.term,
          per_page: 10000,
        }
        return query;
      },
      processResults: function (data) {
      console.log('处理结果', data);
      return {
        results: data.data.value.map(function(item) {
          console.log(item.name);
          return {
            id: item.username,
            text: item.username + "(alias: " + item.alias + ")"
          };

        })
      };

    },
      },

    cache: true
    });

function searchTicket() {
  console.log('ssss212');
  table.ajax.reload();
}

function delTicket(ticketId) {
  swal({
      title: "是否真的要删除此记录?",
      text: "是否真的要删除该记录！！！",
      icon: "warning",
      buttons: true,
      dangerMode: true,
    })
    .then(function(willDelete){
      if (willDelete) {
        // 删除操作
        $.ajax({
        type: "DELETE",
        url: "/api/v1.0/tickets/" + ticketId,
        cache: false,  //禁用缓存
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        success: function (result) {
          if (result.code===0){
            // 刷新数据
            $('#ticket_table').dataTable()._fnAjaxUpdate();
            // 关闭modal
            swal({
            title: "删除成功!",
            text: "2s自动关闭",
            icon: "success",
            showConfirmButton: false,
            timer:2000
            })
            } else {
              swal({
              title: "删除失败:" + result.msg,
              text: "2s自动关闭",
              icon: "error",
              showConfirmButton: false,
              timer:2000
            })
            }

          }
        });
      }
    }
  )
}
