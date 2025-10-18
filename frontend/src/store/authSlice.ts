import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import camelcaseKeys from 'camelcase-keys';
import { jwtDecode } from 'jwt-decode';


interface AuthState {
  isAuthenticated: boolean;
  user: null | User
}

interface User {
  name: string,
  alias: string,
  email: string,
  type: string,
  tenantId: string,
}

const initialState: AuthState = {
  isAuthenticated: false,
  user: null
};

export const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    loginState: (state, action: PayloadAction<string>) => {
      console.log('Before:', state);
      state.isAuthenticated = true;
      const decoded: any = jwtDecode(action.payload);
      state.user = camelcaseKeys(decoded.data, { deep: true }) as User;
      console.log('state111111:', state);
      console.log('statestatestatestatestatestate');
      console.log('After:', state); // 打印状态
    },
    logoutState: (state) => {
      state.isAuthenticated = false;
      state.user = null;
    },
  },
});

export const { loginState, logoutState } = authSlice.actions;

export const authReducer = authSlice.reducer;