# FileField 组件使用说明

## 概述
FileField 是一个支持文件上传和显示的表单字段组件，适用于工作流表单中的附件字段。

## 功能特性
- ✅ 支持多文件上传
- ✅ 文件大小限制
- ✅ 文件数量限制
- ✅ 文件类型限制
- ✅ 文件预览和下载
- ✅ 文件删除功能
- ✅ 拖拽上传支持
- ✅ 编辑和查看模式
- ✅ 国际化支持

## 基本用法

```tsx
import { FileField } from './components/formFields';

// 基本使用
<FileField
    value=""
    fieldRequired={false}
    onChange={(files) => console.log(files)}
    mode="edit"
    props={{}}
/>
```

## 属性说明

### FileFieldProps

| 属性 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| value | `string \| FileInfo[]` | 否 | `''` | 文件值，可以是 JSON 字符串或文件信息数组 |
| fieldRequired | `boolean` | 否 | `false` | 是否为必填字段 |
| onChange | `(value: string \| FileInfo[]) => void` | 否 | - | 值变化回调函数 |
| mode | `'view' \| 'edit'` | 否 | `'edit'` | 显示模式 |
| props | `any` | 否 | `{}` | 扩展属性 |

### props 扩展属性

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| maxFiles | `number` | `10` | 最大文件数量 |
| maxSize | `number` | `10 * 1024 * 1024` | 单个文件最大大小（字节） |
| accept | `string` | `'*'` | 接受的文件类型 |

## 使用示例

### 1. 基本文件上传
```tsx
<FileField
    value=""
    fieldRequired={true}
    onChange={(files) => {
        // 处理文件变化
        console.log('Selected files:', files);
    }}
    mode="edit"
    props={{
        maxFiles: 5,
        maxSize: 5 * 1024 * 1024, // 5MB
        accept: '.pdf,.doc,.docx,.jpg,.png'
    }}
/>
```

### 2. 查看模式
```tsx
<FileField
    value={JSON.stringify([
        { id: '1', name: 'document.pdf', size: 1024000, type: 'application/pdf', url: '/files/document.pdf' }
    ])}
    mode="view"
    props={{}}
/>
```

### 3. 限制文件类型
```tsx
<FileField
    value=""
    onChange={(files) => handleFileChange(files)}
    mode="edit"
    props={{
        accept: 'image/*', // 只接受图片文件
        maxFiles: 3,
        maxSize: 2 * 1024 * 1024 // 2MB
    }}
/>
```

## 数据结构

### FileInfo 接口
```typescript
interface FileInfo {
    id: string;        // 文件唯一标识
    name: string;      // 文件名
    size: number;      // 文件大小（字节）
    type: string;      // 文件类型
    url?: string;      // 文件下载链接（可选）
    file?: File;       // 原始文件对象（可选）
}
```

## 国际化支持

组件支持中英文国际化，相关文本定义在：
- `zh-CN.json`: `common.fileUpload.*`
- `en-US.json`: `common.fileUpload.*`

## 注意事项

1. **文件大小限制**: 默认单个文件最大 10MB，可通过 `props.maxSize` 调整
2. **文件数量限制**: 默认最多 10 个文件，可通过 `props.maxFiles` 调整
3. **文件类型限制**: 可通过 `props.accept` 设置接受的文件类型
4. **数据格式**: 组件内部会将文件信息转换为 JSON 字符串存储
5. **下载功能**: 需要提供 `url` 字段才能支持文件下载

## 样式定制

组件使用 Material-UI 组件库，可以通过主题系统进行样式定制：

```tsx
// 自定义上传区域样式
const theme = createTheme({
  components: {
    MuiBox: {
      styleOverrides: {
        root: {
          '& .upload-area': {
            borderColor: '#1976d2',
            '&:hover': {
              backgroundColor: '#f3f3f3'
            }
          }
        }
      }
    }
  }
});
```
