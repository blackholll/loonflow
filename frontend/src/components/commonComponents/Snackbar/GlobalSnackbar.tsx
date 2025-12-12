// src/components/Snackbar/GlobalSnackbar.tsx
import { Alert, Snackbar } from '@mui/material';
import React from 'react';

interface GlobalSnackbarProps {
  open: boolean;
  onClose: (event: React.SyntheticEvent | Event, reason?: string) => void;
  message: string | React.ReactNode;
  severity: 'error' | 'warning' | 'info' | 'success';
}

const GlobalSnackbar: React.FC<GlobalSnackbarProps> = ({ open, onClose, message, severity }) => {
  return (
    <Snackbar
      open={open}
      autoHideDuration={5000}
      onClose={onClose}
      anchorOrigin={{
        vertical: 'top',
        horizontal: 'center',
      }}
    >
      <Alert onClose={onClose} severity={severity}>
        {message}
      </Alert>
    </Snackbar>
  );
};

export default GlobalSnackbar;