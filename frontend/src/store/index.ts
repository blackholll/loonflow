import { configureStore } from '@reduxjs/toolkit';
import { persistStore, persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage';
import { authReducer, loginState, logoutState } from './authSlice';
import { tenantReducer, setTenantBasicInfo, clearTenantInfo } from './tenantSlice';

const persistConfig = {
  key: 'root',
  storage,
};

const persistedAuthReducer = persistReducer(persistConfig, authReducer);
const persistedTenantReducer = persistReducer(persistConfig, tenantReducer);

const store = configureStore({
  reducer: {
    auth: persistedAuthReducer,
    tenant: persistedTenantReducer,
  },
});
export const persistor = persistStore(store);

export type RootState = ReturnType<typeof store.getState>;

export { store, loginState, logoutState, setTenantBasicInfo, clearTenantInfo };
