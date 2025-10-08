import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { ITenantBasicInfo } from '../types/tenant';

interface TenantState {
  tenantInfo: ITenantBasicInfo | null;
  lastUpdateTime: number | null;
}

const initialState: TenantState = {
  tenantInfo: null,
  lastUpdateTime: null,
};

const tenantSlice = createSlice({
  name: 'tenant',
  initialState,
  reducers: {
    setTenantBasicInfo: (state, action: PayloadAction<ITenantBasicInfo>) => {
      state.tenantInfo = action.payload;
      state.lastUpdateTime = Date.now();
    },
    clearTenantInfo: (state) => {
      state.tenantInfo = null;
      state.lastUpdateTime = null;
    },
  },
});

export const { setTenantBasicInfo, clearTenantInfo } = tenantSlice.actions;
export const tenantReducer = tenantSlice.reducer;