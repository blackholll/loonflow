import TextField from './TextField';
import NumberField from './NumberField';
import TextAreaField from './TextAreaField';
import SelectField from './SelectField';
import RadioField from './RadioField';
import CheckboxField from './CheckboxField';
import TimeField from './TimeField';
import DateField from './DateField';
import DateTimeField from './DateTimeField';
import FileField from './FileField';
import UserField from './UserField';
import DepartmentField from './DepartmentField';

// 导出所有字段组件
export { default as TextField } from './TextField';
export { default as NumberField } from './NumberField';
export { default as TextAreaField } from './TextAreaField';
export { default as SelectField } from './SelectField';
export { default as RadioField } from './RadioField';
export { default as CheckboxField } from './CheckboxField';
export { default as TimeField } from './TimeField';
export { default as DateField } from './DateField';
export { default as DateTimeField } from './DateTimeField';
export { default as FileField } from './FileField';
export { default as UserField } from './UserField';
export { default as DepartmentField } from './DepartmentField';

// 导出类型定义
export type { BaseFieldProps, FieldComponentConfig } from './types';

// 字段类型到组件的映射
export const fieldComponentMap = {
    text: TextField,
    textarea: TextAreaField,
    number: NumberField,
    select: SelectField,
    radio: RadioField,
    checkbox: CheckboxField,
    time: TimeField,
    date: DateField,
    datetime: DateTimeField,
    file: FileField,
    user: UserField,
    department: DepartmentField,
    // 可以继续添加更多字段类型
};

// 获取字段组件的函数
export const getFieldComponent = (fieldType: string) => {
    return fieldComponentMap[fieldType as keyof typeof fieldComponentMap] || TextField;
}; 