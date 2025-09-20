import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField, FormControl, FormLabel, RadioGroup, FormControlLabel, Radio, Icon, Box, Tooltip, InputAdornment, Autocomplete } from '@mui/material';
import { useTranslation } from 'react-i18next';
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import { addApplication } from '../../../services/application';
import useSnackbar from '../../../hooks/useSnackbar';
import { debounce } from 'lodash';
import { getSimpleUsers } from '../../../services/user';
import { addDept, getDeptDetail, updateDept } from '../../../services/dept';

// 定义用户接口
interface User {
  id: string;
  name: string;
  alias: string;
  email: string;
}

interface DeptDetailProps {
  open: boolean
  onClose: (needRefresh: boolean) => void
  deptId?: string,
  selectedDeptId: string,
  selectedDeptName: string
}

const DeptDialog = ({ open, onClose, deptId, selectedDeptId, selectedDeptName }: DeptDetailProps) => {
  const { t } = useTranslation();
  const [name, setName] = useState('');
  const [loading, setLoading] = useState(false);
  const { showMessage } = useSnackbar();

  // 为每个选择框维护独立的用户列表和加载状态
  const [leaderUserList, setLeaderUserList] = useState<User[]>([]);
  const [leaderSearchLoading, setLeaderSearchLoading] = useState(false);
  const [selectedLeader, setSelectedLeader] = useState<User | null>(null);
  const [editDeptParentName, setEditDeptParentName] = useState('');
  const [editDeptParentId, setEditDeptParentId] = useState('');

  const [deptLeaderId, setDeptLeaderId] = useState<string>('');
  const [leaderInputValue, setLeaderInputValue] = useState('');

  const [approverUserList, setApproverUserList] = useState<User[]>([]);
  const [approverSearchLoading, setApproverSearchLoading] = useState(false);
  const [deptApproverList, setDeptApproverList] = useState<string[]>([]);
  const [approverInputValue, setApproverInputValue] = useState('');

  const [selectedApprovers, setSelectedApprovers] = useState<User[]>([]);

  const fetchSimpleUserList = useCallback(async (keyword: string, purpose: string) => {
    if (keyword.length < 2) {
      return;
    }

    try {
      if (purpose === 'leader') {
        setLeaderSearchLoading(true);
      } else {
        setApproverSearchLoading(true);
      }

      const result = await getSimpleUsers(keyword);
      if (result.code === 0) {
        if (purpose === 'leader') {
          setLeaderUserList(result.data.userInfoList);
        } else {
          setApproverUserList(result.data.userInfoList);
        }

      } else {
        showMessage(result.msg, 'error');
      }
    } catch (error: any) {
      showMessage('搜索用户失败', 'error');
    } finally {
      setLeaderSearchLoading(false);
      setApproverSearchLoading(false);
    }
  }, [showMessage]);

  const debouncedFetchSimpleUsers = useMemo(
    () => debounce((keyword: string, purpose: string) => {
      fetchSimpleUserList(keyword, purpose);
    }, 500),
    [fetchSimpleUserList]
  );

  const handelSubmit = async () => {
    if (!name.trim()) {
      showMessage('请输入部门名称', 'error');
      return;
    }
    if (!deptLeaderId) {
      showMessage('请选择部门负责人', 'error');
      return;
    }
    if (deptId) {
      await updateDept(
        deptId,
        name,
        editDeptParentId,
        deptLeaderId,
        deptApproverList,
      )
    } else {
      await addDept(
        name,
        selectedDeptId,
        deptLeaderId,
        deptApproverList,
      )
    }

    onClose(true);
    setName('');
    setDeptLeaderId('');
    setSelectedLeader(null);
    setLeaderInputValue('');
    setDeptApproverList([]);
    setSelectedApprovers([]);
    setApproverInputValue('');
    console.log('submit')
    // add dept
  }

  useEffect(() => {
    const fetchDeptDetail = async () => {
      if (deptId) {
        try {
          setLoading(true);
          const result = await getDeptDetail(deptId);
          if (result.code === 0) {
            setName(result.data.deptInfo.name);
            setEditDeptParentId(result.data.deptInfo.parentDeptInfo?.id || '');
            setEditDeptParentName(result.data.deptInfo.parentDeptInfo?.name || '');
            setDeptLeaderId(result.data.deptInfo.leaderInfo.id);
            setSelectedLeader(result.data.deptInfo.leaderInfo);
            setSelectedApprovers(result.data.deptInfo.approverInfoList);
          }
          setLoading(false);
        } catch (error: any) {
          showMessage(error.message, 'error');
        }
      }

    }
    fetchDeptDetail();
  }, [deptId, showMessage]);

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth style={{ maxWidth: 600, margin: '0 auto' }}>
      <DialogTitle>{deptId ? t('common.update') : t('common.add')}</DialogTitle>
      <DialogContent>
        <TextField
          label="Name"
          value={name}
          required
          fullWidth
          margin="normal"
          onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
            setName(event.target.value);
          }}
        />

        <TextField
          disabled
          fullWidth
          id="outlined-disabled"
          helperText="please select parent department on the left parent tree"
          label="上级部门"
          value={editDeptParentName || selectedDeptName}
        />
        <Autocomplete
          value={selectedLeader}
          onChange={(_event, newValue) => {
            setSelectedLeader(newValue)
            setDeptLeaderId(newValue?.id || '')
          }}
          inputValue={leaderInputValue}
          onInputChange={(_event, newValue) => {
            console.log('leader new value: ', newValue)
            setLeaderInputValue(newValue);
            debouncedFetchSimpleUsers(newValue, 'leader');
          }}
          getOptionLabel={(option) => {
            console.log('option: ', option)
            if (!option) return '';
            return `${option.name}(${option.alias})`;
          }}
          isOptionEqualToValue={(option, value) => option.id === value.id}
          disablePortal
          options={leaderUserList}
          loading={leaderSearchLoading}
          noOptionsText={leaderInputValue.length < 2 ? "请至少输入2个字符搜索" : "无匹配结果"}
          sx={{ marginTop: 2, marginBottom: 2 }}
          renderInput={(params) => (
            <TextField
              {...params}
              required
              label='部门负责人'
              slotProps={{
                input: {
                  ...params.InputProps,
                  endAdornment: (
                    <>
                      {leaderSearchLoading ? <InputAdornment position="end">搜索中...</InputAdornment> : null}
                      {params.InputProps.endAdornment}
                    </>
                  ),
                }
              }}
            />
          )}
        />

        <Autocomplete
          multiple
          value={selectedApprovers}
          onChange={(_event, newValue) => {
            setSelectedApprovers(newValue);
            setDeptApproverList(newValue.map(user => user.id));
          }}
          inputValue={approverInputValue}
          onInputChange={(_event, newValue) => {
            console.log('approve new value: ', newValue)
            setApproverInputValue(newValue);
            debouncedFetchSimpleUsers(newValue, 'approver');
          }}
          getOptionLabel={(option) => {
            if (!option) return '';
            return `${option.name}(${option.alias})`;
          }}
          isOptionEqualToValue={(option, value) => option.id === value.id}
          disablePortal
          options={approverUserList}
          loading={approverSearchLoading}
          noOptionsText={approverInputValue.length < 2 ? "请至少输入2个字符搜索" : "无匹配结果"}
          sx={{ marginTop: 2, marginBottom: 2 }}
          renderInput={(params) => (
            <TextField
              {...params}
              label='部门审批人'
              slotProps={{
                input: {
                  ...params.InputProps,
                  endAdornment: (
                    <>
                      {approverSearchLoading ? <InputAdornment position="end">搜索中...</InputAdornment> : null}
                      {params.InputProps.endAdornment}
                    </>
                  ),
                }
              }}
            />
          )}
        />




      </DialogContent>
      <DialogActions>
        <Button autoFocus onClick={() => onClose(false)}>
          {t('common.cancel')}
        </Button>
        <Button onClick={() => handelSubmit()} disabled={loading}>{t('common.save')}</Button>
      </DialogActions>
    </Dialog>
  )
}

export default DeptDialog;