import React, { useEffect, useState } from 'react';
import {
  Container,
  Typography,
  Avatar,
  Card,
  CardContent,
  Box,
  Chip,
  Divider,
  CircularProgress,
  Alert,
  Paper,
  Stack
} from '@mui/material';
import Grid from '@mui/material/Grid2';
import {
  Business as BusinessIcon,
  Language as LanguageIcon,
  AccountTree as WorkflowIcon,
  Assignment as AssignmentIcon,
  Info as InfoIcon,
  CheckCircle as CheckCircleIcon,
  Cancel as CancelIcon
} from '@mui/icons-material';
import { getTenantDetail } from '../../../services/tenant';
import { ITenantDetailResEntity } from '@/types/tenant';
import useSnackbar from '../../../hooks/useSnackbar';
import { useSelector } from 'react-redux';
import { RootState } from '../../../store';
import { useTranslation } from 'react-i18next';

function Tenant() {
  const [tenantDetail, setTenantDetail] = useState<ITenantDetailResEntity | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const { showMessage } = useSnackbar();
  const tenantId = useSelector((state: RootState) => state.auth.user?.tenantId ?? '');
  const { t } = useTranslation();

  useEffect(() => {
    const fetchTenantInfo = async () => {
      try {
        setLoading(true);
        setError(null);
        const res = await getTenantDetail(tenantId);
        if (res.code === 0) {
          setTenantDetail(res.data.tenantInfo);
        } else {
          setError(res.msg);
          showMessage(res.msg, 'error');
        }
      } catch (error: any) {
        setError(error.message);
        showMessage(error.message, 'error');
      } finally {
        setLoading(false);
      }
    };
    fetchTenantInfo();
  }, [tenantId, showMessage]);

  // 加载状态
  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '400px' }}>
          <Stack alignItems="center" spacing={2}>
            <CircularProgress size={60} />
            <Typography variant="h6" color="text.secondary">
              加载租户信息中...
            </Typography>
          </Stack>
        </Box>
      </Container>
    );
  }

  // 错误状态
  if (error) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <Alert severity="error" sx={{ mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            加载失败
          </Typography>
          <Typography>
            {error}
          </Typography>
        </Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {/* 页面标题 */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 'bold', color: 'primary.main' }}>
          <BusinessIcon sx={{ mr: 2, verticalAlign: 'middle' }} />
          {t("setting.tenant.tenantInfo")}
        </Typography>
      </Box>

      {/* 主要信息卡片 */}
      <Card sx={{ mb: 4, boxShadow: 3, borderRadius: 2 }}>
        <CardContent sx={{ p: 4 }}>
          <Grid container spacing={4} alignItems="center">
            {/* 租户头像和基本信息 */}
            <Grid size={{ xs: 12, md: 4 }}>
              <Box sx={{ textAlign: 'center' }}>
                <Avatar
                  alt={tenantDetail?.name ?? ''}
                  src={tenantDetail?.icon}
                  sx={{
                    width: 120,
                    height: 120,
                    mx: 'auto',
                    mb: 2,
                    boxShadow: 2,
                    border: '4px solid',
                    borderColor: 'primary.main'
                  }}
                />
                <Typography variant="h5" component="h2" gutterBottom sx={{ fontWeight: 'bold' }}>
                  {tenantDetail?.name ?? '未知租户'}
                </Typography>
                {tenantDetail?.isActive ?
                  (<Chip
                    icon={<CheckCircleIcon />}
                    label={t("common.isActive")}
                    color="success"
                    variant="outlined"
                    sx={{ mb: 2 }}
                  />
                  ) : (
                    <Chip
                      icon={<CancelIcon />}
                      label={t("common.isNotActive")}
                      variant="outlined"
                      sx={{ mb: 2 }}
                    />

                  )}
              </Box>
            </Grid>

            {/* 详细信息 */}
            <Grid size={{ xs: 12, md: 8 }}>
              <Stack spacing={3}>
                {/* 域名信息 */}
                <Paper elevation={1} sx={{ p: 3, borderRadius: 2 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <LanguageIcon color="primary" sx={{ mr: 1 }} />
                    <Typography variant="h6" color="primary.main" sx={{ fontWeight: 'bold' }}>
                      {t('setting.tenant.domain')}
                    </Typography>
                  </Box>
                  <Typography variant="body1" sx={{ fontFamily: 'monospace', fontSize: '1.1rem' }}>
                    {String(tenantDetail?.domain ?? '未设置')}
                  </Typography>
                </Paper>

                {/* 限制信息 */}
                <Grid container spacing={2}>
                  <Grid size={{ xs: 12, sm: 6 }}>
                    <Paper elevation={1} sx={{ p: 3, borderRadius: 2, height: '100%' }}>
                      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                        <WorkflowIcon color="secondary" sx={{ mr: 1 }} />
                        <Typography variant="h6" color="secondary.main" sx={{ fontWeight: 'bold' }}>
                          {t('setting.tenant.workflowLimit')}
                        </Typography>
                      </Box>
                      <Typography variant="h4" sx={{ fontWeight: 'bold', color: 'text.primary' }}>
                        {tenantDetail?.workflowLimit === 0 ? (
                          <Chip label={t('setting.tenant.unLimited')} color="success" size="small" />
                        ) : (
                          String(tenantDetail?.workflowLimit || 0)
                        )}
                      </Typography>
                    </Paper>
                  </Grid>

                  <Grid size={{ xs: 12, sm: 6 }}>
                    <Paper elevation={1} sx={{ p: 3, borderRadius: 2, height: '100%' }}>
                      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                        <AssignmentIcon color="info" sx={{ mr: 1 }} />
                        <Typography variant="h6" color="info.main" sx={{ fontWeight: 'bold' }}>
                          {t('setting.tenant.ticketLimit')}
                        </Typography>
                      </Box>
                      <Typography variant="h4" sx={{ fontWeight: 'bold', color: 'text.primary' }}>
                        {tenantDetail?.ticketLimit === 0 ? (
                          <Chip label={t('setting.tenant.unLimited')} color="success" size="small" />
                        ) : (
                          String(tenantDetail?.ticketLimit || 0)
                        )}
                      </Typography>
                    </Paper>
                  </Grid>
                </Grid>
              </Stack>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* 额外信息卡片 */}
      <Card sx={{ boxShadow: 2, borderRadius: 2 }}>
        <CardContent sx={{ p: 3 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <InfoIcon color="primary" sx={{ mr: 1 }} />
            <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
              {t("setting.tenant.tenantDetail")}
            </Typography>
          </Box>
          <Divider sx={{ mb: 2 }} />
          <Grid container spacing={3}>
            <Grid size={{ xs: 12, sm: 6 }}>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                {t("setting.tenant.tenantId")}
              </Typography>
              <Typography variant="body1" sx={{ fontFamily: 'monospace' }}>
                {String(tenantDetail?.id ?? '未知')}
              </Typography>
            </Grid>
            <Grid size={{ xs: 12, sm: 6 }}>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                {t("common.createdAt")}
              </Typography>
              <Typography variant="body1">
                {tenantDetail?.createdAt ? new Date(tenantDetail.createdAt).toLocaleString('zh-CN') : '未知'}
              </Typography>
            </Grid>
            <Grid size={{ xs: 12, sm: 6 }}>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                {t("common.updatedAt")}
              </Typography>
              <Typography variant="body1">
                {tenantDetail?.updatedAt ? new Date(tenantDetail.updatedAt).toLocaleString('zh-CN') : '未知'}
              </Typography>
            </Grid>
          </Grid>
        </CardContent>
      </Card>
    </Container>
  );
}

export default Tenant;

