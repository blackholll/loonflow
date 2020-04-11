  $(function () { $("[data-toggle='tooltip']").tooltip(); });
  $('#workflowSelect').select2({placeholderOption: "first", allowClear:true});

  $("#appTokenModal").on("hidden.bs.modal", function() {
    $(this).removeData("bs.modal");
    $("#token_form")[0].reset();
    $("#workflowSelect").val('').trigger('change')

  });

  $('#app_token_table').DataTable({
    ordering: false,
    "serverSide":true,
    "bFilter":true,
    "lengthMenu": [10, 25, 50, 100 ],
    "language": {
      "searchPlaceholder": "部门名或标签模糊搜索"
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
        url: "/api/v1.0/accounts/app_token",
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
        { "data": "app_name" },
        { "data": "token" },
        { "data": "ticket_sn_prefix" },
        { "data": "workflow_ids", render: function(data, type, full){return '<span class="d-inline-block" tabindex="0" data-toggle="tooltip" title="Disabled tooltip">' + data + '</span>'} },
        { "data": "creator_info", render: function(data, type, full) {if(data.creator_alias){return data.creator_alias}else{return data.creator_username}}},
        { "data": "gmt_created" },
        {render: function(data, type, full){var rosJson=JSON.stringify(full).replace(/"/g, '&quot;');return ('<div><a  onclick="showEditForm(' + rosJson + ')' + '"' + '>编辑</a>|<a onclick="delAppToken(' + full.id + ')' + '"'+  '>删除</a></div>')}}
    ]

  })
  $( document ).ready(function() {
    // 获取工作流选项
    $.ajax({
        type: "GET",
        url: "/api/v1.0/workflows",
        cache: false,  //禁用缓存
        data: {per_page: 10000},  //传入组装的参数
        dataType: "json",
        success: function (result) {
          console.log(result);
          if (result.code===0){
            result.data.value.map(function(currentValue,index,arr){$("#workflowSelect").append("<option value=" + "'" + currentValue.id + "'" + ">" + currentValue.name + "</option>");})
            }
          }


          });
  });
  function submitAppToken(){
    if (! $("#token_form").valid()) {
      return
    }
    var appTokenId = $('#appTokenId').val();
    if (!appTokenId){
      addAppToken()
    }
    else{
      // 编辑
      editAppToken();
    }
  }
  function editAppToken(){
    var appName = $('#inputAppName').val();
    var snPrefix = $('#ticketSnPrefix').val();
    var appTokenId = $('#appTokenId').val();

    var workflowSelect = document.getElementById("workflowSelect");
    var workflowArray = [];
    for(i=0;i<workflowSelect.length;i++){
        if(workflowSelect.options[i].selected){
          workflowArray.push(workflowSelect[i].value);
        }
    };
    var workflowSelerctStr = workflowArray.join(',');
    $.ajax({
        type: "PATCH",
        url: "/api/v1.0/accounts/app_token/" + appTokenId,
        cache: false,  //禁用缓存
        data: JSON.stringify({app_name: appName, ticket_sn_prefix: snPrefix, workflow_ids: workflowSelerctStr}),
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        success: function (result) {
          if (result.code===0){
            // 刷新数据
            $('#app_token_table').dataTable()._fnAjaxUpdate();
            // 关闭modal
            $('#appTokenModal').modal('hide');
            swal({
              title: "编辑成功!",
              text: "2s自动关闭",
              icon: "success",
              showConfirmButton: false,
              timer:2000
            })
            } else {
              swal({
                title: "编辑失败:" + result.msg,
                text: "2s自动关闭",
                icon: "error",
                showConfirmButton: false,
                timer:2000
              })
            }
          }
        });
  }

  function addAppToken(){
    var appName = $('#inputAppName').val();
    var snPrefix = $('#snPrefix').val();
    var workflowSelect = document.getElementById("workflowSelect");
    var workflowArray = [];
    for(i=0;i<workflowSelect.length;i++){
        if(workflowSelect.options[i].selected){
          workflowArray.push(workflowSelect[i].value);
        }
    }
    var workflowSelerctStr = workflowArray.join(',')
    $.ajax({
        type: "POST",
        url: "/api/v1.0/accounts/app_token",
        cache: false,  //禁用缓存
        data: JSON.stringify({app_name: appName, ticket_sn_prefix: snPrefix, workflow_ids: workflowSelerctStr}),
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        success: function (result) {
          if (result.code===0){
            // 刷新数据
            $('#app_token_table').dataTable()._fnAjaxUpdate();
            // 关闭modal
            $('#appTokenModal').modal('hide');
            swal({
              title: "新增成功!",
              text: "2s自动关闭",
              icon: "success",
              showConfirmButton: false,
              timer:2000
            })
            } else {
              swal({
                title: "新增失败:" + result.msg,
                text: "2s自动关闭",
                icon: "error",
                showConfirmButton: false,
                timer:2000
              })
            }
          }
        });
  }
  function showEditForm(data){
    $("#inputAppName").val(data.app_name);
    $("#ticketSnPrefix").val(data.ticket_sn_prefix);

    $("#appTokenId").attr("value",data.id);
    // $("#workflowSelect").attr("value",data.workflow_ids);
    var workflow_ids_arr = data.workflow_ids.split(",");
    $("#workflowSelect").val(workflow_ids_arr).trigger("change");
    $('#appTokenModal').modal('show');
  }

  function delAppToken(appTokenId){
    swal({
      title: "是否真的要删除此记录?",
      text: "删除此记录后，通过该记录中的应用名将无权限调用loonflow的接口",
      icon: "warning",
      buttons: true,
      dangerMode: true,
    })
    .then(function(willDelete) {
      if (willDelete) {
        // 删除操作
        $.ajax({
        type: "DELETE",
        url: "/api/v1.0/accounts/app_token/" + appTokenId,
        cache: false,  //禁用缓存
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        success: function (result) {
          if (result.code===0){
            // 刷新数据
            $('#app_token_table').dataTable()._fnAjaxUpdate();
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
