export interface ILayout {
    span: number;
    orderId?: number; //行容器之间 或者行容器内组件的顺序
}

export interface IExtendedProps {
    optionsWithKeys?: FormOption[];
    multiple?: boolean;
    format?: string;
    timeFormat?: string;
    dateFormat?: string;
    timeZone?: string;
    timeZoneName?: string;
}

export interface IFormField {
    id: string;
    type: string;
    label: string;
    description?: string;
    fieldKey?: string;
    value?: any;
    placeholder?: string;
    layout: ILayout;
    extendedProps?: IExtendedProps;
}


export interface ComponentTemplate {
    type: 'text' | 'textarea' | 'number' | 'select' | 'radio' | 'checkbox' | 'time' | 'date' | 'user' | 'department' | 'file' | 'link' | 'richText' | 'externalData' | 'customCreator' | 'customCreatedAt' | 'ticketStatus' | 'approvalStatus' | 'ticketType' | 'currentHandler' | 'title' | 'ticketNodes';
    componentName: string;
    icon: React.ReactNode;
    defaultProps: Partial<IFormField>;
}

// 定义布局类型
// export interface LayoutConfig {
//     type: 'vertical' | 'horizontal';
//     gutter?: number;
//     span?: number; // 组件在行中的跨度 (3=1/4, 4=1/3, 6=1/2, 12=全宽)
// }

// 定义选项接口
export interface FormOption {
    id: string;
    label: string;
    key: string;
}

// // 定义组件接口
// export interface FormComponent {
//     id: string;
//     type: string;
//     label?: string;
//     description?: string;
//     fieldKey?: string;
//     placeholder?: string;
//     multiple?: boolean;
//     optionsWithKeys?: FormOption[];
//     value?: any;
//     layout: LayoutConfig;
//     [key: string]: any;
// }

// 定义行容器接口
export interface RowContainer {
    id: string;
    type: 'row';
    layout: ILayout;
    components: IFormField[];
}

// 定义表单结构接口
export interface FormStructure {
    type: 'form';
    layout: ILayout;
    components: (RowContainer | IFormField)[];
}

export interface FormDesignProps {
    fieldInfoList?: any[];
}

// React Flow 节点数据类型定义
export interface WorkflowNodeData {
    label: string;
    nodeType: string;
    properties?: {
        name: string;
        description: string;
        assignee: string;
        timeout: number;
        [key: string]: any;
    };
}

// React Flow 边数据类型定义
export interface WorkflowEdgeData {
    label?: string;
    properties?: {
        condition?: string;
        [key: string]: any;
    };
}