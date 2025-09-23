import { IApiResponse, ILabel } from '../types/common';
import { v4 as uuidv4 } from 'uuid';


export interface ILayout {
  span: number,
  orderId?: number
}

export interface INodeLayout {
  x: number,
  y: number,

}
export interface IProps {
  placeholder?: string,
  defaultValue?: any,
  [key: string]: any
}
export interface ISimpleWorkflowEntity {
  id: string,
  workflowId: string,
  name: string,
  description: string
}
export interface IWorkflowEntity {
  id: string,
  name: string,
  description: string,
  version: string,
  workflowId: string,
  createdAt: string,
  updatedAt: string,
  creator: string,
}

export interface ISimpleWorkflowListResData {
  page: number;
  perPage: number;
  total: number;
  workflowInfoList: ISimpleWorkflowEntity[]
}

export interface IWorkflowListResData {
  page: number;
  perPage: number;
  total: number;
  workflowInfoList: IWorkflowEntity[]
}

export interface IWorkflowDetailInfo {
  basicInfo: {
    name: string,
    description: string
  }
  noticeInfo: {
    title: string,
    content: string
  }
  fieldInfoList: []
}

export interface ISimpleWorkflowListRes extends IApiResponse<ISimpleWorkflowListResData> { }

export interface IWorkflowListRes extends IApiResponse<IWorkflowListResData> { }

export interface IWorkflowVersionEntity {
  id: string,
  name: string,
  description: string,
  status: string,
  createdAt: string,
  updatedAt: string,
}
export interface IWorkflowVersionListResData {
  page: number;
  perPage: number;
  total: number;
  versionInfoList: IWorkflowVersionEntity[]
}
export interface IWorkflowVersionListRes extends IApiResponse<IWorkflowVersionListResData> { }

export interface IWorkflowComponent {
  id: string,
  componentKey: string,
  componentName: string,
  componentPermission?: 'readonly' | 'optional' | 'required' | 'hidden',
  value?: any,
  description: string,
  type: 'text' | 'textarea' | 'number' | 'select' | 'radio' | 'checkbox' | 'time' | 'date' | 'user' | 'department' | 'file' | 'link' | 'richText' | 'externalData' | 'customCreator' | 'customCreatedAt' | 'ticketStatus' | 'approvalStatus' | 'ticketType' | 'currentHandler' | 'title' | 'ticketNodes',
  layout: ILayout,
  label: ILabel,
  props: IProps,
}

export interface IWorkflowComponentRow {
  id: string,
  componentKey: string,
  componentName: string,
  description: string,
  type: 'row',
  layout: ILayout,
  label: ILabel,
  children: IWorkflowComponent[],
  props: IProps,
}

export interface IWorkflowFiledPermission {
  [key: string]: 'readonly' | 'write_optional' | 'write_required'
}
export interface IWorkflowNodeProps {
  allowRetreat: boolean,
  rememberLastParticipant: boolean,
  fieldPermissions: IWorkflowFiledPermission,
  participantType: 'user' | 'department',
  participant: string,
  distributeType: 'direct' | 'random',
  [key: string]: any
}
export interface IWorkflowNode {
  id: string,
  type: 'start' | 'end' | 'common' | 'parallel' | 'exclusive' | 'timer' | 'hook',
  name: string,
  label: ILabel,
  layout: INodeLayout,
  props: IWorkflowNodeProps,
}

export interface IWorkflowEdgeProps {
  validateField: boolean,
  condition: string,
  confirmMessage: string,
  [key: string]: any
}
export interface IWorkflowEdge {
  id: string,
  name: string,
  type: 'accept' | 'reject' | 'other',
  sourceNodeId: string,
  targetNodeId: string,
  label: ILabel,
  props: IWorkflowEdgeProps,
  layout: {
    souceHandle: string,
    targetHandle: string
  }
}

export interface INotification {
  titleTemplate: string,
  contentTemplate: string,
  selectedChannelList: string[],
}
export interface IWorkflowHook {
  id: string,
  url: string,
  token: string,
  eventList: ('pre_start' | 'started' | 'force_closed' | 'nomal_end' | 'rejected' | 'withdrawn')[],
}

export interface IWorkflowMetadata {
  id: string,
  name: string,
  versionId: string,
  versionName: string,
  description: string
}
export interface IFormSchema {
  componentInfoList: (IWorkflowComponentRow | IWorkflowComponent)[]
  workflowMetadata?: IWorkflowMetadata
}

export interface IProcessSchema {
  nodeInfoList: IWorkflowNode[],
  edgeInfoList: IWorkflowEdge[],
}
export interface IAdvancedSchema {
  notificationInfo: INotification,
  permissionInfo: IpermissionInfo,
  customizationInfo: ICustomizationInfo,
}
export interface IpermissionInfo {
  adminIdList: string[],
  dispatcherIdList: string[],
  viewerIdList: string[],
  viewerDeptIdList: string[]
}
export interface ICustomizationInfo {
  authorizedAppIdList: string[],
  label: ILabel,
  hookInfoList: IWorkflowHook[]
}

export interface IBasicInfo {
  id: string,
  name: string,
  description: string,
  version: string,
  tenantId: string
}

export interface IWorkflowFullDefinition {
  basicInfo: IBasicInfo,
  formSchema: IFormSchema
  processSchema: IProcessSchema
  advancedSchema: IAdvancedSchema
}

export const createEmptyWorkflowFullDefinition = (): IWorkflowFullDefinition => {
  return {
    basicInfo: {
      id: `temp_${uuidv4()}`,
      name: '',
      description: '',
      version: '',
      tenantId: ''
    },
    formSchema: {
      componentInfoList: []
    },
    processSchema: {
      nodeInfoList: [],
      edgeInfoList: []
    },
    advancedSchema: {
      notificationInfo: {
        titleTemplate: '',
        contentTemplate: '',
        selectedChannelList: []
      },
      permissionInfo: {
        adminIdList: [],
        dispatcherIdList: [],
        viewerIdList: [],
        viewerDeptIdList: []
      },
      customizationInfo: {
        authorizedAppIdList: [],
        label: {},
        hookInfoList: []
      },
    }
  }
}

export interface IWorkflowFullDefinitionRes extends IApiResponse<{ workflowFullDefination: IWorkflowFullDefinition }> { }

export interface IWorkflowReleaseRes extends IApiResponse<{ workflowId: string }> { }

export interface IWorkflowNodeSchema {
  id: string,
  type: 'start',
  name: string,
  label: ILabel,
  props: IWorkflowNodeProps,
}

export interface IWorkflowInitNodeRes extends IApiResponse<{ initNode: IWorkflowNodeSchema }> { }

export interface IWorkflowAction {
  id: string,
  name: string,
  type: 'accept' | 'reject' | 'other' | 'add_comment' | 'forward' | 'consult' | 'consult_submit',
  props: IWorkflowEdgeProps,
}

export interface IWorkflowActionsRes extends IApiResponse<{ actions: IWorkflowAction }> { }

export interface IWorkflowCreationFormRes extends IApiResponse<{ formSchema: IFormSchema }> { }

export interface IWorkflowDiagram {
  nodeInfoList: IWorkflowNode[],
  edgeInfoList: IWorkflowEdge[],
}

export interface IWorkflowDiagramRes extends IApiResponse<{ processSchema: IWorkflowDiagram }> { }
