/**
 * @author 0031
 * bootstrap-table插件工具栏扩展，定时自动刷新表格数据
 * 需要引入abpetkov/switchery.js / istvan-ujjmeszaros/bootstrap-touchspin
 */
(function ($) {
    'use strict';
    // bootstrapTable模板输出变量
    var sprintf = $.fn.bootstrapTable.utils.sprintf;

    // 默认参数
    var defaults = {
        // 是否显示自动刷新按钮
        showAutoRefresh: false,
        // 自动刷新间隔
        autoRefreshInterval: 1
    };

    // 继承bootstrapTable.defaults/icons/locales参数
    $.extend($.fn.bootstrapTable.defaults, defaults);
    $.extend($.fn.bootstrapTable.defaults.icons, {
        autoRefresh: 'fa fa-refresh'
    });
    $.extend($.fn.bootstrapTable.locales, {
        formatAutoRefresh: function () {
            return '自动刷新';
        }
    });
    $.extend($.fn.bootstrapTable.defaults, $.fn.bootstrapTable.locales);

    // 获取构造器与toolbar
    var BootstrapTable = $.fn.bootstrapTable.Constructor,
        _initToolbar = BootstrapTable.prototype.initToolbar;

    // 扩展toolbar
    BootstrapTable.prototype.initToolbar = function () {

        _initToolbar.apply(this, Array.prototype.slice.apply(arguments));

        // 显示按钮
        if (this.options.showAutoRefresh) {
            // 找到dom元素
            var that = this,
                $btnGroup = this.$toolbar.find('>.btn-group'),
                $autoRefresh = $btnGroup.find('div.auto-refresh');

            // 如果该元素不存在，则新建
            if (!$autoRefresh.length) {
                // 判断下拉列表是否打开状态
                // 设置html内容box
                $autoRefresh = $([
                    '<div class="auto-refresh btn-group">',
                        '<button class="btn' +
                        sprintf(' btn-%s', this.options.buttonsClass) +
                        sprintf(' btn-%s', this.options.iconSize) +
                        ' dropdown-toggle"' +
                        'title="' + this.options.formatAutoRefresh() + '" data-toggle="dropdown">',
                    sprintf('<i class="%s %s"></i> ', this.options.iconsPrefix, this.options.icons.autoRefresh),
                    '<span class="caret"></span>',
                    '</button>',
                    '<ul class="dropdown-menu" role="menu" data-stop-propagation="true">',
                    '</ul>',
                    '</div>'].join('')).appendTo($btnGroup);

                var $menu = $autoRefresh.find('.dropdown-menu');

                // 判断是否开启自定义导出开关，如果为true，显示 touch-spin-box，否则隐藏
                var checked = '', display = 'style="display: none"';
                // 加入自定义导出开关
                $menu.append([
                    '<li>',
                    '<div class="switchery-box" title="开启此功能, 将自动定时刷新表格">',
                    '<span>自动刷新</span>&nbsp;&nbsp;',
                    '<input class="switchery auto-refresh-switch" type="checkbox"', checked, '>',
                    '</div>',
                    '</li>',
                    '<li class="time-box" ', display, '>',
                    '<div class="touch-spin-box">',
                    '<div class="form-group">',
                    '<span>刷新时间（秒）</span>',
                    '<input class="touch-spin refresh-interval" type="text">',
                    '</div>',
                    '</li>'
                ].join(''));


                // 判断Switchery是否存在
                if (typeof Switchery == 'function') {
                    // 初始化switchery开关
                    new Switchery(document.querySelector('.auto-refresh .switchery'), {size: 'small'});
                } else {
                    console.error('未引入abpetkov/switchery.js, 请检查代码.');
                }

                // 判断$.fn.TouchSpin是否存在
                if (typeof $.fn.TouchSpin == 'function') {
                    var $spin = $('input.refresh-interval');
                    // 扩展导出条数，如果值不存在，则取默认值
                    $spin.TouchSpin({
                        min: 1,        // 最小1秒
                        max: 60 * 60,  // 最大1小时
                        step: 1,       // 1秒递增
                        initval: that.options.autoRefreshInterval,
                        buttondown_class: "btn btn-info",
                        buttonup_class: "btn btn-info"
                    });

                    // 绑定touchspin相关事件
                    // 值发生改变
                    $spin.on('change', function () {
                        that.options.autoRefreshInterval = parseInt($(this).val());
                        // 先刷新一次数据
                        that.refresh();
                        // 开启定时器
                        startAutoRefreshInterval();
                    });
                    // 按下回车
                    $('.refresh-interval').on('keydown', function (e) {
                        if (e.keyCode == 13) {
                            // 让其失去焦点
                            $(this).blur();
                        }
                        // 阻止事件冒泡
                        e.stopImmediatePropagation();
                    });
                } else {
                    console.error('未引入istvan-ujjmeszaros/bootstrap-touchspin.js, 请检查代码.');
                }

                // 清除定时器函数
                var autoRefreshInterval, clearAutoRefreshInterval = function () {
                    if (autoRefreshInterval) {
                        clearInterval(autoRefreshInterval);
                    }
                };

                // 自动刷新函数
                var startAutoRefreshInterval = function () {
                    clearAutoRefreshInterval();
                    autoRefreshInterval = setInterval(function () {
                        that.refresh();
                    }, that.options.autoRefreshInterval * 1000);
                };

                // 下拉菜单自定义导出span点击
                $menu.find('.time-box > span').eq(0).on('click', function () {
                    $('.auto-refresh-switch').trigger('click');
                });

                // 下拉菜单自定义导出开关发生变化
                $menu.find('.auto-refresh-switch').on('change', function () {
                    var _this_ = $(this);
                    var checked = _this_.get(0).checked;
                    if (checked) {
                        _this_.parents('ul').find('.time-box').slideDown();
                        // 先刷新一次数据
                        that.refresh();
                        // 开启定时器
                        startAutoRefreshInterval();
                    } else {
                        _this_.parents('ul').find('.time-box').slideUp();
                        // 清除定时器
                        clearAutoRefreshInterval();
                    }
                });

                // 阻止下拉菜单关闭
                $('body').on('click','[data-stop-propagation]',function (e) {
                    e.stopImmediatePropagation();
                });
            }
        }
    };
})(jQuery);
