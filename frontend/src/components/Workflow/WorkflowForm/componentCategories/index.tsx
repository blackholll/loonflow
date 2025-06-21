import React, { useState, useRef } from 'react';
import {
    Box,
    Paper,
    Typography,
    Card,
    CardContent,
    TextField,
    Select,
    MenuItem,
    FormControl,
    InputLabel,
    Button,
    Divider,
    IconButton,
    Tooltip,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions
} from '@mui/material';
import Grid from '@mui/material/Grid2';
import { ComponentTemplate, IFormField } from '../../../../types/workflowDesign';

import {
    TextFields as TextFieldsIcon,
    CheckBox as CheckBoxIcon,
    RadioButtonChecked as RadioButtonIcon,
    ExpandMore as SelectIcon,
    Schedule as DateIcon,
    AttachFile as FileIcon,
    Delete as DeleteIcon,
    Settings as SettingsIcon,
    DragIndicator as DragIcon,
    Pin as NumberIcon,
    DateRange as DateRangeIcon,
    Person as UserIcon,
    Groups as GroupsIcon,
    Link, EditNote
} from '@mui/icons-material';


const basicComponentTemplates: ComponentTemplate[] = [
    {
        type: 'text',
        label: '单行文本',
        icon: <TextFieldsIcon />,
        defaultProps: {
            label: '文本输入',
            description: '',
            fieldKey: '',
            placeholder: '请输入文本',
            width: 'half'
        }
    },
    {
        type: 'textarea',
        label: '多行文本',
        icon: <TextFieldsIcon />,
        defaultProps: {
            label: '多行文本',
            description: '',
            fieldKey: '',
            placeholder: '请输入多行文本',
            width: 'half'
        }
    },
    {
        type: 'number',
        label: '数字',
        icon: <NumberIcon />,
        defaultProps: {
            label: '数字',
            description: '',
            fieldKey: '',
            placeholder: '请输入数字',
            width: 'half'
        }
    },
    {
        type: 'select',
        label: '下拉选择',
        icon: <SelectIcon />,
        defaultProps: {
            label: '下拉选择',
            description: '',
            fieldKey: '',
            options: ['选项1', '选项2', '选项3'],
            optionsWithKeys: [
                { id: '1', label: '选项1', key: 'custom_field_option_abcde' },
                { id: '2', label: '选项2', key: 'custom_field_option_fghij' },
                { id: '3', label: '选项3', key: 'custom_field_option_klmno' }
            ],
            width: 'half'
        }
    },
    {
        type: 'radio',
        label: '单选框',
        icon: <RadioButtonIcon />,
        defaultProps: {
            label: '单选框',
            description: '',
            fieldKey: '',
            options: ['选项1', '选项2', '选项3'],
            optionsWithKeys: [
                { id: '1', label: '选项1', key: 'custom_field_option_pqrst' },
                { id: '2', label: '选项2', key: 'custom_field_option_uvwxy' },
                { id: '3', label: '选项3', key: 'custom_field_option_zabcd' }
            ],
            width: 'half'
        }
    },
    {
        type: 'checkbox',
        label: '复选框',
        icon: <CheckBoxIcon />,
        defaultProps: {
            label: '复选框',
            description: '',
            fieldKey: '',
            options: ['选项1', '选项2', '选项3'],
            optionsWithKeys: [
                { id: '1', label: '选项1', key: 'custom_field_option_efghi' },
                { id: '2', label: '选项2', key: 'custom_field_option_jklmn' },
                { id: '3', label: '选项3', key: 'custom_field_option_opqrs' }
            ],
            width: 'half'
        }
    },
    {
        type: 'date',
        label: '日期选择',
        icon: <DateIcon />,
        defaultProps: {
            label: '日期选择',
            description: '',
            fieldKey: '',
            width: 'half'
        }
    }, {
        type: 'dateRange',
        label: '日期区间',
        icon: <DateRangeIcon />,
        defaultProps: {
            label: '日期区间',
            description: '',
            fieldKey: '',
            width: 'half'
        }
    },
    {
        type: 'file',
        label: '附件',
        icon: <FileIcon />,
        defaultProps: {
            label: '附件',
            description: '',
            fieldKey: '',
            width: 'half'
        }
    },
    {
        type: 'user',
        label: '用户',
        icon: <UserIcon />,
        defaultProps: {
            label: '用户',
            description: '',
            fieldKey: '',
            width: 'half'
        }
    },
    {
        type: 'department',
        label: '部门',
        icon: <GroupsIcon />,
        defaultProps: {
            label: '部门',
            description: '',
            fieldKey: '',
            width: 'half'
        }
    },
    {
        type: 'link',
        label: '链接',
        icon: <Link />,
        defaultProps: {
            label: '链接',
            description: '',
            fieldKey: '',
            width: 'half'
        }
    },
    {
        type: 'richText',
        label: '富文本',
        icon: <EditNote />,
        defaultProps: {
            label: '富文本',
            description: '',
            fieldKey: '',
            width: 'half'
        }
    },
    {
        type: 'externalData',
        label: '外部数据源',
        icon: <DateIcon />,
        defaultProps: {
            label: '外部数据源',
            description: '',
            fieldKey: '',
            width: 'half'
        }
    }
];


const InfoComponentTemplates: ComponentTemplate[] = [
    {
        type: 'customCreator',
        label: '创建人',
        icon: <SelectIcon />,
        defaultProps: {
            label: '创建人',
            description: '',
            fieldKey: '',
            width: 'half'
        }
    }, {
        type: 'customCreatedAt',
        label: '创建时间',
        icon: <SelectIcon />,
        defaultProps: {
            label: '创建时间',
            description: '',
            fieldKey: '',
            width: 'half'
        }
    }, {
        type: 'ticketStatus',
        label: '工单状态',
        icon: <SelectIcon />,
        defaultProps: {
            label: '工单状态',
            description: '',
            fieldKey: '',
            width: 'half'
        }
    }, {
        type: 'approvalStatus',
        label: '审批状态',
        icon: <SelectIcon />,
        defaultProps: {
            label: '审批状态',
            description: '',
            fieldKey: '',
            width: 'half'
        }
    }, {
        type: 'ticketType',
        label: '工单类型',
        icon: <SelectIcon />,
        defaultProps: {
            label: '工单类型',
            description: '',
            fieldKey: '',
            width: 'half'
        }
    }, {
        type: 'currentHandler',
        label: '当前处理人',
        icon: <SelectIcon />,
        defaultProps: {
            label: '当前处理人',
            description: '',
            fieldKey: '',
            width: 'half'
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