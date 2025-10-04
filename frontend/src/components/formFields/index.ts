import TextField from './TextField';
import NumberField from './NumberField';
import TextAreaField from './TextAreaField';
import SelectField from './SelectField';
// import DateTimeField from './DateTimeField';
// import UserField from './UserField';
// import DepartmentField from './DepartmentField';

// 导出所有字段组件
export { default as TextField } from './TextField';
export { default as NumberField } from './NumberField';
export { default as TextAreaField } from './TextAreaField';
export { default as SelectField } from './SelectField';
// export { default as DateTimeField } from './DateTimeField';
// export { default as UserField } from './UserField';
// export { default as DepartmentField } from './DepartmentField';

// 导出类型定义
export type { BaseFieldProps, FieldComponentConfig } from './types';

// 字段类型到组件的映射
export const fieldComponentMap = {
    text: TextField,
    textarea: TextAreaField,
    number: NumberField,
    select: SelectField,
    radio: SelectField,
    checkbox: SelectField,
    // date: DateTimeField,
    // time: DateTimeField,
    // datetime: DateTimeField,
    // user: UserField,
    // department: DepartmentField,
    // 可以继续添加更多字段类型
};

// 获取字段组件的函数
export const getFieldComponent = (fieldType: string) => {
    return fieldComponentMap[fieldType as keyof typeof fieldComponentMap] || TextField;
}; 