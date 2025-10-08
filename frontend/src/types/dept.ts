import { ISimpleUser } from "./user";

export interface ISimpleDept {
    id: string;
    name: string;
    children: ISimpleDept[];
}

export interface ISimpleDeptPath {
    id: string;
    name: string;
    path: string;
}

export interface ISimpleParentDept {
    id: string;
    name: string;
}

export interface IDept {
    id: string;
    name: string;
    label: any;
    creatorInfo: ISimpleUser,
    leaderInfo: ISimpleUser,
    approverInfoList: ISimpleUser[],
    children: IDept,
    parentDeptInfo: ISimpleParentDept,
}


