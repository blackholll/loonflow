
import { ComponentTemplate } from '../../../../types/workflowDesign';

import {
    CalendarMonth,
    CheckBox as CheckBoxIcon,
    Person as CreatorIcon,
    AcUnit as DefaultIcon,
    Groups as GroupsIcon,
    Pin as NumberIcon,
    RadioButtonChecked as RadioButtonIcon,
    Schedule,
    ExpandMore as SelectIcon,
    TextFields as TextFieldsIcon,
    MoreHoriz as TicketActStatusIcon,
    FiberManualRecord as TicketNodesIcon,
    Title as TitleIcon,
    Group as UserIcon
} from '@mui/icons-material';

// 创建获取组件模板的函数
const getBasicComponentTemplates = (t: any): ComponentTemplate[] => [
    {
        type: 'text',
        componentName: t('workflow.componentCategories.textComponent'),
        icon: <TextFieldsIcon />,
        defaultProps: {
            description: '',
            fieldKey: '',
            placeholder: t('workflow.componentCategories.textComponentDefaultPlaceholder'),
            layout: { span: 6 }
        }
    },
    {
        type: 'textarea',
        componentName: t('workflow.componentCategories.textareaComponent'),
        icon: <TextFieldsIcon />,
        defaultProps: {
            // label: '多行文本',
            description: '',
            fieldKey: '',
            placeholder: t('workflow.componentCategories.textareaComponentDefaultPlaceholder'),
            layout: { span: 6 }
        }
    },
    {
        type: 'number',
        componentName: t('workflow.componentCategories.numberComponent'),
        icon: <NumberIcon />,
        defaultProps: {
            // label: '数字',
            description: '',
            fieldKey: '',
            placeholder: t('workflow.componentCategories.numberComponentDefaultPlaceholder'),
            layout: { span: 6 }
        }
    },
    {
        type: 'select',
        componentName: t('workflow.componentCategories.selectComponent'),
        icon: <SelectIcon />,
        defaultProps: {
            // label: '下拉选择',
            description: '',
            fieldKey: '',
            extendedProps: {
                multiple: false,
                optionsWithKeys: [
                    { id: '1', label: t('workflow.componentCategories.optionComponentOption1'), key: 'custom_field_option_abcde' },
                    { id: '2', label: t('workflow.componentCategories.optionComponentOption2'), key: 'custom_field_option_fghij' },
                    { id: '3', label: t('workflow.componentCategories.optionComponentOption3'), key: 'custom_field_option_klmno' }
                ]
            },
            layout: { span: 6 }
        }
    },
    {
        type: 'radio',
        componentName: t('workflow.componentCategories.radioComponent'),
        icon: <RadioButtonIcon />,
        defaultProps: {
            // label: '单选框',
            description: '',
            fieldKey: '',
            extendedProps: {
                optionsWithKeys: [
                    { id: '1', label: t('workflow.componentCategories.optionComponentOption1'), key: 'custom_field_option_pqrst' },
                    { id: '2', label: t('workflow.componentCategories.optionComponentOption2'), key: 'custom_field_option_uvwxy' },
                    { id: '3', label: t('workflow.componentCategories.optionComponentOption3'), key: 'custom_field_option_zabcd' }
                ]
            },
            layout: { span: 6 }
        }
    },
    {
        type: 'checkbox',
        componentName: t('workflow.componentCategories.checkboxComponent'),
        icon: <CheckBoxIcon />,
        defaultProps: {
            // label: '复选框',
            description: '',
            fieldKey: '',
            extendedProps: {
                optionsWithKeys: [
                    { id: '1', label: t('workflow.componentCategories.optionComponentOption1'), key: 'custom_field_option_efghi' },
                    { id: '2', label: t('workflow.componentCategories.optionComponentOption2'), key: 'custom_field_option_jklmn' },
                    { id: '3', label: t('workflow.componentCategories.optionComponentOption3'), key: 'custom_field_option_opqrs' }
                ]
            },
            layout: { span: 6 }
        }
    },
    {
        type: 'time',
        componentName: t('workflow.componentCategories.timeComponent'),
        icon: <Schedule />,
        defaultProps: {
            // label: '时间选择',
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
        componentName: t('workflow.componentCategories.dateComponent'),
        icon: <CalendarMonth />,
        defaultProps: {
            description: '',
            fieldKey: '',
            layout: { span: 6 },
        }
    },
    {
        type: 'datetime',
        componentName: t('workflow.componentCategories.dateTimeComponent'),
        icon: <CalendarMonth />,
        defaultProps: {
            description: '',
            fieldKey: '',
            layout: { span: 6 },
            extendedProps: {
                format: 'yyyy-mm-dd hh:mm:ss'
            }
        }
    },
    // {
    //     type: 'file',
    //     componentName: t('workflow.componentCategories.fileComponent'),
    //     icon: <FileIcon />,
    //     defaultProps: {
    //         // label: '附件',
    //         description: '',
    //         fieldKey: '',
    //         layout: { span: 6 }
    //     }
    // },
    {
        type: 'user',
        componentName: t('workflow.componentCategories.userComponent'),
        icon: <UserIcon />,
        defaultProps: {
            // label: '用户',
            description: '',
            fieldKey: '',
            layout: { span: 6 }
        }
    },
    {
        type: 'department',
        componentName: t('workflow.componentCategories.departmentComponent'),
        icon: <GroupsIcon />,
        defaultProps: {
            // label: '部门',
            description: '',
            fieldKey: '',
            layout: { span: 6 }
        }
    }
    // {
    //     type: 'externalData',
    //     componentName: t('workflow.componentCategories.externalDataComponent'),
    //     icon: <DateIcon />,
    //     defaultProps: {
    //         // label: '外部数据源',
    //         description: '',
    //         fieldKey: '',
    //         layout: { span: 6 }
    //     }
    // }
];

const getInfoComponentTemplates = (t: any): ComponentTemplate[] => [
    {
        type: 'title',
        componentName: t('workflow.componentCategories.titleComponent'),
        icon: <TitleIcon />,
        defaultProps: {
            // label: '标题',
            description: '',
            fieldKey: '',
            layout: { span: 6 }
        }
    }, {
        type: 'creator_info',
        componentName: t('workflow.componentCategories.customCreatorComponent'),
        icon: <CreatorIcon />,
        defaultProps: {
            // label: '创建人',
            description: '',
            fieldKey: '',
            layout: { span: 6 }
        }
    }, {
        type: 'created_at',
        componentName: t('workflow.componentCategories.customCreatedAtComponent'),
        icon: <CalendarMonth />,
        defaultProps: {
            // label: '创建时间',
            description: '',
            fieldKey: '',
            layout: { span: 6 }
        }
    }, {
        type: 'ticket_node_infos',
        componentName: t('workflow.componentCategories.ticketNodesComponent'),
        icon: <TicketNodesIcon />,
        defaultProps: {
            // label: '工单状态',
            description: '',
            fieldKey: '',
            layout: { span: 6 }
        }
    }, {
        type: 'act_state',
        componentName: t('workflow.componentCategories.approvalStatusComponent'),
        icon: <TicketActStatusIcon />,
        defaultProps: {
            // label: '审批状态',
            description: '',
            fieldKey: '',
            layout: { span: 6 }
        }
    }, {
        type: 'workflow_info',
        componentName: t('workflow.componentCategories.ticketTypeComponent'),
        icon: <DefaultIcon />,
        defaultProps: {
            // label: '工单类型',
            description: '',
            fieldKey: '',
            layout: { span: 6 }
        }
    }, {
        type: 'current_assignee_infos',
        componentName: t('workflow.componentCategories.currentHandlerComponent'),
        icon: <CreatorIcon />,
        defaultProps: {
            // label: '当前处理人',
            description: '',
            fieldKey: '',
            layout: { span: 6 }
        }
    }
];

// 创建获取组件分类的函数
const getComponentCategories = (t: any) => ({
    basic: {
        title: t('workflow.componentCategories.basicComponent'),
        components: getBasicComponentTemplates(t)
    },
    info: {
        title: t('workflow.componentCategories.infoComponent'),
        components: getInfoComponentTemplates(t)
    }
});

export default getComponentCategories;