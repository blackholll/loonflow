document.write("<script language=javascript src='/static/dist/js/common/useSelect2.js'></script>");
$("#workflow_form").validate();

$('#customNoticeSelect').select2({placeholderOption: "first", allowClear:true});
$( document ).ready(function() {
  // 获取通知列表
  $.ajax({
    type: "GET",
    url: "/api/v1.0/workflows/custom_notices",
    cache: false,  //禁用缓存
    data: {per_page: 10000},  //传入组装的参数
    dataType: "json",
    success: function (result) {
      console.log(result);
      if (result.code===0){
        result.data.value.map(function(currentValue,index,arr){$("#customNoticeSelect").append("<option value=" + "'" + currentValue.id + "'" + ">" + currentValue.name + "</option>");})
      }
    }
  });
  initSelect2Items(
    "/api/v1.0/accounts/users",
    '#workflowAdmin',
    makeUserOption
  );
});

$('#workflowAdmin').select2({allowClear: true});

function makeUserOption(data) {
  var user = data.username + '(id:' + data.id + ',alias:' + data.alias + ')'
  return "<option value=" + "'" + data.username + "'" + ">" + user + "</option>"
}

  $('#workflow_table').DataTable({
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
    param.from_admin='1';
    console.log(param);
    $.ajax({
      type: "GET",
      url: "/api/v1.0/workflows",
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
      {render: function(data, type, full){if (full.view_permission_check){return "是"}return "否"}},
      { "data": "creator" },
      { "data": "workflow_admin" },
      { "data": "gmt_created" },
      {render: function(data, type, full){var rosJson=JSON.stringify(full).replace(/"/g, '&quot;');return ('<div><a  onclick="showEditForm(' + rosJson + ')' + '"' + '>编辑</a>/<a onclick="delWorkflow(' + full.id + ')' + '"'+  '>删除</a>/<a target="_blank" href="/manage/workflow_manage/'+ full.id + '"'+ '>配置</a>/<a target="_blank" href="/manage/workflow_flow_chart/'+ full.id + '"'+ '>查看流程图</a></div>')}}
  ]

})
  function showEditForm(data){
    $("#workflowName").val(data.name);
    $("#workflowDesc").val(data.description);
    if(data.notices){
      var notice_ids_arr = data.notices.split(",");
      $("#customNoticeSelect").val(notice_ids_arr).trigger("change");
    }

    var workflow_admin_arr = data.workflow_admin.split(",");
    initSelect2Items(
        "/api/v1.0/accounts/users",
        '#workflowAdmin',
        makeUserOption,
        workflow_admin_arr
    );

    if (data.view_permission_check) {
      $('#viewPermissionCheck').attr('checked', true);
    } else {
      $('#viewPermissionCheck').attr('checked', false);
    };
    $("#limitExpression").val(data.limit_expression);
    $("#displayFormStr").val(data.display_form_str);
    $("#workflowId").val(data.id);
    $("#titleTemplate").val(data.title_template);
    $("#contentTemplate").val(data.content_template);

    $('#workflowModal').modal('show');
  }

  function submitWorkflow(){
    if (! $("#workflow_form").valid()) {
      return
    }
    var workflowId = $('#workflowId').val();
    var workflowName = $("#workflowName").val();
    var workflowDesc = $("#workflowDesc").val();
    var titleTemplate = $("#titleTemplate").val();
    var contentTemplate = $("#contentTemplate").val();
    // let noticeScriptSelect = $("#customNoticeSelect");
    var noticeScriptSelect = document.getElementById("customNoticeSelect");
    var noticeScriptSelectArray = [];
    for(i=0; i<noticeScriptSelect.length; i++){
      if(noticeScriptSelect.options[i].selected){
        noticeScriptSelectArray.push(noticeScriptSelect[i].value);
      };
    };
    var noticeScriptSelectStr = noticeScriptSelectArray.join(',');


    var workflowAdminSelect = document.getElementById("workflowAdmin");
    var workflowAdminArray = [];
    for(i=0; i<workflowAdminSelect.length; i++){
      if(workflowAdminSelect.options[i].selected){
        workflowAdminArray.push(workflowAdminSelect[i].value);
      };
    };
    var workflowAdminStr = workflowAdminArray.join(',');


    var limitExpression = $("#limitExpression").val();
    var displayFormStr = $("#displayFormStr").val();
    var viewPermissionCheck = 0
    if ($("#viewPermissionCheck").checked){
      viewPermissionCheck = 1;
    };
    if (!limitExpressionFormatCheck(limitExpression)){
      swal({
        title: "限制表达式不合法!",
        text: "限制表达式必须是字典对象的json格式。请按照提示输入合法的表达式",
        icon: "error",
        showConfirmButton: false,
        })
      return false;
    }
    if (!displayFormstrFormatCheck(displayFormStr)){
      swal({
        title: "工作流展示表单不合法!",
        text: "工作流展示表单必须是数组对象的json格式，请按照提示输入合法的表达式",
        icon: "error",
        showConfirmButton: false,
        })
      return false;
    }
    paramData = {
      name: workflowName,
      description: workflowDesc,
      notices: noticeScriptSelectStr,
      view_permission_check: viewPermissionCheck,
      limit_expression: limitExpression,
      display_form_str: displayFormStr,
      workflow_admin: workflowAdminStr,
      title_template: titleTemplate,
      content_template: contentTemplate,
    }
    if (!workflowId){
      $.ajax({
      url: "/api/v1.0/workflows",
      type: "POST",
      processDate: false,
      data : JSON.stringify(paramData),
      contentType: 'application/json',
      success: function(result){
        if (result.code===0) {
          $("#workflowModal").modal("hide");
          swal({
            title: "新增成功, 别忘了去'用户权限'-'调用权限'中给应用授权哦!",
            text: "2s自动关闭",
            showConfirmButton: false,
            timer: 2000,
          })
          $('#workflow_table').dataTable()._fnAjaxUpdate();
        } else {
          swal({
            title: "新增失败:" + result.msg,
            text: "2s自动关闭",
            showConfirmButton: false,
            timer: 2000,
            icon: 'error',
          })
        }

      }
    });
    } else{
      $.ajax({
      url: "/api/v1.0/workflows/" + workflowId,
      type: "PATCH",
      processDate: false,
      data : JSON.stringify(paramData),
      contentType: 'application/json',
      success: function(result){
        if (result.code===0) {
          $("#workflowModal").modal("hide");
          swal({
            title: "新增成功!",
            text: "2s自动关闭",
            showConfirmButton: false,
            timer: 2000,
          })
          $('#workflow_table').dataTable()._fnAjaxUpdate();
        } else {
          swal({
            title: "新增成功!",
            text: "2s自动关闭",
            showConfirmButton: false,
            timer: 2000,
            icon: "error"
          })
        }

      }
    });
    }
  }

  function limitExpressionFormatCheck(str){
    if (str.startsWith('{') && isJsonCheck(str)){
      return true;
    }
    return false
  }

  function displayFormstrFormatCheck(str){
    if (str.startsWith('[') && isJsonCheck(str)){
      return true;
    }
    return false
  }
  function isJsonCheck(str) {
    try {
        $.parseJSON(str);
    } catch (e) {
        return false;
    }
    return true;
}
  $("#workflowModal").on("hidden.bs.modal", function() {
    document.getElementById("workflow_form").reset(); //此操作无法清空select2中的内容
    $("#customNoticeSelect").val('').trigger('change')
  });

  function delWorkflow(workflowId) {
    swal({
      title: "是否真的要删除此记录?",
      text: "请确认没有此工作流的工单记录后再删除，否则包含此类工单的工单列表及工单详情都会有问题，慎重！！！",
      icon: "warning",
      buttons: true,
      dangerMode: true,
    })
    .then(function(willDelete) {
      if (willDelete) {
        // 删除操作
        $.ajax({
        type: "DELETE",
        url: "/api/v1.0/workflows/" + workflowId,
        cache: false,  //禁用缓存
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        success: function (result) {
          if (result.code===0){
            // 刷新数据
            $('#workflow_table').dataTable()._fnAjaxUpdate();
            swal({
              title: "删除成功!",
              text: "2s自动关闭",
              icon: "success",
              showConfirmButton: false,
              timer:2000
            })
            } else {
            swal({
              title: "删除失败：" + result.msg,
              text: "2s自动关闭",
              icon: "success",
              showConfirmButton: false,
              timer:2000,
              icon: "error"
            })
          }
          }
        });
      }
    }
    );
  }
