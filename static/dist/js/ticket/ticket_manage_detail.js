

$( document ).ready(function() {
    // 获取操作记录
    $.ajax({
        type: "GET",
        url: "/api/v1.0/tickets/" + getTicketId() +"/flowlogs",
        cache: false,  //禁用缓存
        data: {per_page: 10000},  //传入组装的参数
        dataType: "json",
        success: function (result) {
          console.log(result);
          if (result.code===0){
            var flowLogHtml = "";
            var flowLogHtmlArray = [];
            result.data.value.map(function(res){
                // 时间:2020-02-03 10:00:00 处理人:张三 当前状态:发起人编辑中 操作:同意 处理意见/结果:处理完成
                flowLogHtmlArray.push("<li>" + "时间: " + res.gmt_created + " 处理人: " + res.participant_info.participant_alias
                  + " 当前状态: " + res.state.state_name + " 操作: " + res.transition.transition_name + " 处理意见: " + res.suggestion + "</li>")
            })
            flowLogHtml = flowLogHtmlArray.join('');
            $("#flowLog").html(flowLogHtml);
            }
          }


          });
  });

$(document).ready(function(){
    //获取操作flowstep记录
  $.ajax({
        type: "GET",
        url: "/api/v1.0/tickets/" + getTicketId() +"/flowsteps",
        cache: false,  //禁用缓存
        data: {per_page: 10000},  //传入组装的参数
        dataType: "json",
        success: function (result) {
          console.log(result);
          if (result.code===0){
              var stepList = [];
              var activeId = 0;
              var nowId = 0;
              var activeStateId = result.data.current_state_id;
              result.data.value.map(function(res){
                  if (res.state_id === activeStateId){
                      activeId = nowId;
                  }
                  nowId = nowId + 1;
                  if (res.state_flow_log_list[0]) {
                      // 多条处理记录时候
                      var state_flow_log_0 = res.state_flow_log_list[0]
                      var description = state_flow_log_0.participant_info.participant_alias + ' '
                        + state_flow_log_0.transition.transition_name + ' @' + state_flow_log_0.gmt_created
                      var customHtml='';
                      var actionList = [];
                      if (res.state_flow_log_list.length>1){
                          //当前状态存在多条处理记录
                        res.state_flow_log_list.map(function(res1){
                            actionList.push('<li>' +res1.participant_info.participant_alias + ' '
                        + res1.transition.transition_name + ' @' + res1.gmt_created + '</li>')
                        })
                        var customHtml = '<button style="order: 3;" onclick="showAllAction(' + "'" + actionList.join('') + "'" +  ')"' + '>全部操作</button>';
                      }
                      step0 = {title: res.state_name, description:description, customHtml:customHtml}
                  } else {
                      step0 ={title: res.state_name, description:''}
                  }
                  stepList.push(step0);
              })
                steps({
                    el: "#ticketStep",
                    data: stepList,
                    sides: "two-sides",
                    active: activeId
                });



            }
          }


          });
})

$(document).ready(function() {
  // 工单详情
  $.ajax({
    type: "GET",
    url: "/api/v1.0/tickets/" + getTicketId(),
    cache: false,  //禁用缓存
    dataType: "json",
    success: function (result) {
      if (result.code === 0) {
        var detailHtml = "";
        var fieldList = result.data.value.field_list;
        fieldList.map(function (field) {
          if (field.field_type_id === 55) {
              //文本域
            var newfield = '<label for="starttime" class="col-sm-2 control-label">' + field.field_name
              + '</label><div class="col-md-4">' + field.field_value +  '</div>';
            detailHtml = detailHtml + newfield;

          }

          else if ([5, 10, 15, 20, 25, 30, 60, 70, 80].indexOf(field.field_type_id) > -1) {
            var newfield = '<label for="starttime" class="col-sm-2 control-label">' + field.field_name
              + '</label><div class="col-md-4"> <input class="form-control" type="text" readonly="readonly" value='
              + field.field_value + '></div>';
            detailHtml = detailHtml + newfield;
        }
        })
        $("#ticketDetailForm").html(detailHtml);

      }
      else {
        swal({
          title: "获取工单详情失败:" + result.msg,
          text: "2s自动关闭",
          icon: "error",
          showConfirmButton: false,
          timer:2000
        })
      }

    }
  })
})

