function showRoleUsers(role_id, name){
  $('#addRoleUserRoleId').val(role_id);
  $('#roleUserTitle').html('角色用户('+ name + ')');
  $('#role_user_table').DataTable({
  ordering: false,
  "serverSide":true,
  "bFilter":true,
  "lengthMenu": [10, 25, 50, 100 ],
  "language": {
    "searchPlaceholder": "用户名或姓名模糊搜索"
  },

  ajax: function (data, callback, settings) {
    var param = {};
    param.per_page = data.length;//页面显示记录条数，在页面显示每页显示多少项的时候
    param.page = (data.start / data.length)+1;//当前页码
    param.search_value=data.search.value;
    $.ajax({
      type: "GET",
      url: "/api/v1.0/accounts/roles/"+ role_id + "/users",
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
    {
      render: function (data, type, full) {
        var delRoleButton = '<a onclick="delRoleUser(' + role_id + ',' + full.id + ')' + '">删除</a>'
        return ('<div>' + delRoleButton + '</div>')
      }
    }

  ]

})
  $('#roleUserModal').modal('show');

}

function submitRole() {
  // if (! $("#role_form").valid()) {
  //     return
  //   }

  var roleId = $('#roleId').val()
  var roleName = $("#roleName").val();
  var roleDescription = $("#roleDescription").val();
  var roleLabel = $("#roleLabel").val();
  var paramData = {
      name : roleName,
      description : roleDescription,
      label: roleLabel
  };
  if (roleId) {
    // edit role
    $.ajax({
      url: "/api/v1.0/accounts/roles" + '/' + roleId,
      type: "PATCH",
      processDate: false,
      data : JSON.stringify(paramData),
      contentType: 'application/json',
      success: function(result){
        $("#RoleModal").modal("hide");
        if(result.code===0){
          swal({
          title: "修改成功!",
          text: "2s自动关闭",
          showConfirmButton: false,
          timer: 2000,
          })
        } else {
          swal({
            title: "修改失败:" + data.msg,
            icon: "error",
            text: "2s自动关闭",
            showConfirmButton: false,
            timer: 2000,
        })
        }

        $('#role_table').dataTable()._fnAjaxUpdate();
      }
    });

  } else {
    // add role
    $.ajax({
      url: "/api/v1.0/accounts/roles",
      type: "POST",
      processDate: false,
      data : JSON.stringify(paramData),
      contentType: 'application/json',
      success: function(result){
        $("#RoleModal").modal("hide");
        if (result.code===0){
          swal({
          title: "新增成功!",
          text: "2s自动关闭",
          showConfirmButton: false,
          timer: 2000,
        })
        } else {
          swal({
          title: "新增成功:" + result.msg,
          text: "2s自动关闭",
          icon: "error",
          showConfirmButton: false,
          timer: 2000,
        })
        }

        $('#role_table').dataTable()._fnAjaxUpdate();
      }
    });
  }
}

function delRoleUser(roleId, userId) {
    swal({
        title: "是否真的要删除该用户?",
        text: "是否真的要删除该用户！！！",
        icon: "warning",
        buttons: true,
        dangerMode: true,
    })
        .then(function (willDelete) {
            if (willDelete) {
                // 删除操作
                $.ajax({
                    type: "DELETE",
                    url: "/api/v1.0/accounts/roles/" + roleId + "/users/" + userId,
                    cache: false,  //禁用缓存
                    dataType: "json",
                    contentType: "application/json; charset=utf-8",
                    success: function (result) {
                        if (result.code === 0) {
                            // 刷新数据
                            $('#role_user_table').dataTable()._fnAjaxUpdate();
                            if (result.code === 0) {
                                swal({
                                    title: "删除成功!",
                                    text: "2s自动关闭",
                                    icon: "success",
                                    showConfirmButton: false,
                                    timer: 2000
                                })
                            } else {
                                swal({
                                    title: "删除失败:" + result.msg,
                                    text: "2s自动关闭",
                                    icon: "error",
                                    showConfirmButton: false,
                                    timer: 2000
                                })
                            }
                        }
                    }
                });
            }
        }
        )
}


function delRole(roleId) {
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
        url: "/api/v1.0/accounts/roles/" + roleId,
        cache: false,  //禁用缓存
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        success: function (result) {
          if (result.code===0){
            // 刷新数据
            $('#role_table').dataTable()._fnAjaxUpdate();
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

function showEditRoleModel(data){
    $("#roleName").val(data.name);
    $("#roleDescription").val(data.description);
    $("#roleLabel").val(data.label);
    $("#roleId").val(data.id);
    $('#RoleModal').modal('show');
  }

function submitRoleUser() {
  var roleUserId = $('#roleUserId').val()
  var addRoleUserRoleId = $('#addRoleUserRoleId').val()
  var paramData = {'user_id': Number(roleUserId)};
  $.ajax({
      url: "/api/v1.0/accounts/roles/"+ addRoleUserRoleId + '/users',
      type: "POST",
      processDate: false,
      data : JSON.stringify(paramData),
      contentType: 'application/json',
      success: function(result){
        $("#AddRoleUserModal").modal("hide");
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

        $('#role_user_table').dataTable()._fnAjaxUpdate();
      }
    });

}

$("#RoleModal").on("hidden.bs.modal", function() {
  document.getElementById("role_form").reset();
});