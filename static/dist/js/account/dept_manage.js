document.write("<script language=javascript src='/static/dist/js/common/useSelect2.js'></script>")
$('#dept_table').DataTable({
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
      url: "/api/v1.0/accounts/depts",
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
      { "data": "parent_dept_info", render: function(data, type, full) {return data.parent_dept_name}},
      { "data": "leader_info", render: function(data, type, full) {
        if (data.leader_username) {
          return data.leader_alias + "(" + data.leader_username  +")"
          } else {
            return data.leader_alias
          }
        } 
      },
      { "data": "approver_info", render: function(data, type, full) { if(data.length){return (data.map(function(value,index,array){return value.approver_alias +"(" + value.approver_name +")"}).join(','))} else {return ''}  }},
      { "data": "label" },
      { "data": "creator_info", render: function(data, type, full) {if(data.creator_alias){return data.creator_alias}else{return full.creator}}},
      { "data": "gmt_created" },
      {render: function(data, type, full) {
        var rosJson=JSON.stringify(full).replace(/"/g, '&quot;');
        var editDeptButton = '<a onclick="showEditDeptModal(' + rosJson + ')'  + '"' +  '>编辑</a>';
        var delDeptButton = '<a onclick="delDept(' + full.id + ')' + '"' + '>删除</a>';
        return '<div>' + editDeptButton + '/' + delDeptButton + '</div>'
        }}

  ]

})

function submitDept() {
  if (! $("#dept_form").valid()) {
      return
    }
  var deptId = $("#deptId").val();
  var deptName = $("#deptName").val();
  var deptLabel = $("#deptLabel").val();
  var parent_dept_id = $("#parent_dept_id").val() - 0;
  if (! parent_dept_id) {
    parent_dept_id = 0
  }

  var deptLeader = $("#deptLeader").val();
  if (!deptLeader) {
    deptLeader='';
  }

  var deptApprover = $("#deptApprover").val();
  var paramData = {
    name: deptName,
    label: deptLabel,
    parent_dept_id: parent_dept_id,
    leader: deptLeader,
    approver: deptApprover.join(',')
  }
  if (deptId) {
    $.ajax({
      url: "/api/v1.0/accounts/depts/"+  deptId,
      type: "PATCH",
      processDate: false,
      data : JSON.stringify(paramData),
      contentType: 'application/json',
      success: function(result){
        $("#deptModal").modal("hide");
        if (result.code===0){
          swal({
          title: "新增成功!",
          text: "2s自动关闭",
          showConfirmButton: false,
          timer: 2000,
        })
        } else {
          swal({
          title: "新增失败:" + result.msg,
          text: "2s自动关闭",
          icon: 'error',
          showConfirmButton: false,
          timer: 2000,
        })
        }

        $('#dept_table').dataTable()._fnAjaxUpdate();
      }
    });
  } else {
    $.ajax({
      url: "/api/v1.0/accounts/depts",
      type: "POST",
      processDate: false,
      data : JSON.stringify(paramData),
      contentType: 'application/json',
      success: function(result){
        $("#deptModal").modal("hide");
        if (result.code===0){
          swal({
          title: "新增成功!",
          text: "2s自动关闭",
          showConfirmButton: false,
          timer: 2000,
        })
        } else {
          swal({
          title: "新增失败:" + result.msg,
          text: "2s自动关闭",
          icon: 'error',
          showConfirmButton: false,
          timer: 2000,
        })
        }

        $('#dept_table').dataTable()._fnAjaxUpdate();
      }
    });
  }
}

function makeParentDeptOption(data) {
  return "<option value=" + "'" + data.id + "'" + ">" + data.name + "</option>"
}

function makeUserOption(data) {
  var user = data.username + '(id:' + data.id + ',alias:' + data.alias + ')';
  return "<option value=" + "'" + data.id + "'" + ">" + user + "</option>"
}

function showEditDeptModal(data) {
  $('#deptId').val(data.id)
  $('#deptName').val(data.name)
  $('#deptLabel').val(data.label)
  initSelect2Items(
    "/api/v1.0/accounts/depts",
    "#parent_dept_id",
    makeParentDeptOption,
    data.parent_dept_id
  )
  initSelect2Items(
    "/api/v1.0/accounts/users",
    "#deptLeader",
    makeUserOption,
    data.leader_info.leader_id
  )
  var approvers = data.approver_info.map(function(item) {
    return item.approver_id;
  })
  initSelect2Items(
    "/api/v1.0/accounts/users",
    "#deptApprover",
    makeUserOption,
    approvers
  )
  $('#deptModal').modal('show');
}

function delDept(deptId) {
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
        url: "/api/v1.0/accounts/depts/" + deptId,
        cache: false,  //禁用缓存
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        success: function (result) {
          if (result.code===0){
            // 刷新数据
            $('#dept_table').dataTable()._fnAjaxUpdate();
            // 关闭modal
            if (result.code===0) {
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
          }
        });
      }
    }
  )
}

$('#parent_dept_id').select2({allowClear: true});
$('#deptLeader').select2({allowClear:true});
$('#deptApprover').select2({allowClear:true});

$("#deptModal").on("hidden.bs.modal", function() {
  document.getElementById("dept_form").reset();
  $("#parent_dept_id").val('').trigger('change')
  $("#deptLeader").val('').trigger('change')
  $("#deptApprover").val('').trigger('change')
});

$( document ).ready(function() {
  initSelect2Items(
    "/api/v1.0/accounts/depts",
    "#parent_dept_id",
    makeParentDeptOption
  )
  initSelect2Items(
    "/api/v1.0/accounts/users",
    "#deptLeader",
    makeUserOption
  )
  initSelect2Items(
    "/api/v1.0/accounts/users",
    "#deptApprover",
    makeUserOption
  )
});
