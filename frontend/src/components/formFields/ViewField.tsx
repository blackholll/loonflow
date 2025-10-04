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
    let displayValue = '-';
    if (type === 'text') {
        displayValue = value;
    } else if (type === 'number') {
        displayValue = value;
    } else if (type === 'select') {
        displayValue = value;
    } else if (type === 'datetime') {
        const date = new Date(value);
        displayValue = date.toLocaleString();
    } else if (type === 'date') {
        const date = new Date(value);
        displayValue = date.toLocaleDateString();
    } else if (type === 'time') {
        const date = new Date(value);
        displayValue = date.toLocaleTimeString();
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