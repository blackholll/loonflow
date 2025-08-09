import React from 'react';

import { ComponentTemplate } from '../../../../types/workflowDesign';

import {
    TextFields as TextFieldsIcon,
    CheckBox as CheckBoxIcon,
    RadioButtonChecked as RadioButtonIcon,
    ExpandMore as SelectIcon,
    Schedule as DateIcon,
    AttachFile as FileIcon,
    Pin as NumberIcon,
    DateRange as DateRangeIcon,
    Person as UserIcon,
    Groups as GroupsIcon,
    Link, EditNote, Schedule, CalendarMonth
} from '@mui/icons-material';


const basicComponentTemplates: ComponentTemplate[] = [
    {
        type: 'text',
        componentName: '单行文本',
        icon: <TextFieldsIcon />,
        defaultProps: {
            label: '文本输入',
            description: '',
            fieldKey: '',
            placeholder: '请输入文本',
            layout: { span: 6 }
        }
    },
    {
        type: 'textarea',
        componentName: '多行文本',
        icon: <TextFieldsIcon />,
        defaultProps: {
            label: '多行文本',
            description: '',
            fieldKey: '',
            placeholder: '请输入多行文本',
            layout: { span: 6 }
        }
    },
    {
        type: 'number',
        componentName: '数字',
        icon: <NumberIcon />,
        defaultProps: {
            label: '数字',
            description: '',
            fieldKey: '',
            placeholder: '请输入数字',
            layout: { span: 6 }
        }
    },
    {
        type: 'select',
        componentName: '下拉选择',
        icon: <SelectIcon />,
        defaultProps: {
            label: '下拉选择',
            description: '',
            fieldKey: '',
            extendedProps: {
                multiple: false,
                optionsWithKeys: [
                    { id: '1', label: '选项1', key: 'custom_field_option_abcde' },
                    { id: '2', label: '选项2', key: 'custom_field_option_fghij' },
                    { id: '3', label: '选项3', key: 'custom_field_option_klmno' }
                ]
            },
            layout: { span: 6 }
        }
    },
    {
        type: 'radio',
        componentName: '单选框',
        icon: <RadioButtonIcon />,
        defaultProps: {
            label: '单选框',
            description: '',
            fieldKey: '',
            extendedProps: {
                optionsWithKeys: [
                    { id: '1', label: '选项1', key: 'custom_field_option_pqrst' },
                    { id: '2', label: '选项2', key: 'custom_field_option_uvwxy' },
                    { id: '3', label: '选项3', key: 'custom_field_option_zabcd' }
                ]
            },
            layout: { span: 6 }
        }
    },
    {
        type: 'checkbox',
        componentName: '复选框',
        icon: <CheckBoxIcon />,
        defaultProps: {
            label: '复选框',
            description: '',
            fieldKey: '',
            extendedProps: {
                optionsWithKeys: [
                    { id: '1', label: '选项1', key: 'custom_field_option_efghi' },
                    { id: '2', label: '选项2', key: 'custom_field_option_jklmn' },
                    { id: '3', label: '选项3', key: 'custom_field_option_opqrs' }
                ]
            },
            layout: { span: 6 }
        }
    },
    {
        type: 'time',
        componentName: '时间选择',
        icon: <Schedule />,
        defaultProps: {
            label: '时间选择',
            description: '',
            fieldKey: '',
            layout: { span: 6 },
            extendedProps: {
                format: 'hh:mm:ss'
            }
        }
    },
    {
        type: 'date',
        componentName: '日期选择',
        icon: <CalendarMonth />,
        defaultProps: {
            label: '日期选择',
            description: '',
            fieldKey: '',
            layout: { span: 6 },
            extendedProps: {
                format: 'yyyy-mm-dd hh:mm:ss'
            }
        }
    },
    {
        type: 'file',
        componentName: '附件',
        icon: <FileIcon />,
        defaultProps: {
            label: '附件',
            description: '',
            fieldKey: '',
            layout: { span: 6 }
        }
    },
    {
        type: 'user',
        componentName: '用户',
        icon: <UserIcon />,
        defaultProps: {
            label: '用户',
            description: '',
            fieldKey: '',
            layout: { span: 6 }
        }
    },
    {
        type: 'department',
        componentName: '部门',
        icon: <GroupsIcon />,
        defaultProps: {
            label: '部门',
            description: '',
            fieldKey: '',
            layout: { span: 6 }
        }
    },
    {
        type: 'link',
        componentName: '链接',
        icon: <Link />,
        defaultProps: {
            label: '链接',
            description: '',
            fieldKey: '',
            layout: { span: 6 }
        }
    },
    {
        type: 'richText',
        componentName: '富文本',
        icon: <EditNote />,
        defaultProps: {
            label: '富文本',
            description: '',
            fieldKey: '',
            layout: { span: 6 }
        }
    },
    {
        type: 'externalData',
        componentName: '外部数据源',
        icon: <DateIcon />,
        defaultProps: {
            label: '外部数据源',
            description: '',
            fieldKey: '',
            layout: { span: 6 }
        }
    }
];


const InfoComponentTemplates: ComponentTemplate[] = [
    {
        type: 'customCreator',
        componentName: '创建人',
        icon: <SelectIcon />,
        defaultProps: {
            label: '创建人',
            description: '',
            fieldKey: '',
            layout: { span: 6 }
        }
    }, {
        type: 'customCreatedAt',
        componentName: '创建时间',
        icon: <SelectIcon />,
        defaultProps: {
            label: '创建时间',
            description: '',
            fieldKey: '',
            layout: { span: 6 }
        }
    }, {
        type: 'ticketStatus',
        componentName: '工单状态',
        icon: <SelectIcon />,
        defaultProps: {
            label: '工单状态',
            description: '',
            fieldKey: '',
            layout: { span: 6 }
        }
    }, {
        type: 'approvalStatus',
        componentName: '审批状态',
        icon: <SelectIcon />,
        defaultProps: {
            label: '审批状态',
            description: '',
            fieldKey: '',
            layout: { span: 6 }
        }
    }, {
        type: 'ticketType',
        componentName: '工单类型',
        icon: <SelectIcon />,
        defaultProps: {
            label: '工单类型',
            description: '',
            fieldKey: '',
            layout: { span: 6 }
        }
    }, {
        type: 'currentHandler',
        componentName: '当前处理人',
        icon: <SelectIcon />,
        defaultProps: {
            label: '当前处理人',
            description: '',
            fieldKey: '',
            layout: { span: 6 }
        }
    }
]

// 组件分类
const componentCategories = {
    basic: {
        title: '基础组件',
        components: basicComponentTemplates
    },

    info: {
        title: '信息组件',
        components: InfoComponentTemplates
    }
};

export default componentCategories;