import { Typography } from "@mui/material";


interface ViewFieldProps {
    type: string;
    value: string;
    props: any;
}

function ViewField({
    type,
    value,
    props
}: ViewFieldProps) {
    // todo: support more types
    let displayValue = '';
    if (type === 'datetime') {
        const date = new Date(value);
        displayValue = date.toLocaleString(undefined, { hour12: false });
    } else if (type === 'date') {
        const date = new Date(value);
        displayValue = date.toLocaleDateString();
    } else if (type === 'time') {
        // 如果是纯时间格式（HH:mm 或 HH:mm:ss），直接显示
        if (/^\d{2}:\d{2}(:\d{2})?$/.test(value)) {
            displayValue = value;
        } else {
            // 如果是ISO格式，解析并提取时间部分
            const date = new Date(value);
            if (!isNaN(date.getTime())) {
                displayValue = date.toLocaleTimeString(undefined, { hour12: false });
            } else {
                displayValue = value;
            }
        }
    } else {
        displayValue = value;
    }


    // return (<FormControl fullWidth={true}>
    //     <div style={{
    //         padding: '16.5px 14px',
    //         border: '1px solid #c0c0c0',
    //         borderRadius: '4px',
    //         backgroundColor: '#f5f5f5',
    //         minHeight: props.multiline ? `${props.rows * 24}px` : 'auto'
    //     }}>
    //         {displayValue || '-'}
    //     </div>
    // </FormControl>)

    return (<Typography variant="body2" sx={{ whiteSpace: 'pre-line' }}>{displayValue || '-'}</Typography>)
}

export default ViewField;