import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import {jwtDecode} from 'jwt-decode';

interface AuthState {
  isAuthenticated: boolean;
  user: null | { name: string}
}

interface User {
  name: string,
  alias: string,
  email: string,
  type: string
}

interface IjwtDecode {
  exp: number,
  iat: number
  data: User
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
      const decoded: IjwtDecode = jwtDecode(action.payload);
      state.user = decoded.data;
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