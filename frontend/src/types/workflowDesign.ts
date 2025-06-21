
export interface IFormField {
    id: string;
    type: string;
    label: string;
    width: 'full' | 'half';
    placeholder?: string;
    options?: string[];
    validation?: string;
    position: { x: number; y: number };
}

export interface ComponentTemplate {
    type: string;
    label: string;
    icon: React.ReactNode;
    defaultProps: Partial<IFormField>;
}

// 将 IFormField 重命名为 FormField 以保持兼容性
type FormField = IFormField;

// 定义布局类型
export interface LayoutConfig {
    type: 'vertical' | 'horizontal';
    gutter?: number;
    span?: number; // 组件在行中的跨度 (3=1/4, 4=1/3, 6=1/2, 12=全宽)
}

// 定义组件接口
export interface FormComponent {
    id: string;
    type: string;
    label?: string;
    placeholder?: string;
    options?: string[];
    layout: LayoutConfig;
    [key: string]: any;
}

// 定义行容器接口
export interface RowContainer {
    id: string;
    type: 'row';
    layout: LayoutConfig;
    components: FormComponent[];
    label?: string; // 添加可选的 label 属性
}

// 定义表单结构接口
export interface FormStructure {
    type: 'form';
    layout: LayoutConfig;
    components: (RowContainer | FormComponent)[];
}

export interface ComponentTemplate {
    type: string;
    label: string;
    icon: React.ReactNode;
    defaultProps: Partial<FormField>;
}

export interface FormDesignProps {
    fieldInfoList?: any[];
}