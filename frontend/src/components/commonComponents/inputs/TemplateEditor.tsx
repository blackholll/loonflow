import React, { useRef } from 'react';
import { Editor, Modifier, CompositeDecorator, ContentState, EditorState as EditorStateClass } from 'draft-js';
import 'draft-js/dist/Draft.css';
import { Box, Chip, Button } from '@mui/material';
import { useTranslation } from 'react-i18next';


function TagSpan(props: any) {
    const { availableFields } = props;
    const keyMatch = /\{\{([\w.]+)\}\}/.exec(props.decoratedText);
    let label = props.children;
    if (keyMatch && availableFields) {
        const found = availableFields.find((f: any) => f.key === keyMatch[1]);
        if (found) label = found.label;
    }
    return (
        <Chip
            size="small"
            label={label}
            sx={{ background: '#eee', fontWeight: 500, fontSize: 14, margin: '0 2px' }}
        />
    );
}

function tagStrategy(contentBlock: any, callback: any, contentState: any) {
    const text = contentBlock.getText();
    const regex = /\{\{([\w.]+)\}\}/g;
    let matchArr, start;
    while ((matchArr = regex.exec(text)) !== null) {
        start = matchArr.index;
        callback(start, start + matchArr[0].length);
    }
}

function createDecorator(availableFields: { key: string; label: string }[]) {
    return new CompositeDecorator([
        {
            strategy: tagStrategy,
            component: (props: any) => <TagSpan {...props} availableFields={availableFields} />,
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
    const [editorState, setEditorState] = React.useState(() =>
        value
            ? EditorStateClass.createWithContent(ContentState.createFromText(value), createDecorator(availableFields))
            : EditorStateClass.createEmpty(createDecorator(availableFields))
    );
    const editorRef = useRef<any>(null);

    const insertTag = (field: { key: string; label: string }) => {
        const contentState = editorState.getCurrentContent();
        const selection = editorState.getSelection();
        const tagText = `{{${field.key}}}\u200B`;
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
        setEditorState((prev: any) => EditorStateClass.set(prev, { decorator: createDecorator(availableFields) }));
    }, [availableFields]);

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