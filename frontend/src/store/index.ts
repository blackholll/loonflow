import { configureStore } from '@reduxjs/toolkit';
import { persistStore, persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage';
import { authReducer, loginState, logoutState } from './authSlice'; // 导入 reducer 和 actions

const persistConfig = {
  key: 'root',
  storage,
};

const persistedReducer = persistReducer(persistConfig, authReducer);


const store = configureStore({
  reducer: {
    auth: persistedReducer,
  },
});
export const persistor = persistStore(store);

export type RootState = ReturnType<typeof store.getState>;


export { store, loginState, logoutState }; 
