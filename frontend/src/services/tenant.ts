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