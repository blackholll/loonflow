import { IWorkflowComponent } from "../../../../types/workflow";
import {
    TextField,
    NumberField,
    TextAreaField,
    SelectField,
    RadioField,
    CheckboxField,
    TimeField,
    DateField,
    DateTimeField,
    FileField,
    UserField,
    DepartmentField,
    TicketCreatorField,
    TicketCreatedAtField,
    TicketNodesField,
    TicketActStateField,
    WorkflowInfoField,
    TicketCurrentAssigneeInfosField
    // UserField,
    // DepartmentField,
} from '../../../formFields';
import React, { useState, useEffect } from 'react';

interface RenderFormComponentProps {
    component: IWorkflowComponent;
    handleComponentUpdate: (updatedComponent: IWorkflowComponent) => void;
}

function RenderFormComponent({ component, handleComponentUpdate }: RenderFormComponentProps): React.ReactElement {
    // 根据组件类型和multiple属性确定初始值
    const getInitialValue = () => {
        const defaultValue = component?.props?.value || component?.props?.defaultValue;
        if (defaultValue !== undefined) {
            return defaultValue;
        }

        // 对于用户和部门字段，如果multiple为true，初始值应该是数组
        if ((component?.type === 'user' || component?.type === 'department') && component?.props?.multiple) {
            return [];
        }

        return '';
    };

    const [value, setValue] = useState(getInitialValue());

    const handleFieldChange = (newValue: any) => {
        if (handleComponentUpdate && component) {
            const updatedComponent = {
                ...component,
                props: {
                    ...component.props,
                    value: newValue
                }
            };
            setValue(newValue);
            handleComponentUpdate(updatedComponent);
        }
    };

    // 同步value状态
    useEffect(() => {
        const currentValue = component?.props?.value || component?.props?.defaultValue;
        if (currentValue !== undefined && currentValue !== value) {
            setValue(currentValue);
        }
    }, [component?.props?.value, component?.props?.defaultValue, value]);

    // 添加防护措施，确保组件参数有效
    if (!component || !component.type) {
        console.warn('RenderFormComponent: Invalid component received', component);
        return <div>无效的组件</div>;
    }

    // 根据组件类型渲染不同的表单字段
    switch (component.type) {
        case 'text':
            return (
                <TextField
                    value={value}
                    fieldRequired={component.componentPermission === 'required'}
                    onChange={handleFieldChange}
                    mode={component.componentPermission === 'readonly' ? 'view' : 'edit'}
                    props={component.props}
                />
            );
        case 'textarea':
            return (
                <TextAreaField
                    value={value}
                    fieldRequired={component.componentPermission === 'required'}
                    onChange={handleFieldChange}
                    mode={component.componentPermission === 'readonly' ? 'view' : 'edit'}
                    props={component.props}
                />
            );
        case 'number':
            return (
                <NumberField
                    value={value}
                    fieldRequired={component.componentPermission === 'required'}
                    onChange={handleFieldChange}
                    mode={component.componentPermission === 'readonly' ? 'view' : 'edit'}
                    props={component.props}
                />
            );
        case 'select':
            return (
                <SelectField
                    value={value}
                    fieldRequired={component.componentPermission === 'required'}
                    onChange={handleFieldChange}
                    mode={component.componentPermission === 'readonly' ? 'view' : 'edit'}
                    props={component.props}
                />
            );
        case 'radio':
            return (
                <RadioField
                    value={value}
                    fieldRequired={component.componentPermission === 'required'}
                    onChange={handleFieldChange}
                    mode={component.componentPermission === 'readonly' ? 'view' : 'edit'}
                    props={component.props}
                />
            );
        case 'checkbox':
            return (
                <CheckboxField
                    value={value}
                    fieldRequired={component.componentPermission === 'required'}
                    onChange={handleFieldChange}
                    mode={component.componentPermission === 'readonly' ? 'view' : 'edit'}
                    props={component.props}
                />
            );
        case 'time':
            return (
                <TimeField
                    value={value}
                    fieldRequired={component.componentPermission === 'required'}
                    onChange={handleFieldChange}
                    mode={component.componentPermission === 'readonly' ? 'view' : 'edit'}
                    props={component.props}
                />
            );
        case 'date':
            return (
                <DateField
                    value={value}
                    fieldRequired={component.componentPermission === 'required'}
                    onChange={handleFieldChange}
                    mode={component.componentPermission === 'readonly' ? 'view' : 'edit'}
                    props={component.props}
                />
            );
        case 'datetime':
            return (
                <DateTimeField
                    value={value}
                    fieldRequired={component.componentPermission === 'required'}
                    onChange={handleFieldChange}
                    mode={component.componentPermission === 'readonly' ? 'view' : 'edit'}
                    props={component.props}
                />
            );
        case 'file':
            return (
                <FileField
                    value={value}
                    fieldRequired={component.componentPermission === 'required'}
                    onChange={handleFieldChange}
                    mode={component.componentPermission === 'readonly' ? 'view' : 'edit'}
                    props={component.props}
                />
            );
        case 'user':
            return (
                <UserField
                    value={value}
                    fieldRequired={component.componentPermission === 'required'}
                    onChange={handleFieldChange}
                    mode={component.componentPermission === 'readonly' ? 'view' : 'edit'}
                    props={component.props}
                />
            );
        case 'department':
            return (
                <DepartmentField
                    value={value}
                    fieldRequired={component.componentPermission === 'required'}
                    onChange={handleFieldChange}
                    mode={component.componentPermission === 'readonly' ? 'view' : 'edit'}
                    props={component.props}
                />
            );
        case 'creator_info':
            return (
                <TicketCreatorField
                    value={value}
                />
            );
        case 'created_at':
            return (
                <TicketCreatedAtField
                    value={value}
                />
            );
        case 'ticket_node_infos':
            return (
                <TicketNodesField
                    value={value}
                />
            );
        case 'act_state':
            return (
                <TicketActStateField
                    value={value}
                />
            );
        case 'workflow_info':
            return (
                <WorkflowInfoField
                    value={value}
                />
            );
        case 'current_assignee_infos':
            return (
                <TicketCurrentAssigneeInfosField
                    value={value}
                />
            );
        // case 'textarea':
        //     return (
        //         <TextField
        //             field={fieldData}
        //             value={component.props?.defaultValue || ''}
        //             onChange={handleFieldChange}
        //             mode="design"
        //             size="small"
        //             variant="outlined"
        //             fullWidth
        //             multiline
        //             rows={3}
        //         />
        //     );
        // case 'number':
        //     return (
        //         <NumberField
        //             field={fieldData}
        //             value={component.props?.defaultValue || ''}
        //             onChange={handleFieldChange}
        //             mode="design"
        //             size="small"
        //             variant="outlined"
        //             fullWidth
        //         />
        //     );
        // case 'select':
        //     return (
        //         <SelectField
        //             field={fieldData}
        //             value={component.props?.defaultValue || ''}
        //             onChange={handleFieldChange}
        //             mode="design"
        //             size="small"
        //             variant="outlined"
        //             fullWidth
        //             multiple={component.props?.multiple || false}
        //             options={component.props?.optionsWithKeys || []}
        //         />
        //     );
        // case 'radio':
        //     return (
        //         <SelectField
        //             field={fieldData}
        //             value={component.props?.defaultValue || ''}
        //             onChange={handleFieldChange}
        //             mode="design"
        //             size="small"
        //             variant="outlined"
        //             fullWidth
        //             multiple={false}
        //             options={component.props?.optionsWithKeys || []}
        //         />
        //     );
        // case 'checkbox':
        //     return (
        //         <SelectField
        //             field={fieldData}
        //             value={component.props?.defaultValue || ''}
        //             onChange={handleFieldChange}
        //             mode="design"
        //             size="small"
        //             variant="outlined"
        //             fullWidth
        //             multiple={true}
        //             options={component.props?.optionsWithKeys || []}
        //         />
        //     );
        // case 'date':
        //     return (
        //         <DateTimeField
        //             field={fieldData}
        //             value={component.props?.defaultValue || ''}
        //             onChange={handleFieldChange}
        //             mode="design"
        //             size="small"
        //             variant="outlined"
        //             fullWidth
        //             type="date"
        //         />
        //     );
        // case 'time':
        //     return (
        //         <DateTimeField
        //             field={fieldData}
        //             value={component.props?.defaultValue || ''}
        //             onChange={handleFieldChange}
        //             mode="design"
        //             size="small"
        //             variant="outlined"
        //             fullWidth
        //             type="time"
        //         />
        //     );
        // case 'user':
        //     return (
        //         <UserField
        //             field={fieldData}
        //             value={component.props?.defaultValue || ''}
        //             onChange={handleFieldChange}
        //             mode="design"
        //             size="small"
        //             variant="outlined"
        //             fullWidth
        //             multiple={component.props?.multiple || false}
        //             users={component.props?.users || []}
        //         />
        //     );
        // case 'department':
        //     return (
        //         <DepartmentField
        //             field={fieldData}
        //             value={component.props?.defaultValue || ''}
        //             onChange={handleFieldChange}
        //             mode="design"
        //             size="small"
        //             variant="outlined"
        //             fullWidth
        //             multiple={component.props?.multiple || false}
        //             departments={component.props?.departments || []}
        //         />
        //     );
        default:
            return (
                <TextField
                    value={value}
                    fieldRequired={false}
                    onChange={handleFieldChange}
                    mode={component.componentPermission === 'readonly' ? 'view' : 'edit'}
                    props={component.props}
                />
            );
    }
}

export default RenderFormComponent;