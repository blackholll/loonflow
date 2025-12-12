
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

// create function to get component templates
const getBasicComponentTemplates = (t: any): ComponentTemplate[] => [
    {
        type: 'text',
        componentName: t('workflow.componentCategories.textComponent'),
        icon: <TextFieldsIcon />,
        defaultProps: {
            description: '',
            fieldKey: '',
            placeholder: '',
            layout: { span: 6 }
        }
    },
    {
        type: 'textarea',
        componentName: t('workflow.componentCategories.textareaComponent'),
        icon: <TextFieldsIcon />,
        defaultProps: {
            description: '',
            fieldKey: '',
            placeholder: '',
            layout: { span: 6 }
        }
    },
    {
        type: 'number',
        componentName: t('workflow.componentCategories.numberComponent'),
        icon: <NumberIcon />,
        defaultProps: {
            description: '',
            fieldKey: '',
            placeholder: '',
            layout: { span: 6 },
            props: {
                allowNegative: false,
                allowDecimal: false,
                fixedPrecision: false,
                thousandSeparator: true,
                precision: 0,
                min: 0,
                max: 0,
                unitPrefix: '',
                unitSuffix: ''
            }
        }
    },
    {
        type: 'select',
        componentName: t('workflow.componentCategories.selectComponent'),
        icon: <SelectIcon />,
        defaultProps: {
            description: '',
            fieldKey: '',
            props: {
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
            description: '',
            fieldKey: '',
            props: {
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
            description: '',
            fieldKey: '',
            props: {
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
            description: '',
            fieldKey: '',
            layout: { span: 6 },
            props: {
                format: 'HH:mm:ss'
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
            props: {
                format: 'YYYY-MM-DD'
            }
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
            props: {
                format: 'YYYY-MM-DD HH:mm:ss'
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
            description: '',
            fieldKey: '',
            layout: { span: 6 },
            props: {
                multiple: false
            }
        }
    },
    {
        type: 'department',
        componentName: t('workflow.componentCategories.departmentComponent'),
        icon: <GroupsIcon />,
        defaultProps: {
            description: '',
            fieldKey: '',
            layout: { span: 6 },
            props: {
                multiple: false
            }
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
            description: '',
            fieldKey: '',
            layout: { span: 6 },
            props: {
                titleGenerateMode: 'manual',
            }
        }
    }, {
        type: 'creator_info',
        componentName: t('workflow.componentCategories.customCreatorComponent'),
        icon: <CreatorIcon />,
        defaultProps: {
            description: '',
            fieldKey: '',
            layout: { span: 6 }
        }
    }, {
        type: 'created_at',
        componentName: t('workflow.componentCategories.customCreatedAtComponent'),
        icon: <CalendarMonth />,
        defaultProps: {
            description: '',
            fieldKey: '',
            layout: { span: 6 }
        }
    }, {
        type: 'ticket_node_infos',
        componentName: t('workflow.componentCategories.ticketNodesComponent'),
        icon: <TicketNodesIcon />,
        defaultProps: {
            description: '',
            fieldKey: '',
            layout: { span: 6 }
        }
    }, {
        type: 'act_state',
        componentName: t('workflow.componentCategories.approvalStatusComponent'),
        icon: <TicketActStatusIcon />,
        defaultProps: {
            description: '',
            fieldKey: '',
            layout: { span: 6 }
        }
    }, {
        type: 'workflow_info',
        componentName: t('workflow.componentCategories.ticketTypeComponent'),
        icon: <DefaultIcon />,
        defaultProps: {
            description: '',
            fieldKey: '',
            layout: { span: 6 }
        }
    }, {
        type: 'current_assignee_infos',
        componentName: t('workflow.componentCategories.currentHandlerComponent'),
        icon: <CreatorIcon />,
        defaultProps: {
            description: '',
            fieldKey: '',
            layout: { span: 6 }
        }
    }
];

// create function to get component categories
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