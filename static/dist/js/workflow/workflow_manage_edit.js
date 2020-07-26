
  $('#fieldType').select2({placeholderOption: "first", allowClear:true});
  // $('#subWorkflowId').select2({placeholderOption: "first", allowClear:true});
  $('#sourceStateId').select2({allowClear:true});
  $('#destinationStateId').select2({allowClear:true});

  $("#stateModal").on("hidden.bs.modal", function() {
    $(this).removeData("bs.modal");
    $("#subWorkflowId").val('').trigger('change');
    $("#workflow_state_form")[0].reset();
    $("#stateId").val("");
    $("#stateParticipantTypeIdDiv").show();
    $("#stateParticipantDiv").show();
  });
  $("#transitionModal").on("hidden.bs.modal", function() {
    $(this).removeData("bs.modal");
    $("#workflow_transiton_form")[0].reset();
    $("#transitionId").val("");
  });

function initStateItems(srcStateId, dstStateId) {
  let param = {};
  param.per_page = 1000;
  param.page = 1
  $.ajax({
    type: "GET",
    url: "/api/v1.0/workflows/" + getWorkflowId() + "/states",
    cache: false,  //禁用缓存
    data: param,  //传入组装的参数
    dataType: "json",
    success: function (result) {
      $("#sourceStateId").empty();
      result.data.value.map(function (currentValue, index, arr) {
        $("#sourceStateId").append(
          "<option value=" + "'" + currentValue.id + "'" + ">" + currentValue.name + "</option>"
        );
      })
      $("#sourceStateId").val(srcStateId).trigger("change");

      $("#destinationStateId").empty();
      result.data.value.map(function (currentValue, index, arr) {
        $("#destinationStateId").append(
          "<option value=" + "'" + currentValue.id + "'" + ">" + currentValue.name + "</option>"
        );
      })
      $("#destinationStateId").val(dstStateId).trigger("change");
    },
  });
}

  $("#customFieldModal").on("hidden.bs.modal", function() {
    $(this).removeData("bs.modal");
    $("#workflow_custom_field_form")[0].reset();
    $("#customFieldId").val("");
    $("#fieldType").val('').trigger('change')
  });
  $( document ).ready(function() {
    // 获取工作流详情
    $.ajax({
        type: "GET",
        url: "/api/v1.0/workflows/"+ getWorkflowId(),
        cache: false,  //禁用缓存
        dataType: "json",
        success: function (result) {
          if (result.code===0){
            $("#workflowName").append(result.data.name);
            }
          }
        });
    // 获取工作流列表，用于支持状态配置子工作流
    $.ajax({
    type: "GET",
    url: "/api/v1.0/workflows",
    cache: false,  //禁用缓存
    data: {per_page:500}, // 500 应该够了
    dataType: "json",
    success: function (result) {
      if (result.code===0){
            result.data.value.map(function(currentValue,index,arr){$("#subWorkflowId").append("<option value=" + "'" + currentValue.id + "'" + ">" + currentValue.name + "</option>");})
      }
      }
    });
    initStateItems();
  });
  $('#custom_field_table').DataTable({
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
      url: "/api/v1.0/workflows/"+ getWorkflowId() + "/custom_fields",
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
      { "data": "field_key"},
      { "data": "field_name"},
      {render: function(data, type, full){
        if (full.field_type_id === 5){
          return "字符型"
          } else if (full.field_type_id === 10){
            return "整型"
          } else if (full.field_type_id === 15){
            return "浮点型"
          } else if (full.field_type_id === 20){
            return "布尔型"
          } else if (full.field_type_id === 25){
            return "日期型"
          } else if (full.field_type_id === 30){
            return "日期时间型"
          } else if (full.field_type_id === 35){
            return "单选框"
          } else if (full.field_type_id === 40){
            return "多选框"
          } else if (full.field_type_id === 45){
            return "下拉列表"
          } else if (full.field_type_id === 50){
            return "下拉列表多选"
          } else if (full.field_type_id === 55){
            return "文本域"
          } else if (full.field_type_id === 60){
            return "用户名"
          } else if (full.field_type_id === 70){
            return "多选用户名"
          } else if (full.field_type_id === 80){
            return "附件"
          }
        return "未知";

        }},

      { "data": "order_id"},
      { "data": "description"},
      { "data": "creator"},
      { "data": "gmt_created"},
      {render: function(data, type, full){var rosJson=JSON.stringify(full).replace(/"/g, '&quot;');return ('<div><a  onclick="showEditForm(' + rosJson + ')' + '"' + '>编辑</a>/<a onclick="delCustomField(' + full.id + ')' + '"'+  '>删除</a></div>')}}

  ]
})
  $('#state_table').DataTable({
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
      url: "/api/v1.0/workflows/"+ getWorkflowId() + "/states",
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
      { "data": "name"},
      { "data": "is_hidden"},
      { "data": "order_id"},
      {render: function(data, type, full){
        if (full.type_id === 0){
          return "普通状态"
          } else if  (full.type_id === 1){
          return "初始状态"
          } else if  (full.type_id === 2){
          return "结束状态"
          }
          return "未知"
        }
        },
      {render: function(data, type, full){
        if (full.participant_type_id === 1){
          return "个人"
          } else if  (full.participant_type_id === 2){
          return "多人"
          } else if  (full.participant_type_id === 3){
          return "部门"
          } else if  (full.participant_type_id=== 4){
          return "角色"
          } else if  (full.participant_type_id=== 5){
          return "变量"
          } else if  (full.participant_type_id=== 6){
          return "脚本"
          } else if  (full.participant_type_id=== 7){
          return "工单字段"
          } else if  (full.participant_type_id=== 8){
          return "父工单字段"
          } else if  (full.participant_type_id=== 10){
          return "hook"
          } else if  (full.participant_type_id=== 0){
          return "N/A"
          }
          return "未知"
        }
        },
      {render: function(data, type, full){return full.participant_info.participant_alias}},
      {render: function(data, type, full){
          if (full.distribute_type_id === 1) {
            return '主动接单'
          } else if (full.distribute_type_id === 2) {
            return '直接处理'
          } else if (full.distribute_type_id === 3) {
            return '随机分配'
          } else if (full.distribute_type_id === 4) {
            return '全部处理'
          }
        }
      },
      { "data": "creator"},
      { "data": "gmt_created"},
      {render: function(data, type, full){var rosJson=JSON.stringify(full).replace(/"/g, '&quot;');return ('<div><a  onclick="showEditStateForm(' + rosJson + ')' + '"' + '>编辑</a>/<a onclick="delState(' + full.id + ')' + '"'+  '>删除</a></div>')}}

  ]
})
  $('#transition_table').DataTable({
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
      url: "/api/v1.0/workflows/"+ getWorkflowId() + "/transitions",
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
      { "data": "name"},
      {render: function(data, type, full){
        console.log(full.transition_type_id);
        if (full.transition_type_id === 1){
          return "常规流转"
          } else if  (full.transition_type_id === 2){
          return "定时器流转"
          }
          return "未知"
        }
        },
      { "data": "timer"},
      {render: function(data, type, full){return full.source_state_info.name}},
      {render: function(data, type, full){return full.destination_state_info.name}},

      { "data": "condition_expression"},
      {render: function(data, type, full){
        if (full.attribute_type_id===1){
          return '同意'
        } else if (full.attribute_type_id===2){
          return '拒绝'
        } else if (full.attribute_type_id===3){
          return '其他'
        }
      }},
      { "data": "field_require_check"},
      { "data": "alert_enable"},
      { "data": "creator"},
      { "data": "gmt_created"},
      {render: function(data, type, full){var rosJson=JSON.stringify(full).replace(/"/g, '&quot;');return ('<div><a  onclick="showEditTransitionForm(' + rosJson + ')' + '"' + '>编辑</a>/<a onclick="delTransition(' + full.id + ')' + '"'+  '>删除</a></div>')}}

  ]
})

function getWorkflowId() {
    var urlPath = window.location.pathname;
    var workflowId = Number(urlPath.split('/')[3]);
    return workflowId
}

  function fieldChoiceFormatCheck(str){
    if (str.startsWith('{') && isJsonCheck(str)){
      return true;
    }
    return false
  }

  function booleanFieldDisplayFormatCheck(str){
    if (str.startsWith('{') && isJsonCheck(str)){
      return true;
    }
    return false
  }
  function labelFormatCheck(str){
    if (str.startsWith('{') && isJsonCheck(str)){
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


  function showEditForm(data){
    $("#fieldKey").val(data.field_key);
    $("#fieldName").val(data.field_name);
    // $("#fieldType").val(data.field_type_id);
    $("#fieldType").val(data.field_type_id).trigger("change");
    $("#orderId").val(data.order_id);
    $("#defaultValue").val(data.default_value);
    $("#fieldDesc").val(data.description);
    $("#label").val(JSON.stringify(data.label));
    $("#booleanFieldDisplay").val(JSON.stringify(data.boolean_field_display));
    $("#fieldChoice").val(JSON.stringify(data.field_choice));
    $("#fieldTemplate").val(data.field_template);
    $("#customFieldId").val(data.id);
    // $("#subWorkflowId").val(data.sub_workflow_id)
    // $("#subWorkflowId").trigger("change");
    // $("#subWorkflowId").val(String(data.sub_workflow_id)).trigger("change");
    // $('#subWorkflowId').select2(String(data.sub_workflow_id));
    // select2 初始化有问题，暂时不用select2
    $("#subWorkflowId").val(String(data.sub_workflow_id));
    $('#customFieldModal').modal('show');
  }

  function submitCustomField(){
    if (! $("#workflow_custom_field_form").valid()) {
      return
    }
    var customFieldId = $('#customFieldId').val();
    var fieldKey = $("#fieldKey").val();
    var fieldName = $("#fieldName").val();
    var fieldType = $("#fieldType").val()
    var orderId = $("#orderId").val();
    var defaultValue = $("#defaultValue").val();
    var fieldDesc = $("#fieldDesc").val();
    var label = $("#label").val();
    var booleanFieldDisplay = $("#booleanFieldDisplay").val();
    var fieldChoice = $("#fieldChoice").val();
    var fieldTemplate = $("#fieldTemplate").val();
    if (!fieldChoiceFormatCheck(fieldChoice)){
      swal({
        title: "字段选项内容不合法!",
        text: "字段选项必须是字典对象的json格式。请按照提示输入合法的表达式",
        icon: "error",
        showConfirmButton: false,
        })
      return false;
    }
    if (!booleanFieldDisplayFormatCheck(booleanFieldDisplay)){
      swal({
        title: "布尔显示定义内容不合法!",
        text: "布尔显示定义必须是数组对象的json格式，请按照提示输入合法的表达式",
        icon: "error",
        showConfirmButton: false,
        })
      return false;
    }
    if (!labelFormatCheck(label)){
      swal({
        title: "标签定义内容不合法!",
        text: "标签定义定义必须是数组对象的json格式，请按照提示输入合法的表达式",
        icon: "error",
        showConfirmButton: false,
        })
      return false;
    }
    var paramData = {
      field_key: fieldKey,
      field_name: fieldName,
      field_type_id: Number(fieldType),
      order_id: Number(orderId),
      default_value: defaultValue,
      description: fieldDesc,
      label: label,
      field_template: fieldTemplate,
      boolean_field_display: booleanFieldDisplay,
      field_choice: fieldChoice,
    }

    if(!customFieldId){
      $.ajax({
      url: "/api/v1.0/workflows/" + getWorkflowId() + "/custom_fields",
      type: "POST",
      processDate: false,
      data : JSON.stringify(paramData),
      contentType: 'application/json',
      success: function(result){
        if (result.code === 0) {
          $("#customFieldModal").modal("hide");
          swal({
            title: "新增成功!",
            text: "2s自动关闭",
            showConfirmButton: false,
            timer: 2000,
          })
          $('#custom_field_table').dataTable()._fnAjaxUpdate();
        } else {
          swal({
            title: "新增失败:" + result.msg,
            text: "2s自动关闭",
            showConfirmButton: false,
            timer: 2000,
            icon: "error"
          })
        }

      }
    });
    }
    else{
      $.ajax({
      url: "/api/v1.0/workflows/" + getWorkflowId() + "/custom_fields/" + customFieldId,
      type: "PATCH",
      processDate: false,
      data : JSON.stringify(paramData),
      contentType: 'application/json',
      success: function(result){
        if (result.code ===0) {
          $("#customFieldModal").modal("hide");
          swal({
            title: "更新成功!",
            text: "2s自动关闭",
            showConfirmButton: false,
            timer: 2000,
          })
          $('#custom_field_table').dataTable()._fnAjaxUpdate();
        } else {
          swal({
            title: "更新失败:" + result.msg,
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

  function delCustomField(customFieldId){
    swal({
      title: "是否真的要删除此记录?",
      text: "请确认此字段未被使用(包括历史工单)后再删除，否则包含此类工单的工单列表及工单详情都会有问题，慎重！！！",
      icon: "warning",
      buttons: true,
      dangerMode: true,
    })
    .then(function(willDelete) {
      if (willDelete) {
        // 删除操作
        $.ajax({
        type: "DELETE",
        url: "/api/v1.0/workflows/" + getWorkflowId() + "/custom_fields/" + customFieldId,
        cache: false,  //禁用缓存
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        success: function (result) {
          if (result.code===0){
            // 刷新数据
            $('#custom_field_table').dataTable()._fnAjaxUpdate();
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
              icon: "success",
              showConfirmButton: false,
              timer:2000,
              icon: "error"
            })
          }
          }
        });
      }
    });
  }

  function showEditStateForm(data){
    $("#stateName").val(data.name);
    if (data.is_hidden) {
      $("#isHidden").attr('checked', true);
    } else {
      $("#isHidden").attr('checked', false);
    };
    if (data.enable_retreat) {
      $("#enableRetreat").attr('checked', true);
    } else {
      $("#enableRetreat").attr('checked', false);
    };
    
    if (data.remember_last_man_enable) {
      $("#RememberLastManEnable").attr('checked', true);
    } else {
      $("#RememberLastManEnable").attr('checked', false);
    }

    $("#stateOrderId").val(data.order_id);
    $("#stateTypeId").val(data.type_id);
    if (data.type_id !== 0){
      // 不显示参与人类型及参与人
      $("#stateParticipantTypeIdDiv").hide();
      $("#stateParticipantDiv").hide();
    }
    $("#stateParticipantTypeId").val(data.participant_type_id);
    $("#stateParticipant").val(data.participant);
    $("#stateDistributeTypeId").val(data.distribute_type_id);
    $("#stateFieldStr").val(JSON.stringify(data.state_field_str));
    $("#stateLabel").val(JSON.stringify(data.label));
    $("#stateId").val(data.id);
    $('#stateModal').modal('show');
  }

  function submitState(){
    if (! $("#workflow_state_form").valid()) {
      return
    }
    var stateName = $("#stateName").val();
    var subWorkflowId = $("#subWorkflowId").val();
    var isHidden = $("#isHidden").val();
    var stateOrderId = $("#stateOrderId").val();
    var stateTypeId = $("#stateTypeId").val();
    var RememberLastManEnable = $("#RememberLastManEnable").val();
    var stateParticipantTypeId = $("#stateParticipantTypeId").val();
    var stateParticipant = $("#stateParticipant").val();
    var stateDistributeTypeId = $("#stateDistributeTypeId").val();
    var stateFieldStr = $("#stateFieldStr").val();
    var stateLabel = $("#stateLabel").val();

    var RememberLastManEnable = 0
    if ($("#RememberLastManEnable").prop('checked')){
      RememberLastManEnable = 1;
    };
    var isHidden = 0
    if ($("#isHidden").prop('checked')){
      isHidden = 1;
    };
    var enableRetreat = 0
    if ($("#enableRetreat").prop('checked')){
      enableRetreat = 1;
    };

    if (!isJsonCheck(stateFieldStr)){
      swal({
        title: "状态字段内容不合法!",
        text: "状态字段选项必须是字典对象的json格式。请按照提示输入合法的表达式",
        icon: "error",
        showConfirmButton: false,
        })
      return false;
    }
    if (!isJsonCheck(stateLabel)){
      swal({
        title: "状态标签内容不合法!",
        text: "状态标签必须是字典对象(可以为空字典)的json格式，请按照提示输入合法的表达式",
        icon: "error",
        showConfirmButton: false,
        })
      return false;
    }

    var paramData = {
      name: stateName,
      is_hidden: Number(isHidden),
      order_id: Number(stateOrderId),
      type_id: Number(stateTypeId),
      remember_last_man_enable: Number(RememberLastManEnable),
      enable_retreat: Number(enableRetreat),
      participant_type_id: Number(stateParticipantTypeId),
      participant: stateParticipant,
      distribute_type_id: Number(stateDistributeTypeId),
      state_field_str: stateFieldStr,
      label: stateLabel,
    }

    var stateId = $('#stateId').val();
    if(!stateId){
      $.ajax({
      url: "/api/v1.0/workflows/" + getWorkflowId() + "/states",
      type: "POST",
      processDate: false,
      data : JSON.stringify(paramData),
      contentType: 'application/json',
      success: function(result){
        if (result.code === 0) {
          $("#stateModal").modal("hide");
          swal({
            title: "新增成功!",
            text: "2s自动关闭",
            showConfirmButton: false,
            timer: 2000,
          })
          $('#state_table').dataTable()._fnAjaxUpdate();
        } else {
          swal({
            title: "新增失败:" + result.msg,
            text: "2s自动关闭",
            showConfirmButton: false,
            timer: 2000,
            icon: "error"
          })
        }
      }
    });
    }
    else{
      $.ajax({
      url: "/api/v1.0/workflows/" + getWorkflowId() + "/states/" + stateId,
      type: "PATCH",
      processDate: false,
      data : JSON.stringify(paramData),
      contentType: 'application/json',
      success: function(result){
        if (result.code ===0) {
          $("#stateModal").modal("hide");
          swal({
            title: "更新成功!",
            text: "2s自动关闭",
            showConfirmButton: false,
            timer: 2000,
          })
          $('#state_table').dataTable()._fnAjaxUpdate();
        } else {
          swal({
            title: "更新失败:" + result.msg,
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

  function delState(stateId){
    swal({
      title: "是否真的要删除此状态记录?",
      text: "请确认此状态未被使用(包括历史工单)后再删除，否则包含此类工单的工单列表及工单详情都会有问题，慎重！！！",
      icon: "warning",
      buttons: true,
      dangerMode: true,
    })
    .then(function(willDelete){
      if (willDelete) {
        // 删除操作
        $.ajax({
        type: "DELETE",
        url: "/api/v1.0/workflows/" + getWorkflowId() + "/states/" + stateId,
        cache: false,  //禁用缓存
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        success: function (result) {
          if (result.code===0){
            // 刷新数据
            $('#state_table').dataTable()._fnAjaxUpdate();
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

  function showEditTransitionForm(data){
    $("#transitionName").val(data.name);
    $("#transitionTypeId").val(data.transition_type_id);
    $("#timer").val(data.timer);
    initStateItems(data.source_state_id, data.destination_state_id);
    $("#conditionExpression").val(data.condition_expression);
    $("#attributeTypeId").val(data.attribute_type_id);
    $("#alertText").val(data.alert_text);
    $("#transitionId").val(data.id);


    if (data.field_require_check) {
      $('#fieldRequireCheck').attr('checked', true);
    } else {
      $('#fieldRequireCheck').attr('checked', false);
    };
    if (data.alert_enable) {
      $('#alertEnable').attr('checked', true);
    } else {
      $('#alertEnable').attr('checked', false);
    };

    $('#transitionModal').modal('show');
  }
  function submitTransiton(){
    if (! $("#workflow_transiton_form").valid()) {
      return
    }
    var transitionId = $('#transitionId').val();
    var transitionName = $("#transitionName").val();
    var transitionTypeId = $("#transitionTypeId").val();
    var timer = $("#timer").val();
    var sourceStateId = $("#sourceStateId").val();
    var destinationStateId = $("#destinationStateId").val();
    var conditionExpression = $("#conditionExpression").val();
    var attributeTypeId = $("#attributeTypeId").val();
    var alertText = $("#alertText").val();

    var fieldRequireCheck = 0
    if ($("#fieldRequireCheck").prop('checked')){
      fieldRequireCheck = 1;
    };
    var alertEnable = 0
    if ($("#alertEnable").prop('checked')){
      alertEnable = 1;
    };

    if (!isJsonCheck(conditionExpression)){
      swal({
        title: "条件表达式内容不合法!",
        text: "条件表达式必须是数组对象的json格式。请按照提示输入合法的表达式",
        icon: "error",
        showConfirmButton: false,
        })
      return false;
    }

    var paramData = {
      name: transitionName,
      transition_type_id: Number(transitionTypeId),
      timer: Number(timer),
      source_state_id: Number(sourceStateId),
      destination_state_id: Number(destinationStateId),
      condition_expression: conditionExpression,
      attribute_type_id: Number(attributeTypeId),
      alert_text: alertText,
      field_require_check: Number(fieldRequireCheck),
      alert_enable: Number(alertEnable),
    }

    if(!transitionId){
      $.ajax({
      url: "/api/v1.0/workflows/" + getWorkflowId() + "/transitions",
      type: "POST",
      processDate: false,
      data : JSON.stringify(paramData),
      contentType: 'application/json',
      success: function(result){
        if (result.code===0) {
          $("#transitionModal").modal("hide");
          swal({
            title: "新增成功!",
            text: "2s自动关闭",
            showConfirmButton: false,
            timer: 2000,
          })
          $('#transition_table').dataTable()._fnAjaxUpdate();
        } else {
          swal({
            title: "新增失败:" + result.msg,
            text: "2s自动关闭",
            showConfirmButton: false,
            timer: 2000,
            icon: "error"
          })
        }

      }
    });
    }
    else{
      $.ajax({
      url: "/api/v1.0/workflows/" + getWorkflowId() + "/transitions/" + transitionId,
      type: "PATCH",
      processDate: false,
      data : JSON.stringify(paramData),
      contentType: 'application/json',
      success: function(result){
        if (result.code === 0) {
          $("#transitionModal").modal("hide");
          swal({
            title: "更新成功!",
            text: "2s自动关闭",
            showConfirmButton: false,
            timer: 2000,
          })
          $('#transition_table').dataTable()._fnAjaxUpdate();
        } else {
          swal({
            title: "更新失败:" + result.msg,
            text: "2s自动关闭",
            showConfirmButton: false,
            timer: 2000,
            error: result.msg
          })
        }

      }
    });

    }
  }

  function delTransition(transtionId){
    swal({
      title: "是否真的要删除此流转记录?",
      text: "",
      icon: "warning",
      buttons: true,
      dangerMode: true,
    })
    .then(function(willDelete) {
      if (willDelete) {
        // 删除操作
        $.ajax({
        type: "DELETE",
        url: "/api/v1.0/workflows/" + getWorkflowId() + "/transitions/" + transtionId,
        cache: false,  //禁用缓存
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        success: function (result) {
          if (result.code===0){
            // 刷新数据
            $('#transition_table').dataTable()._fnAjaxUpdate();
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
                title: "删除成功!",
                text: "2s自动关闭",
                icon: "error",
                showConfirmButton: false,
                timer:2000
              })
          }
          }
        });
      }
    });
  }

  function stateTypeChange() {
    console.log('state change ');
    if ($("#stateTypeId").val() !== '0'){
      // 不显示参与人类型及参与人
      $("#stateParticipantTypeId").val('0');
      $("#stateParticipant").val('');
      $("#stateParticipantTypeIdDiv").hide();
      $("#stateParticipantDiv").hide();  
    } else {
      $("#stateParticipantTypeIdDiv").show();
      $("#stateParticipantDiv").show(); 
    }
  }