// src/components/Snackbar/GlobalSnackbar.tsx
import React from 'react';
import { Snackbar, Alert, SnackbarProps } from '@mui/material';

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