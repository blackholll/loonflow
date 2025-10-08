import { SxProps } from "@mui/material";
import { ButtonProps } from "@mui/material/Button";

export const getButtonProps = (actionType: string): Partial<ButtonProps> & { sx?: SxProps } => {
    switch (actionType) {
        case 'agree':
            return {
                variant: 'contained',
                color: 'success',
                sx: {
                    backgroundColor: '#4caf50',
                    '&:hover': {
                        backgroundColor: '#45a049',
                    }
                }
            };
        case 'reject':
            return {
                variant: 'contained',
                color: 'error',
                sx: {
                    backgroundColor: '#f44336',
                    '&:hover': {
                        backgroundColor: '#da190b',
                    }
                }
            };
        case 'forward':
        case 'consult':
        case 'consult_submit':
            return {
                variant: 'outlined',
                color: 'primary',
                sx: {
                    borderColor: '#1976d2',
                    color: '#1976d2',
                    '&:hover': {
                        backgroundColor: '#1976d2',
                        color: 'white',
                    }
                }
            };
        case 'add_comment':
            return {
                variant: 'outlined',
                color: 'primary',
                sx: {
                    borderColor: '#1976d2',
                    color: '#1976d2',
                    '&:hover': {
                        backgroundColor: '#1976d2',
                        color: 'white',
                    }
                }
            };
        case 'withdraw':
            return {
                variant: 'outlined',
                color: 'primary',
                sx: {
                    borderColor: '#1976d2',
                    color: '#1976d2',
                    '&:hover': {
                        backgroundColor: '#1976d2',
                        color: 'white',
                    }
                }
            };
        case 'other':
            return {
                variant: 'outlined',
                color: 'primary',
                sx: {
                    borderColor: '#1976d2',
                    color: '#1976d2',
                    '&:hover': {
                        backgroundColor: '#1976d2',
                        color: 'white',
                    }
                }
            };
        case 'force_forward':
            return {
                variant: 'outlined',
                color: 'secondary',
            };
        case 'force_close':
            return {
                variant: 'outlined',
                color: 'secondary',
            };
        case 'force_alter_node':
            return {
                variant: 'outlined',
                color: 'secondary',
            };
        default:
            return {
                variant: 'contained',
                color: 'primary'
            };
    }
};

export default getButtonProps;


