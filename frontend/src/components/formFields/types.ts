import { IFormField } from '../../types/workflowDesign';

// 基础字段组件属性接口
export interface BaseFieldProps {
    field: IFormField;
    value?: any;
    onChange?: (value: any) => void;
    disabled?: boolean;
    readOnly?: boolean;
    required?: boolean;
    error?: boolean;
    helperText?: string;
    size?: 'small' | 'medium' | 'large';
    variant?: 'outlined' | 'filled' | 'standard';
    fullWidth?: boolean;
}


// 字段组件配置
export interface FieldComponentConfig {
    // mode: FieldRenderMode;
    showLabel?: boolean;
    showDescription?: boolean;
    showValidation?: boolean;
} 