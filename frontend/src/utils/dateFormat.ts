/**
 * 日期格式化工具函数
 * 解决Safari浏览器中日期解析问题
 */

/**
 * 安全地解析日期字符串，兼容Safari浏览器
 * @param dateString 日期字符串
 * @returns Date对象或null
 */
export function safeParseDate(dateString: string): Date | null {
    if (!dateString) return null;

    try {
        // 处理带时区的日期格式 (如: 2023-12-01 10:30:00 +0800)
        // Safari不支持这种格式，需要转换为ISO格式
        if (dateString.includes('+') || dateString.includes('-') && dateString.length > 19) {
            // 提取时区信息
            const timezoneMatch = dateString.match(/([+-]\d{4})$/);
            if (timezoneMatch) {
                const timezone = timezoneMatch[1];
                const datePart = dateString.replace(/\s*[+-]\d{4}$/, '');
                // 转换为ISO格式
                const isoString = `${datePart}.000${timezone}`;
                return new Date(isoString);
            }
        }

        // 处理标准格式的日期字符串
        return new Date(dateString);
    } catch (error) {
        console.warn('日期解析失败:', dateString, error);
        return null;
    }
}

/**
 * 格式化日期为本地化字符串
 * @param dateString 日期字符串
 * @param options 格式化选项
 * @returns 格式化后的日期字符串
 */
export function formatDate(
    dateString: string,
    options: Intl.DateTimeFormatOptions = {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false
    }
): string {
    const date = safeParseDate(dateString);
    if (!date) return 'Invalid Date';

    try {
        console.log('date', date);
        return date.toLocaleString('zh-CN', options);
    } catch (error) {
        console.warn('日期格式化失败:', dateString, error);
        return 'Invalid Date';
    }
}

/**
 * 格式化日期为简短格式 (YYYY-MM-DD HH:mm)
 * @param dateString 日期字符串
 * @returns 格式化后的日期字符串
 */
export function formatShortDate(dateString: string): string {
    return formatDate(dateString, {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        hour12: false
    });
}

/**
 * 格式化日期为日期格式 (YYYY-MM-DD)
 * @param dateString 日期字符串
 * @returns 格式化后的日期字符串
 */
export function formatDateOnly(dateString: string): string {
    return formatDate(dateString, {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    });
}
