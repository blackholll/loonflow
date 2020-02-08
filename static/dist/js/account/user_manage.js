
$("#UserModal").on("hidden.bs.modal", function() {
    document.getElementById("user_form").reset(); //此操作无法清空select2中的内容
    $("#userDeptId").val('').trigger('change')
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

function showEditUserForm(data){
  $("#userName").val(data.username);
  $("#userAlias").val(data.alias);
  $("#userEmail").val(data.email);
  $("#userPhone").val(data.phone);
  $("#userDeptId").val(data.dept_info.dept_id).trigger("change");
  $("#userId").val(data.id);

  if (data.is_admin) {
    $('#isAdmin').attr('checked', true);
  } else {
    $('#isAdmin').attr('checked', false);
  }
  if (data.is_workflow_admin) {
    $('#isWorkflowAdmin').attr('checked', true);
  } else {
    $('#isWorkflowAdmin').attr('checked', false);
  }
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
    var userDeptId = Number($("#userDeptId").val());
    var isActive = 0
    if ($("#isActive").prop('checked')){
      isActive = 1;
    };
    var isAdmin = 0
    if ($("#isAdmin").prop('checked')){
      isAdmin = 1;
    };
    var isWorkflowAdmin = 0
    if ($("#isWorkflowAdmin").prop('checked')){
      isWorkflowAdmin = 1;
    }
    paramData = {
      username : userName,
      alias : userAlias,
      phone: userPhone,
      email: userEmail,
      password: userPassword,
      dept_id: userDeptId,
      is_active: isActive,
      is_admin: isAdmin,
      is_workflow_admin: isWorkflowAdmin
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
    var userDeptId = Number($("#userDeptId").val());
    var userId = $('#userId').val();

    var isActive = 0
    if ($("#isActive").prop('checked')){
      isActive = 1;
    };
    var isAdmin = 0
    if ($("#isAdmin").prop('checked')){
      isAdmin = 1;
    };
    var isWorkflowAdmin = 0
    if ($("#isWorkflowAdmin").prop('checked')){
      isWorkflowAdmin = 1;
    }
    paramData = {
      username : userName,
      alias : userAlias,
      phone: userPhone,
      email: userEmail,
      dept_id: userDeptId,
      is_active: isActive,
      is_admin: isAdmin,
      is_workflow_admin: isWorkflowAdmin
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