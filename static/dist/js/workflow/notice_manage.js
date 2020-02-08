$("#noticeModal").on("hidden.bs.modal", function() {
    $(this).removeData("bs.modal");
    $("#notice_form")[0].reset();
    $("#nowNoticeFile").html('');
    $("#noticeId").val("");
});

  $('#notice_table').DataTable({
  ordering: false,
  "serverSide":true,
  "bFilter":true,
  "lengthMenu": [10, 25, 50, 100 ],
  "language": {
    "searchPlaceholder": "名称或描述模糊搜索"
  },

  ajax: function (data, callback, settings) {
    console.log(data);
    var param = {};
    param.per_page = data.length;//页面显示记录条数，在页面显示每页显示多少项的时候
    param.page = (data.start / data.length)+1;//当前页码
    param.search_value=data.search.value;
    console.log(param);
    $.ajax({
      type: "GET",
      url: "/api/v1.0/workflows/custom_notices",
      cache: false,  //禁用缓存
      data: param,  //传入组装的参数
      dataType: "json",
      success: function (result) {
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
      { "data": "name" },
      { "data": "description" },
      { "data": "creator" },
      { "data": "gmt_created" },
      {render: function(data, type, full){var rosJson=JSON.stringify(full).replace(/"/g, '&quot;');return ('<div><a  onclick="showEditForm(' + rosJson + ')' + '"' + '>编辑</a>/<a onclick="delNotice(' + full.id + ')' + '"'+  '>删除</a>')}}
  ]

})

function showEditForm(data){
    $("#noticeName").val(data.name);
    $("#noticeDesc").val(data.description);
    $("#hookUrl").val(data.hook_url);
    $("#hookToken").val(data.hook_token);
    $("#noticeId").val(data.id);
    $('#noticeModal').modal('show');
  }

function submitNotice(){
    var noticeId = $("#noticeId").val();
    var noticeName = $("#noticeName").val();
    var noticeDesc = $("#noticeDesc").val();
    var hookUrl = $("#hookUrl").val();
    var hookToken = $("#hookToken").val();
    var params = {};
    params.name = noticeName;
    params.description = noticeDesc;
    params.hook_url = hookUrl;
    params.hook_token = hookToken;

    if (!noticeId) {
      // add notice
      $.ajax({
      type: "POST",
      url: "/api/v1.0/workflows/custom_notices",
      cache: false,  //禁用缓存
      data: JSON.stringify(params),  //传入组装的参数
      dataType: "json",
      success: function(callback) {
        $('#noticeModal').modal('hide')
        swal({
            title: "编辑成功!",
            text: "2s自动关闭",
            icon: "success",
            showConfirmButton: false,
            timer:2000
          })
        $('#notice_table').dataTable()._fnAjaxUpdate();
      }
    });
    } else {
      // update notice
      $.ajax({
      type: "PATCH",
      url: "/api/v1.0/workflows/custom_notices/" + noticeId,
      cache: false,  //禁用缓存
      data: JSON.stringify(params),  //传入组装的参数
      dataType: "json",
      success: function(callback) {
        $('#noticeModal').modal('hide')
        swal({
            title: "编辑成功!",
            text: "2s自动关闭",
            icon: "success",
            showConfirmButton: false,
            timer:2000
          })
        $('#notice_table').dataTable()._fnAjaxUpdate();
      }
    });
    }
  };

  function delNotice(noticeId) {
    swal({
      title: "是否真的要删除此记录?",
      text: "本删除操作只标记记录的删除状态，脚本文件不会实际删除",
      icon: "warning",
      buttons: true,
      dangerMode: true,
    })
    .then(function(willDelete) {
      if (willDelete) {
        // 删除操作
        $.ajax({
        type: "DELETE",
        url: "/api/v1.0/workflows/custom_notices/" + noticeId,
        cache: false,  //禁用缓存
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        success: function (result) {
          if (result.code===0){
            // 刷新数据
            $('#notice_table').dataTable()._fnAjaxUpdate();
            // 关闭modal
            swal({
              title: "删除成功!",
              text: "2s自动关闭",
              icon: "success",
              showConfirmButton: false,
              timer:2000
            })
            }
          }
        });
      }
    });
  }