document.write("<script language=javascript src='/static/dist/js/common/useSelect2.js'></script>")
$("#UserModal").on("hidden.bs.modal", function() {
    document.getElementById("user_form").reset(); //此操作无法清空select2中的内容
    $("#userDeptId").val('').trigger('change');
    $('#passwordGroup').show();
    $("#commonUser").attr("checked", true);
    $("#workflowAdmin").attr("checked", false);
    $("#superAdmin").attr("checked", false);
    $("#isActive").attr("checked", true);

  });

function showUserRole(user_id, username){
  $('#userRoleTitle').html('用户角色('+ username + ')');
  $('#user_role_table').DataTable({
  ordering: false,
  "serverSide":true,
  "bFilter":true,
  "lengthMenu": [10, 25, 50, 100 ],
  "language": {
    "searchPlaceholder": "输入角色名称模糊搜索"
  },

  ajax: function (data, callback, settings) {
    var param = {};
    param.per_page = data.length;//页面显示记录条数，在页面显示每页显示多少项的时候
    param.page = (data.start / data.length)+1;//当前页码
    param.search_value=data.search.value;
    $.ajax({
      type: "GET",
      url: "/api/v1.0/accounts/users/"+ user_id + "/roles",
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
      { "data": "name" }
  ]

})
  $('#userRoleModal').modal('show');

}

function submitUser() {
    var userId = $('#userId').val();
    if(!userId){
      addUser();
    }
    else{
      editUser();
    }
}

function makeDeptOption(data) {
  return "<option value=" + "'" + data.id + "'" + ">" + data.name + "</option>"
}

function showEditUserForm(data){
  console.log(data);
  $("#userName").val(data.username);
  $("#userAlias").val(data.alias);
  $("#userEmail").val(data.email);
  $("#userPhone").val(data.phone);
  var user_dept_info_list = data.user_dept_info_list;
  var user_dept_id_list = []
  user_dept_info_list.map(function (user_dept_info) {
    user_dept_id_list.push(String(user_dept_info.id));

  })
  initSelect2Items(
    "/api/v1.0/accounts/depts",
    "#userDeptId",
    makeDeptOption,
    user_dept_id_list
  );
  if(data.type_id===0){
    $("#commonUser").attr("checked", true);
    $("#workflowAdmin").attr("checked", false);
    $("#superAdmin").attr("checked", false);

  } else if(data.type_id===1){
    $("#commonUser").attr("checked", false);
    $("#workflowAdmin").attr("checked", true);
    $("#superAdmin").attr("checked", false);
  } else if(data.type_id===2){
    $("#commonUser").attr("checked", false);
    $("#workflowAdmin").attr("checked", false);
    $("#superAdmin").attr("checked", true);
  }
  if(data.is_active === true) {
    $("#isActive").attr("checked", true);
  } else {
    $("#isActive").attr("checked", false);
  }


  $("#userType").val(data.type_id);
  $("#userId").val(data.id);
  $('#passwordGroup').hide(); // 密码不允许直接编辑
  $('#UserModal').modal('show');
}

function addUser() {
    if (! $("#user_form").valid()) {
      return
    }
    var userName = $("#userName").val();
    var userAlias = $("#userAlias").val();
    var userPhone = $("#userPhone").val();
    var userEmail = $("#userEmail").val();
    var userPassword = $("#userPassword").val();
    var userDeptId = $("#userDeptId").val().join(',');
    var userTypeId = Number($("input[name='typeId']:checked").val());


    var isActive = 0
    if ($("#isActive").prop('checked')){
      isActive = 1;
    };

    paramData = {
      username : userName,
      alias : userAlias,
      phone: userPhone,
      email: userEmail,
      password: userPassword,
      dept_ids: userDeptId,
      is_active: isActive,
      type_id: userTypeId,
    }
    $.ajax({
      url: "/api/v1.0/accounts/users",
      type: "POST",
      processDate: false,
      data : JSON.stringify(paramData),
      contentType: 'application/json',
      success: function(result){
        if (result.code ===0) {
          $("#UserModal").modal("hide");
          swal({
            title: "新增成功!",
            text: "2s自动关闭",
            showConfirmButton: false,
            timer: 2000,
          })
          $('#user_table').dataTable()._fnAjaxUpdate();
        } else {
          swal({
            title: "新增失败:" + result.msg,
            text: "2s自动关闭",
            showConfirmButton: false,
            timer: 2000,
            icon: 'error'
          })
        }

      }
    });
}

function editUser() {
    if (! $("#user_form").valid()) {
      return
    }
    var userName = $("#userName").val();
    var userAlias = $("#userAlias").val();
    var userPhone = $("#userPhone").val();
    var userEmail = $("#userEmail").val();
    var userDeptId = $("#userDeptId").val().join(',');
    var userId = $('#userId').val();

    var isActive = 0
    if ($("#isActive").prop('checked')){
      isActive = 1;
    };

    var userDeptId = $("#userDeptId").val().join(',');
    var userTypeId = Number($("input[name='typeId']:checked").val());

    paramData = {
      username : userName,
      alias : userAlias,
      phone: userPhone,
      email: userEmail,
      dept_ids: userDeptId,
      is_active: isActive,
      type_id: userTypeId
    }
    $.ajax({
      url: "/api/v1.0/accounts/users/" + userId,
      type: "PATCH",
      processDate: false,
      data : JSON.stringify(paramData),
      contentType: 'application/json',
      success: function(result){
        if (result.code === 0) {
          $("#UserModal").modal("hide");
          swal({
            title: "更新成功!",
            text: "2s自动关闭",
            showConfirmButton: false,
            timer: 2000,
          })
          $('#user_table').dataTable()._fnAjaxUpdate();
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

function delUser(userId) {
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
        url: "/api/v1.0/accounts/users/" + userId,
        cache: false,  //禁用缓存
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        success: function (result) {
          if (result.code===0){
            // 刷新数据
            $('#role_table').dataTable()._fnAjaxUpdate();
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
    }
  )
}

function resetPassword(userId) {
    swal({
      title: "是否真的要重置该用户密码?",
      text: "仅管理员或者工作流管理员账户允许被重置密码",
      icon: "warning",
      buttons: true,
      dangerMode: true,
    })
    .then(function(willDelete){
      if (willDelete) {
        // 删除操作
        $.ajax({
        type: "POST",
        url: "/api/v1.0/accounts/users/" + userId + "/reset_password",
        cache: false,  //禁用缓存
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        success: function (result) {
          if (result.code===0){
            // 刷新数据
            $('#user_table').dataTable()._fnAjaxUpdate();
            // 关闭modal
            swal({
              title: "重置密码成功,密码已被重置为123456!",
              text: "2s自动关闭",
              icon: "success",
              showConfirmButton: false,
              timer:2000
            })
            } else {
            swal({title:"删除失败:" + result.msg,
            text: "2s自动关闭",
            icon: "error",
            showConfirmButton: false,
            timer:2000})
          }
          }
        });
      }
    }
  )
}

function adminChange() {
    var isAdmin = 0;
    if ($("#isAdmin").prop('checked')){
      isAdmin = 1;
    };
    var isWorkflowAdmin = 0
    if ($("#isWorkflowAdmin").prop('checked')){
      isWorkflowAdmin = 1;
    }
    if (isAdmin || isWorkflowAdmin) {
      // admin allow set password
      $("#userPassword").attr("disabled", false);
    } else {
      $("#userPassword").attr("disabled", true);
    }
}

$("#user_form").validate();

$('#userDeptId').select2({allowClear: true});

$("#userRoleModal").on("hidden.bs.modal", function() {
  $(this).removeData("bs.modal");
  // $('#user_role_table').dataTable().Rows.Clear()
  $('#user_role_table').dataTable().fnClearTable();
  $('#user_role_table').dataTable().fnDestroy();
  });

$('#user_table').DataTable({
ordering: false,
"serverSide":true,
"bFilter":true,
"lengthMenu": [10, 25, 50, 100 ],
"language": {
  "searchPlaceholder": "用户名或姓名模糊搜索"
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
    url: "/api/v1.0/accounts/users",
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
    { "data": "username" },
    { "data": "alias" },
    { "data": "email" },
    { "data": "phone" },
    { "data": "user_dept_info_list", render:function (data, type, full) {
      var dept_name_info_list= [];
      $.map(data, function(user_dept){
        dept_name_info_list.push(user_dept.name);

      });
      if (dept_name_info_list.length !== 0){
        return dept_name_info_list.join(',');
      } else {
        return '';
      }

       }},
    { "data": "is_active", render:function (data, type, full) {if(data){return "正常"} else{return "未激活"}}},
    { "data": "type_id", render:function (data, type, full) {if(data==0){return "普通用户"} else if(data==1){return "工作流管理员"} else if(data==2){return "超级管理员"}}},
    { "data": "creator_info", render:function (data, type, full) {if(data.creator_alias){return data.creator_alias}else{return data.creator_username}}},
    // { "data": "creator_info", render:function (data, type, full) {return data.creator_username}},
    // { "data": "creator_info"},
    { "data": "gmt_created" },
    {render: function(data, type, full){
      var rosJson=JSON.stringify(full).replace(/"/g, '&quot;');
      return ('<div><a onclick="showEditUserForm('+ rosJson + ')' + '"' + '>编辑</a>' + '/' + '<a onclick="resetPassword(' + full.id + ')' +'"'+'>重置密码</a>'+ '/' +'<a  onclick="showUserRole(' + full.id + ',' + "'" + full.username + "'" + ')' + '"' + '>查看角色</a>' + '/' + '<a onclick="delUser(' + full.id + ')' + '"'+ '>删除</a>' + ' </div>')
    }}
]
})

$( document ).ready(function() {
  initSelect2Items(
    "/api/v1.0/accounts/depts",
    "#userDeptId",
    makeDeptOption
  )
});
