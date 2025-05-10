import { ISimpleUser } from "./user";

export interface ISimpleDept {
    id: string;
    name: string;
    children: ISimpleDept[];
}

export interface ISimpleParentDept {
    id: string;
    name: string;
}

export interface IDept {
    id: string;
    name: string;
    label: any;
    creator_info: ISimpleUser,
    leader_info: ISimpleUser,
    approver_info_list: ISimpleUser[],
    children: IDept,
    parent_dept_info: ISimpleParentDept,
}