$(document).ready(function() {
  // 获取工单对应工作流的所有状态
  $.ajax({
    type: "GET",
    url: "/api/v1.0/tickets/" + getTicketId(),
    cache: false,  //禁用缓存
    dataType: "json",
    success: function (result) {
      if (result.code === 0) {
        var workflowId = result.data.value.workflow_id;
        $.ajax({
          type: "GET",
          url: "/api/v1.0/workflows/" + workflowId + "/states",
          cache: false,  //禁用缓存
          dataType: "json",
          success: function (result) {
            if (result.code === 0) {
              // 填充状态选择下拉框
              result.data.value.map(function(currentValue,index,arr){$("#targetState").append("<option value=" + "'" + currentValue.id + "'" + ">" + currentValue.name + "</option>");})
              }
            }
      
          })
        }}
      }
  )
    })

    
  


function getTicketId() {
    var urlPath = window.location.pathname;
    var ticketId = Number(urlPath.split('/')[3]);
    return ticketId
}

function showAllAction(actionList) {
    $("#ticketAllAction").html(actionList);
    $('#ticketAllActionModal').modal('show');
}

function showDeliverModal(){
  $('#ticketDeliverModal').modal('show');
}

function showCloseModal(){
  $('#ticketCloseModal').modal('show');
}

function showStateModal(){
  $('#ticketStateModal').modal('show');
}

$('#deliverTarget').select2({
  placeholderOption: "first",
  allowClear:true,
  language: {
    searching: function() {
        return "输入用户名称搜索...";
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
      return {
        id: item.username,
        text: item.username + "(id:" + item.id + "," + "alias:" + item.alias + ")"
      };

    })
  };

},
  },

cache: true
});

function submitDeliverTicket(){
  //提交转交
  var ticketId = getTicketId();
  var targetUser =  $("#deliverTarget").val();
  var suggestion = $("#deliverSuggestion").val();
  var params = {
    target_username:targetUser,
    suggestion:suggestion,
    from_admin:1  // 管理员强制转交
  };
  $.ajax({
    url: "/api/v1.0/tickets/" + ticketId + '/deliver',
    type: "POST",
    processDate: false,
    data : JSON.stringify(params),
    contentType: 'application/json',
    success: function(result){
      if (result.code===0) {
        swal({
          title: "转交成功!",
          text: "2s自动关闭",
          showConfirmButton: false,
          timer: 2000,
        })
        $("#ticketDeliverModal").modal("hide");
        window.location.reload();   
      } else {
        swal({
          title: "转交失败:" + result.msg,
          text: "2s自动关闭",
          showConfirmButton: false,
          timer: 2000,
          icon: 'error',
        })
      }
    }
  });
}

function submitStateTicket(){
  //修改工单状态
  var ticketId = getTicketId();
  var targetState =  Number($("#targetState").val());
  var suggestion = $("#stateSuggestion").val();
  var params = {state_id:targetState, suggestion:suggestion};
  $.ajax({
    url: "/api/v1.0/tickets/" + ticketId + '/state',
    type: "PUT",
    processDate: false,
    data : JSON.stringify(params),
    contentType: 'application/json',
    success: function(result){
      if (result.code===0) {
        swal({
          title: "强制修改状态成功!",
          text: "2s自动关闭",
          showConfirmButton: false,
          timer: 2000,
        })
        $("#ticketStateModal").modal("hide");
        window.location.reload();   
      } else {
        swal({
          title: "强制修改状态失败:" + result.msg,
          text: "2s自动关闭",
          showConfirmButton: false,
          timer: 2000,
          icon: 'error',
        })
      }
    }
  });
}


function submitCloseTicket(){
  //关闭工单
  var ticketId = getTicketId();
  var suggestion = $("#closeSuggestion").val();
  var params = {suggestion:suggestion};
  $.ajax({
    url: "/api/v1.0/tickets/" + ticketId + '/close',
    type: "POST",
    processDate: false,
    data : JSON.stringify(params),
    contentType: 'application/json',
    success: function(result){
      if (result.code===0) {
        swal({
          title: "关闭成功!",
          text: "2s自动关闭",
          showConfirmButton: false,
          timer: 2000,
        })
        $("#ticketCloseModal").modal("hide");
        window.location.reload();
        //刷新当前页面   
      } else {
        swal({
          title: "关闭失败:" + result.msg,
          text: "2s自动关闭",
          showConfirmButton: false,
          timer: 2000,
          icon: 'error',
        })
      }
    }
  });
}


