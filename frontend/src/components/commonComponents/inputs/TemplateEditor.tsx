import { Close } from '@mui/icons-material';
import { Box, Button, IconButton } from '@mui/material';
import { CompositeDecorator, ContentState, Editor, EditorState as EditorStateClass, Modifier, SelectionState } from 'draft-js';
import 'draft-js/dist/Draft.css';
import React, { useRef } from 'react';
import { useTranslation } from 'react-i18next';


function TagSpan(props: any) {
    const { availableFields, onDelete } = props;
    const keyMatch = /\{([\w.]+)\}/.exec(props.decoratedText);
    let label = props.children;

    // 如果 children 是对象，尝试获取文本内容
    if (typeof label === 'object' && label !== null) {
        if (Array.isArray(label) && label.length > 0) {
            label = label[0];
        } else if (label.props && label.props.children) {
            label = label.props.children;
        } else {
            label = label.toString();
        }
    }

    if (keyMatch && availableFields) {
        const found = availableFields.find((f: any) => f.key === keyMatch[1]);
        if (found) label = found.label;
    }

    const handleDelete = (e: React.MouseEvent) => {
        e.preventDefault();
        e.stopPropagation();
        if (onDelete && keyMatch) {
            // 通过内容状态查找匹配的文本位置
            const contentState = props.contentState;
            const text = contentState.getFirstBlock().getText();
            const tagText = keyMatch[0];

            // 查找所有匹配项，找到当前装饰器对应的那个
            const regex = new RegExp(tagText.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g');
            let match;
            while ((match = regex.exec(text)) !== null) {
                const start = match.index;
                const end = start + tagText.length;

                // 检查这个位置是否与当前装饰器匹配
                if (props.decoratedText === tagText) {
                    onDelete(tagText, start, end);
                    break;
                }
            }
        }
    };

    return (
        <Box
            sx={{
                display: 'inline-flex',
                alignItems: 'center',
                background: '#eee',
                borderRadius: '16px',
                padding: '4px 8px',
                margin: '0 2px',
                fontSize: '14px',
                fontWeight: 500,
                position: 'relative'
            }}
        >
            <span>{label}</span>
            <IconButton
                size="small"
                onClick={handleDelete}
                onMouseDown={handleDelete}
                sx={{
                    width: '16px',
                    height: '16px',
                    padding: 0,
                    marginLeft: '4px',
                    '&:hover': {
                        backgroundColor: 'rgba(0, 0, 0, 0.1)'
                    }
                }}
            >
                <Close sx={{ fontSize: '12px' }} />
            </IconButton>
        </Box>
    );
}

function tagStrategy(contentBlock: any, callback: any, _contentState: any) {
    const text = contentBlock.getText();
    const regex = /\{([\w.]+)\}/g;
    let matchArr, start;
    while ((matchArr = regex.exec(text)) !== null) {
        start = matchArr.index;
        // 装饰整个 field 区块，包含大括号
        callback(start, start + matchArr[0].length, {
            tagText: matchArr[0],
            start: start,
            end: start + matchArr[0].length
        });
    }
}

function createDecorator(availableFields: { key: string; label: string }[], onDelete?: (tagText: string, start: number, end: number) => void) {
    return new CompositeDecorator([
        {
            strategy: tagStrategy,
            component: (props: any) => <TagSpan {...props} availableFields={availableFields} onDelete={onDelete} />,
        },
    ]);
}

export interface TemplateEditorProps {
    value: string;
    onChange: (val: string) => void;
    availableFields: { key: string; label: string }[];
    placeholder?: string;
}

export default function TemplateEditor({ value, onChange, availableFields, placeholder }: TemplateEditorProps) {
    const { t } = useTranslation();
    const editorRef = useRef<any>(null);

    const [editorState, setEditorState] = React.useState(() =>
        value
            ? EditorStateClass.createWithContent(ContentState.createFromText(value), createDecorator(availableFields))
            : EditorStateClass.createEmpty(createDecorator(availableFields))
    );

    const handleDeleteField = React.useCallback((tagText: string, start: number, end: number) => {
        const contentState = editorState.getCurrentContent();
        const blockKey = contentState.getFirstBlock().getKey();
        const selection = SelectionState.createEmpty(blockKey).merge({
            anchorOffset: start,
            focusOffset: end,
        });

        const newContentState = Modifier.removeRange(contentState, selection, 'backward');
        const newEditorState = EditorStateClass.push(editorState, newContentState, 'remove-range');

        // 设置光标位置到删除位置
        const newSelection = SelectionState.createEmpty(blockKey).merge({
            anchorOffset: start,
            focusOffset: start,
        });
        const finalEditorState = EditorStateClass.forceSelection(newEditorState, newSelection);

        setEditorState(finalEditorState);
    }, [editorState]);

    const handleBeforeInput = (chars: string) => {
        const selection = editorState.getSelection();
        const contentState = editorState.getCurrentContent();
        const blockKey = selection.getStartKey();
        const block = contentState.getBlockForKey(blockKey);
        const text = block.getText();
        const startOffset = selection.getStartOffset();

        // 检查光标是否在零宽空格后面
        if (startOffset > 0 && text.charAt(startOffset - 1) === '\u200B') {
            // 如果光标在零宽空格后面，替换零宽空格为输入的字符
            const newSelection = selection.merge({
                anchorOffset: startOffset - 1,
                focusOffset: startOffset,
            });
            const newContentState = Modifier.replaceText(contentState, newSelection, chars);
            const newEditorState = EditorStateClass.push(editorState, newContentState, 'insert-characters');

            // 设置光标位置到插入字符后
            const finalSelection = newSelection.merge({
                anchorOffset: startOffset,
                focusOffset: startOffset,
            });
            const finalEditorState = EditorStateClass.forceSelection(newEditorState, finalSelection);
            setEditorState(finalEditorState);
            return 'handled';
        }

        return 'not-handled';
    };

    const insertTag = (field: { key: string; label: string }) => {
        const contentState = editorState.getCurrentContent();
        const selection = editorState.getSelection();
        const tagText = `{${field.key}}\u200B`;
        // insert tag + zero width space
        let newContentState = Modifier.insertText(contentState, selection, tagText);
        // calculate final cursor position
        const afterTagOffset = selection.getStartOffset() + tagText.length;
        const newSelection = selection.merge({
            anchorOffset: afterTagOffset,
            focusOffset: afterTagOffset,
            isBackward: false,
        });
        // update editorState
        let newEditorState = EditorStateClass.push(editorState, newContentState, 'insert-characters');
        newEditorState = EditorStateClass.forceSelection(newEditorState, newSelection);
        setEditorState(newEditorState);
        setTimeout(() => editorRef.current && editorRef.current.focus(), 0);
    };

    // listen to content change, remove zero width space and pass to external
    React.useEffect(() => {
        const content = editorState.getCurrentContent();
        const raw = content.getPlainText();
        onChange(raw.replace(/\u200B/g, ''));
    }, [editorState, onChange]);

    // handle availableFields change, update decorator
    React.useEffect(() => {
        setEditorState((prev: any) => EditorStateClass.set(prev, { decorator: createDecorator(availableFields, handleDeleteField) }));
    }, [availableFields, handleDeleteField]);

    return (
        <Box>
            <Box
                sx={{
                    border: '1px solid #ccc',
                    borderRadius: 1,
                    minHeight: 48,
                    padding: 1,
                    cursor: 'text',
                    background: '#fafbfc',
                    mb: 1,
                }}
                onClick={() => editorRef.current && editorRef.current.focus()}
            >
                <Editor
                    ref={editorRef}
                    editorState={editorState}
                    onChange={setEditorState}
                    handleBeforeInput={handleBeforeInput}
                    placeholder={placeholder}
                />
            </Box>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 1 }}>
                {t('common.insert')}:
                {availableFields.map((field) => (
                    <Button
                        key={field.key}
                        size="small"
                        variant="outlined"
                        sx={{ background: '#f5f5f5' }}
                        onClick={() => insertTag(field)}
                    >
                        {field.label}
                    </Button>
                ))}
            </Box>
        </Box>
    );
} 