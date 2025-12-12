const ForkTsCheckerWebpackPlugin = require('fork-ts-checker-webpack-plugin');

module.exports = {
    webpack: {
        configure: (webpackConfig) => {
            // 找到并移除 ForkTsCheckerWebpackPlugin
            webpackConfig.plugins = webpackConfig.plugins.filter(
                plugin => !(plugin instanceof ForkTsCheckerWebpackPlugin)
            );

            // 可选：如果你想保留类型检查但提高内存限制，可以这样配置：
            // webpackConfig.plugins = webpackConfig.plugins.map(plugin => {
            //   if (plugin instanceof ForkTsCheckerWebpackPlugin) {
            //     return new ForkTsCheckerWebpackPlugin({
            //       ...plugin.options,
            //       typescript: {
            //         ...plugin.options.typescript,
            //         memoryLimit: 8192, // 8GB 内存限制
            //       },
            //     });
            //   }
            //   return plugin;
            // });

            return webpackConfig;
        },
    },
};
