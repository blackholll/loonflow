#!/usr/bin/env node

// 快速TypeScript编译脚本
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('🚀 开始快速TypeScript编译...');

// 清理缓存
try {
    if (fs.existsSync('tsconfig.tsbuildinfo')) {
        fs.unlinkSync('tsconfig.tsbuildinfo');
        console.log('✅ 清理了编译缓存');
    }
} catch (error) {
    console.log('⚠️ 清理缓存失败:', error.message);
}

// 设置环境变量优化
process.env.NODE_OPTIONS = '--max-old-space-size=8192';

try {
    console.log('📦 开始编译...');
    const startTime = Date.now();

    // 使用优化的编译参数
    execSync('npx tsc --incremental --skipLibCheck --noEmit', {
        stdio: 'inherit',
        cwd: process.cwd()
    });

    const endTime = Date.now();
    const duration = (endTime - startTime) / 1000;

    console.log(`✅ 编译完成！耗时: ${duration.toFixed(2)}秒`);

} catch (error) {
    console.error('❌ 编译失败:', error.message);
    process.exit(1);
}
