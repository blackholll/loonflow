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
    // UserField,
    // DepartmentField,
} from '../../../formFields';
import React, { useState } from 'react';

interface RenderFormComponentProps {
    component: IWorkflowComponent;
    handleComponentUpdate: (updatedComponent: IWorkflowComponent) => void;
}

function RenderFormComponent({ component, handleComponentUpdate }: RenderFormComponentProps): React.ReactElement {
    const [value, setValue] = useState(component?.props?.value || component?.props?.defaultValue || '');

    const handleFieldChange = (newValue: any) => {
        console.log('handleFieldChange1111', newValue)
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

    // useEffect(() => {
    //     setValue(component?.props?.value || component?.props?.defaultValue || '');
    // }, [component?.props?.value, component?.props?.defaultValue]);

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