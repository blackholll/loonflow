import {
    Add as AddIcon,
    Delete as DeleteIcon,
    Visibility as VisibilityIcon,
    VisibilityOff as VisibilityOffIcon
} from '@mui/icons-material';
import {
    Alert,
    Box,
    Button,
    Checkbox,
    FormControl,
    FormControlLabel,
    FormLabel,
    IconButton,
    InputLabel,
    Link,
    MenuItem,
    Radio,
    RadioGroup,
    Select,
    TextField,
    Typography
} from '@mui/material';
import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { materialDark } from 'react-syntax-highlighter/dist/esm/styles/prism';
import TemplateEditor from '../../../../components/commonComponents/inputs/TemplateEditor';
import { IFormSchema, IWorkflowComponent, IWorkflowComponentRow } from '../../../../types/workflow';
import { FormOption } from '../../../../types/workflowDesign';


interface ComponentPropertiesProps {
    component: IWorkflowComponent | IWorkflowComponentRow;
    onUpdate: (component: IWorkflowComponent | IWorkflowComponentRow) => void;
    formSchema: IFormSchema;
}

const EXTERNAL_DATA_SERVER_SAMPLE = `# This is sample for external data source server's code using Django.
# Request body: JSON snapshot of ticket field values. Response: {"code": 0, "data": {"value": ...}, "msg": ""}
import hashlib
import json
from django.http import JsonResponse
from django.views import View

class TicketMockExternalDataSourceView(BaseView):
    """
    Mock endpoint for external data source field testing.
    Expects the same headers as hook calls: signature + timestamp (md5(timestamp + token)).
    Request body is the ticket fields JSON object.
    Response shape matches fetch_external_data_source_value: code 0 and data.value.

    Query params:
    - style or displayStyle: json | key_value | text (same as form field displayStyle).
      Demo payload is shaped for that rendering mode.
    - token: optional, for signature_check when signature/timestamp are sent.
    """

    @staticmethod
    def _demo_value_for_style(style: str, _body: dict) -> object:
        """Minimal sample values for each displayStyle (_body is the ticket fields POST body, unused)."""
        if style == 'json':
            return [
                {'id': 1, 'name': 'demo_item_a', 'ok': True},
                {'id': 2, 'name': 'demo_item_b', 'ok': False},
            ]

        if style == 'key_value':
            return {'a': 1, 'b': 2, 'c': 3}

        return 'this is a sample text from external'

    def post(self, request, *args, **kwargs):
        signature = request.META.get('HTTP_SIGNATURE')
        timestamp = request.META.get('HTTP_TIMESTAMP')
        token = "" # should be the same as you configured in loonflow
        if token and signature and timestamp:
            try:
                common_service_ins.signature_check(timestamp, signature, token)
            except CustomCommonException as e:
                return api_response(-1, str(e), {})

        # you can return the result base on ticket detail info from body
        try:
            body = json.loads(request.body.decode('utf-8')) if request.body else {}
        except (json.JSONDecodeError, UnicodeDecodeError):
            body = {}
        if not isinstance(body, dict):
            body = {}

        raw_style = (
            request.GET.get('style')
            or request.GET.get('displayStyle')
            or 'text'
        )
        style = str(raw_style).strip().lower()
        if style in ('keyvalue', 'key-value'):
            style = 'key_value'
        if style not in ('json', 'key_value', 'text'):
            style = 'text'

        demo_value = self._demo_value_for_style(style, body)
        return api_response(0, '', {'value': demo_value})
`;

