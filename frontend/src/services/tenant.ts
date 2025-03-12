import apiClient from "./api";
import {ITenantDetailRes} from "../types/tenant";

export const getTenantDetail = async (tenantId: string): Promise<ITenantDetailRes> => {
  try {
    const response = await apiClient.get(`/api/v1.0/accounts/tenants/${tenantId}`);
    return response.data;
  } catch (error) {
    throw error;
  }
}

export const getTenantByDomain = async (domain: string): Promise<ITenantDetailRes> => {
  try {
    const response = await apiClient.get('/api/v1.0/accounts/tenants/by_domain', {
      params: { domain }
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};