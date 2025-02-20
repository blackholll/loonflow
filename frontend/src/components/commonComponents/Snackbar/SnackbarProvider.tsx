// src/components/Snackbar/SnackbarProvider.tsx
import React, { createContext, useContext, useState, ReactNode } from 'react';
import GlobalSnackbar from './GlobalSnackbar';

interface SnackbarContextType {
  showMessage: (message: string, severity: 'error' | 'warning' | 'info' | 'success') => void;
}

export const SnackbarContext = createContext<SnackbarContextType | undefined>(undefined);

interface SnackbarProviderProps {
  children: ReactNode;
}

const SnackbarProvider: React.FC<SnackbarProviderProps> = ({ children }) => {
  const [open, setOpen] = useState(false);
  const [message, setMessage] = useState('');
  const [severity, setSeverity] = useState<'error' | 'warning' | 'info' | 'success'>('info');

  const handleClose = (event: React.SyntheticEvent | Event, reason?: string) => {
    if (reason === 'clickaway') {
      return;
    }
    setOpen(false);
  };

  const showMessage = (msg: string, sev: 'error' | 'warning' | 'info' | 'success') => {
    setMessage(msg);
    setSeverity(sev);
    setOpen(true);
  };

  return (
    <SnackbarContext.Provider value={{ showMessage }}>
      {children}
      <GlobalSnackbar
        open={open}
        onClose={handleClose}
        message={message}
        severity={severity}
      />
    </SnackbarContext.Provider>
  );
};

export default SnackbarProvider;