function ComponentProperties({ component, onUpdate, formSchema }: ComponentPropertiesProps) {
    const [showOptionKeys, setShowOptionKeys] = useState(false);
    const [showExternalDataSample, setShowExternalDataSample] = useState(false);
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
        fields.push({ key: 'creator', label: t('common.creator') });

        setAvailableFields(fields);
    }, [formSchema, t]);

    const handleChange = (key: string, value: any) => {
        if (key === 'precision') {
            const nextProps = {
                ...(component as IWorkflowComponent).props,
                precision: value
            };
            if (typeof value === 'number' && value > 0) {
                nextProps.allowDecimal = true;
            }
            onUpdate({
                ...component,
                props: nextProps
            });
            return;
        }

        // 将需要写入 props 的键统一处理
        if ([
            'multiple', 'placeholder', 'defaultValue',
            'format', 'timeFormat', 'dateFormat', 'timeZone', 'timeZoneName',
            'titleTemplate', 'titleGenerateMode',
            // number 组件相关 props
            'allowDecimal', 'fixedPrecision', 'thousandSeparator', 'allowNegative',
            'precision', 'min', 'max', 'unitPrefix', 'unitSuffix',
            // 选项类
            'optionsWithKeys',
            'dataSourceUrl',
            'dataSourceToken',
            'displayStyle'
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
                label={t('common.name')}
                value={(component as IWorkflowComponent).componentName || ''}
                onChange={(e) => handleChange('componentName', e.target.value)}
                fullWidth
                size="small"
                required
                disabled={['title', 'creator_info', 'created_at', 'ticket_nodes', 'act_state', 'workflow_info', 'current_assignee_infos'].includes(component.type)}
                error={!((component as IWorkflowComponent).componentName || '').trim()}
                helperText={!((component as IWorkflowComponent).componentName || '').trim() ? t('workflow.componentProperties.fieldNameHelperText') : ''}
            />

            <TextField
                label={t('common.description')}
                value={(component as IWorkflowComponent).description || ''}
                onChange={(e) => handleChange('description', e.target.value)}
                fullWidth
                disabled={['title', 'creator_info', 'created_at', 'ticket_nodes', 'act_state', 'workflow_info', 'current_assignee_infos'].includes(component.type)}
                size="small"
                multiline
                rows={2}
                placeholder={t('workflow.componentProperties.fieldDescriptionHelperText')}
            />

            {component.type === 'externaldata' && (
                <>
                    <Alert severity="info">{t('workflow.componentProperties.externalDataReadonlyNote')}</Alert>
                    <TextField
                        label={t('workflow.componentProperties.dataSourceUrl')}
                        value={(component as IWorkflowComponent).props?.dataSourceUrl || ''}
                        onChange={(e) => handleChange('dataSourceUrl', e.target.value)}
                        fullWidth
                        size="small"
                        required
                        error={!((component as IWorkflowComponent).props?.dataSourceUrl || '').trim()}
                        helperText={
                            !((component as IWorkflowComponent).props?.dataSourceUrl || '').trim()
                                ? t('workflow.componentProperties.dataSourceUrlRequired')
                                : ''
                        }
                    />
                    <TextField
                        label={t('workflow.componentProperties.dataSourceToken')}
                        value={(component as IWorkflowComponent).props?.dataSourceToken || ''}
                        onChange={(e) => handleChange('dataSourceToken', e.target.value)}
                        fullWidth
                        size="small"
                        type="password"
                        autoComplete="new-password"
                        required
                        error={!((component as IWorkflowComponent).props?.dataSourceToken || '').trim()}
                        helperText={
                            !((component as IWorkflowComponent).props?.dataSourceToken || '').trim()
                                ? t('workflow.componentProperties.dataSourceTokenRequired')
                                : ''
                        }
                    />
                    <Link
                        component="button"
                        type="button"
                        variant="body2"
                        onClick={() => setShowExternalDataSample(!showExternalDataSample)}
                    >
                        {showExternalDataSample
                            ? t('workflow.componentProperties.hideExternalDataSample')
                            : t('workflow.componentProperties.showExternalDataSample')}
                    </Link>
                    {showExternalDataSample && (
                        <SyntaxHighlighter
                            language="python"
                            style={materialDark}
                            showLineNumbers
                            customStyle={{ margin: 0, borderRadius: '4px' }}
                        >
                            {EXTERNAL_DATA_SERVER_SAMPLE}
                        </SyntaxHighlighter>
                    )}
                    <FormControl fullWidth size="small">
                        <InputLabel>{t('workflow.componentProperties.displayStyle')}</InputLabel>
                        <Select
                            value={(component as IWorkflowComponent).props?.displayStyle || 'text'}
                            label={t('workflow.componentProperties.displayStyle')}
                            onChange={(e) => handleChange('displayStyle', e.target.value)}
                        >
                            <MenuItem value="json">{t('workflow.componentProperties.displayStyleJson')}</MenuItem>
                            <MenuItem value="key_value">{t('workflow.componentProperties.displayStyleKeyValue')}</MenuItem>
                            <MenuItem value="text">{t('workflow.componentProperties.displayStyleText')}</MenuItem>
                        </Select>
                    </FormControl>
                </>
            )}

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

            {(['text', 'textarea', 'richtext'].includes(component.type as string)) && (
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
            {component.type === 'time' && (
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>

                    <FormControl fullWidth size="small">
                        <InputLabel>{t('workflow.componentProperties.timeFormat')}</InputLabel>
                        <Select
                            value={(component as IWorkflowComponent).props?.format || 'HH:mm'}
                            label={t('workflow.componentProperties.timeFormat')}
                            onChange={(e) => handleChange('format', e.target.value)}
                        >
                            <MenuItem value="HH:mm">{t('common.dateTimePicker.timeFormatHourMin')}</MenuItem>
                            <MenuItem value="HH:mm:ss">{t('common.dateTimePicker.timeFormatHourMinSec')}</MenuItem>
                        </Select>
                    </FormControl>
                </Box>
            )}

            {/* datetime 类型属性配置 */}
            {component.type === 'datetime' && (
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                    <FormControl fullWidth size="small">
                        <InputLabel>{t('workflow.componentProperties.dateTimeFormat')}</InputLabel>
                        <Select
                            value={(component as IWorkflowComponent).props?.format || 'YYYY-MM-DD HH:mm:ss'}
                            label={t('workflow.componentProperties.dateTimeFormat')}
                            onChange={(e) => handleChange('format', e.target.value)}
                        >
                            <MenuItem value="YYYY-MM-DD HH:mm">{t('common.dateTimePicker.dateTimeFormatHourMin')}</MenuItem>
                            <MenuItem value="YYYY-MM-DD HH:mm:ss">{t('common.dateTimePicker.dateTimeFormatHourMinSec')}</MenuItem>
                        </Select>
                    </FormControl>
                </Box>
            )}

            {/* number 类型属性配置 */}
            {component.type === 'number' && (
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
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
                                checked={(component as IWorkflowComponent).props?.allowNegative ?? false}
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