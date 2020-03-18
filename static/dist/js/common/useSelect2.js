function initSelect2Items(url, dom, makeOption, selectedId) {
  let param = {};
  param.per_page = 1000;
  param.page = 1
  $.ajax({
    type: "GET",
    url: url,
    cache: false,  //禁用缓存
    data: param,  //传入组装的参数
    dataType: "json",
    success: function (result) {
      $(dom).empty();
      result.data.value.map(function (currentValue, index, arr) {
        console.log('currentValue')
        console.log(currentValue)
        $(dom).append(
          makeOption(currentValue)
        );
      })
      $(dom).val(selectedId).trigger("change");
    },
  });
}
