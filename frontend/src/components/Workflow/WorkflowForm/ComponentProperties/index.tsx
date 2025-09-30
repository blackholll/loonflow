import React, { useState, useEffect } from 'react';
import {
    Box,
    Typography,
    TextField,
    Select,
    MenuItem,
    FormControl,
    InputLabel,
    Button,
    IconButton,
    Alert,
    FormControlLabel,
    Checkbox,
    RadioGroup,
    Radio,
    FormLabel
} from '@mui/material';
import {
    Delete as DeleteIcon,
    Add as AddIcon,
    Visibility as VisibilityIcon,
    VisibilityOff as VisibilityOffIcon
} from '@mui/icons-material';
import { FormOption } from '../../../../types/workflowDesign';
import { IWorkflowComponent, IWorkflowComponentRow, IFormSchema } from '../../../../types/workflow';
import TemplateEditor from '../../../../components/commonComponents/inputs/TemplateEditor';
import { useTranslation } from 'react-i18next';


interface ComponentPropertiesProps {
    component: IWorkflowComponent | IWorkflowComponentRow;
    onUpdate: (component: IWorkflowComponent | IWorkflowComponentRow) => void;
    formSchema: IFormSchema;
}

function ComponentProperties({ component, onUpdate, formSchema }: ComponentPropertiesProps) {
    const [showOptionKeys, setShowOptionKeys] = useState(false);
    const [availableFields, setAvailableFields] = useState<{ key: string; label: string }[]>([]);

    const { t } = useTranslation();
    useEffect(() => {
        const fields: { key: string; label: string }[] = [];

        formSchema.componentInfoList.forEach((component) => {
            if (component.type === 'row' && 'children' in component) {
                component.children.forEach((childComponent) => {
                    if (childComponent.componentKey !== 'title')
                        fields.push({
                            key: childComponent.componentKey,
                            label: childComponent.componentName
                        });
                });
            }
        });
        fields.push({ key: 'created_at', label: t('common.createdAt') });
        fields.push({ key: 'updated_at', label: t('common.updatedAt') });
        fields.push({ key: 'creator', label: t('common.creator') });

        setAvailableFields(fields);
    }, [formSchema, t]);

    const handleChange = (key: string, value: any) => {
        // 将需要写入 props 的键统一处理
        if ([
            'multiple', 'placeholder', 'defaultValue',
            'format', 'timeFormat', 'dateFormat', 'timeZone', 'timeZoneName',
            'titleTemplate', 'titleGenerateMode',
            // number 组件相关 props
            'allowDecimal', 'fixedPrecision', 'thousandSeparator', 'allowNegative',
            'precision', 'min', 'max', 'unitPrefix', 'unitSuffix',
            // 选项类
            'optionsWithKeys'
        ].indexOf(key) !== -1) {
            onUpdate({
                ...component,
                props: {
                    ...(component as IWorkflowComponent).props,
                    [key]: value
                }
            });
            return;
        }
        onUpdate({
            ...component,
            [key]: value
        });
    };

    const handleLayoutChange = (key: string, value: any) => {
        onUpdate({
            ...component,
            layout: {
                ...component.layout,
                [key]: value
            }
        });
    };

    const handleOptionChange = (index: number, value: string) => {
        if (component.type === 'row') return;

        const formComponent = component as IWorkflowComponent;
        const newOptionsWithKeys = [...(formComponent.props?.optionsWithKeys || [])];
        newOptionsWithKeys[index] = {
            ...newOptionsWithKeys[index],
            label: value
        };
        handleChange('optionsWithKeys', newOptionsWithKeys);
    };

    const addOption = () => {
        if (component.type === 'row') return;

        const formComponent = component as IWorkflowComponent;
        const newOption: FormOption = {
            id: `option_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
            label: `${t('workflow.componentProperties.options')}${(formComponent.props?.optionsWithKeys?.length || 0) + 1}`,
            key: `custom_field_option_${Math.random().toString(36).substr(2, 5)}`
        };
        const newOptionsWithKeys = [...(formComponent.props?.optionsWithKeys || []), newOption];
        handleChange('optionsWithKeys', newOptionsWithKeys);
    };

    const removeOption = (index: number) => {
        if (component.type === 'row') return;

        const formComponent = component as IWorkflowComponent;
        const newOptionsWithKeys = (formComponent.props?.optionsWithKeys || []).filter((_: FormOption, i: number) => i !== index);
        handleChange('optionsWithKeys', newOptionsWithKeys);
    };

    const toggleOptionKeysVisibility = () => {
        setShowOptionKeys(!showOptionKeys);
    };

    if (component.type === 'row') {
        return null;
    }

    return (
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <TextField
                label={t('workflow.componentProperties.fieldKey')}
                value={(component as IWorkflowComponent).componentKey || ''}
                fullWidth
                size="small"
                disabled
                helperText={t('workflow.componentProperties.fieldKeyHelperText')}
            />

            <TextField
                label={t('name')}
                value={(component as IWorkflowComponent).componentName || ''}
                onChange={(e) => handleChange('componentName', e.target.value)}
                fullWidth
                size="small"
                required
                disabled={component.type === 'title'}
                error={!((component as IWorkflowComponent).componentName || '').trim()}
                helperText={!((component as IWorkflowComponent).componentName || '').trim() ? t('workflow.componentProperties.fieldNameHelperText') : ''}
            />

            <TextField
                label={t('description')}
                value={(component as IWorkflowComponent).description || ''}
                onChange={(e) => handleChange('description', e.target.value)}
                fullWidth
                disabled={component.type === 'title'}
                size="small"
                multiline
                rows={2}
                placeholder={t('workflow.componentProperties.fieldDescriptionHelperText')}
            />


            {component.type === 'title' && (
                <>
                    <FormLabel id="demo-row-radio-buttons-group-label" required>{t('workflow.componentProperties.titleGenerateMode')}</FormLabel>
                    <RadioGroup
                        row
                        aria-labelledby="demo-row-radio-buttons-group-label"
                        name="row-radio-buttons-group"
                        onChange={(e) => handleChange('titleGenerateMode', e.target.value)}
                        value={component.props.titleGenerateMode}
                    >
                        <FormControlLabel value="manual" control={<Radio />} label={t('workflow.componentProperties.manualInput')} />
                        <FormControlLabel value="automatic" control={<Radio />} label={t('workflow.componentProperties.autoGenerate')} />
                    </RadioGroup>
                </>
            )}

            {component.type === 'title' && component.props.titleGenerateMode === 'automatic' ? (
                <>
                    <FormLabel id="template-editor-label" required>{t('workflow.componentProperties.titleTemplate')}</FormLabel>
                    <TemplateEditor
                        value={component.props.titleTemplate}
                        onChange={(e) => handleChange('titleTemplate', e)}
                        availableFields={availableFields}
                        placeholder={t('workflow.componentProperties.titleTemplatePlaceholder')}
                    />
                </>
            ) : null}

            {(component.type === 'text' || component.type === 'textarea') && (
                <TextField
                    label={t('workflow.componentProperties.placeholder')}
                    value={(component as IWorkflowComponent).props.placeholder || ''}
                    onChange={(e) => handleChange('placeholder', e.target.value)}
                    fullWidth
                    size="small"
                />
            )}


            {['select', 'user', 'department'].indexOf(component.type) !== -1 && (
                <FormControlLabel
                    control={
                        <Checkbox
                            checked={(component as IWorkflowComponent).props?.multiple || false}
                            onChange={(e) => handleChange('multiple', e.target.checked)}
                            size="small"
                        />
                    }
                    label={t('workflow.componentProperties.supportMultiple')}
                />
            )}

            <FormControl fullWidth size="small">
                <InputLabel>{t('workflow.componentProperties.width')}</InputLabel>
                <Select
                    value={(component as IWorkflowComponent).layout.span || 12}
                    label={t('workflow.componentProperties.width')}
                    onChange={(e) => handleLayoutChange('span', Number(e.target.value))}
                >
                    <MenuItem value={3}>1/4</MenuItem>
                    <MenuItem value={4}>1/3</MenuItem>
                    <MenuItem value={6}>1/2</MenuItem>
                    <MenuItem value={12}>{t('workflow.componentProperties.fullWidth')}</MenuItem>
                </Select>
            </FormControl>
            {component.type === 'time' ? (<FormControl fullWidth size="small">
                <InputLabel>{t('workflow.componentProperties.timeFormat')}</InputLabel>
                <Select
                    value={(component as IWorkflowComponent).layout.span || 12}
                    label={t('workflow.componentProperties.timeFormat')}
                    onChange={(e) => handleLayoutChange('format', e.target.value)}
                >
                    <MenuItem value={"hh:mm:ss a"}>{t('workflow.componentProperties.timeFormatHourMinSec')}</MenuItem>
                    <MenuItem value={"hh aa"}>{t('workflow.componentProperties.timeFormatHour')}</MenuItem>
                    <MenuItem value={"mm:ss"}>{t('workflow.componentProperties.timeFormatMinSec')}</MenuItem>
                </Select>
            </FormControl>) : null}

            {/* number 类型属性配置 */}
            {component.type === 'number' && (
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                    <TextField
                        label={t('workflow.componentProperties.placeholder')}
                        value={(component as IWorkflowComponent).props?.placeholder || ''}
                        onChange={(e) => handleChange('placeholder', e.target.value)}
                        fullWidth
                        size="small"
                    />

                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={(component as IWorkflowComponent).props?.allowDecimal !== false}
                                onChange={(e) => handleChange('allowDecimal', e.target.checked)}
                                size="small"
                            />
                        }
                        label={t('workflow.componentProperties.allowDecimal')}
                    />

                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={(component as IWorkflowComponent).props?.fixedPrecision === true}
                                onChange={(e) => handleChange('fixedPrecision', e.target.checked)}
                                size="small"
                            />
                        }
                        label={t('workflow.componentProperties.fixedDecimalScale')}
                    />

                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={(component as IWorkflowComponent).props?.thousandSeparator ?? true}
                                onChange={(e) => handleChange('thousandSeparator', e.target.checked)}
                                size="small"
                            />
                        }
                        label={t('workflow.componentProperties.thousandSeparator')}
                    />

                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={(component as IWorkflowComponent).props?.allowNegative ?? true}
                                onChange={(e) => handleChange('allowNegative', e.target.checked)}
                                size="small"
                            />
                        }
                        label={t('workflow.componentProperties.allowNegative')}
                    />

                    <TextField
                        label={t('workflow.componentProperties.precision')}
                        type="number"
                        value={(component as IWorkflowComponent).props?.precision ?? ''}
                        onChange={(e) => handleChange('precision', e.target.value === '' ? '' : Number(e.target.value))}
                        size="small"
                        fullWidth
                    />

                    <TextField
                        label={t('workflow.componentProperties.min')}
                        type="number"
                        value={(component as IWorkflowComponent).props?.min ?? ''}
                        onChange={(e) => handleChange('min', e.target.value === '' ? '' : Number(e.target.value))}
                        size="small"
                        fullWidth
                    />

                    <TextField
                        label={t('workflow.componentProperties.max')}
                        type="number"
                        value={(component as IWorkflowComponent).props?.max ?? ''}
                        onChange={(e) => handleChange('max', e.target.value === '' ? '' : Number(e.target.value))}
                        size="small"
                        fullWidth
                    />

                    <TextField
                        label={t('workflow.componentProperties.unitPrefix')}
                        value={(component as IWorkflowComponent).props?.unitPrefix || ''}
                        onChange={(e) => handleChange('unitPrefix', e.target.value)}
                        size="small"
                        fullWidth
                    />

                    <TextField
                        label={t('workflow.componentProperties.unitSuffix')}
                        value={(component as IWorkflowComponent).props?.unitSuffix || ''}
                        onChange={(e) => handleChange('unitSuffix', e.target.value)}
                        size="small"
                        fullWidth
                    />
                </Box>
            )}

            {(component.type === 'select' || component.type === 'radio' || component.type === 'checkbox') && (
                <Box>
                    <Typography variant="subtitle2" gutterBottom>
                        {t('workflow.componentProperties.options')}
                    </Typography>

                    <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
                        <Button
                            variant="outlined"
                            size="small"
                            onClick={addOption}
                            startIcon={<AddIcon />}
                            sx={{ flex: 1 }}
                        >
                            {t('workflow.componentProperties.addOption')}
                        </Button>
                        <Button
                            variant="outlined"
                            size="small"
                            onClick={toggleOptionKeysVisibility}
                            startIcon={showOptionKeys ? <VisibilityOffIcon /> : <VisibilityIcon />}
                            sx={{ flex: 1 }}
                        >
                            {showOptionKeys ? t('workflow.componentProperties.hideOptionKeys') : t('workflow.componentProperties.showOptionKeys')}
                        </Button>
                    </Box>

                    {showOptionKeys && <Alert severity="info">{t('workflow.componentProperties.optionKeysInfo')}</Alert>}

                    {(component as IWorkflowComponent).props?.optionsWithKeys?.map((option: FormOption, index: number) => (
                        <Box key={option.id} sx={{ display: 'flex', gap: 1, mb: 1 }}>
                            <TextField
                                value={showOptionKeys ? `${option.label} (${option.key})` : option.label}
                                onChange={(e) => handleOptionChange(index, e.target.value)}
                                size="small"
                                sx={{ flex: 1 }}
                                disabled={showOptionKeys}
                            />
                            {showOptionKeys ? null : <IconButton
                                size="small"
                                color="error"
                                onClick={() => removeOption(index)}
                            >
                                <DeleteIcon fontSize="small" />
                            </IconButton>}
                        </Box>
                    ))}
                </Box>
            )}
        </Box>
    );
}

export default ComponentProperties;