import axios from "axios";
import * as API from './API';


const instance = axios.create({
    baseURL: '/api/v1.0',
  });

export async function getSimpleWorkflowList(params: API.SimpleWorkflowListType) {
    const response = await instance.get('/simple_workflows', {params:params});
    return response.data;
}