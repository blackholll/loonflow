import React, { useEffect, useState } from 'react';
import { Container, Typography, Avatar, Card, CardContent } from '@mui/material';
import Grid from '@mui/material/Grid2';
import { getTenantDetail } from '../../../services/tenant';
import { ITenantDetailResEntity } from '@/types/tenant';
import useSnackbar from '../../../hooks/useSnackbar';
import { useSelector } from 'react-redux';
import { RootState } from '../../../store';
import { useTranslation } from 'react-i18next';

function Tenant() {
  const [tenantDetail, setTenantDetail] = useState<ITenantDetailResEntity | null>(null);
  const { showMessage } = useSnackbar();
  const tenantId = useSelector((state: RootState) => state.auth.user?.tenantId ?? '');
  const { t } = useTranslation();

  useEffect(() => {
    const fetchTenantInfo = async () => {
      try {

        const res = await getTenantDetail(tenantId);
        if (res.code === 0) {
          setTenantDetail(res.data.tenantInfo);
        } else {
          showMessage(res.msg, 'error');
        }
      } catch (error: any) {
        showMessage(error.message, 'error');
      }
    };
    fetchTenantInfo();
  }, []);

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Grid container spacing={2} alignItems="center">
        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Avatar alt={tenantDetail?.name ?? ''} src={tenantDetail?.icon} sx={{ width: 100, height: 100 }} />
        </Grid>
        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Grid sx={{ marginBottom: 2 }}>
            <Typography sx={{ color: 'gray' }}>{t('setting.tenant.name')}:</Typography>
            <Typography>{tenantDetail?.name ?? ''}</Typography>
          </Grid>
          <Grid sx={{ marginBottom: 2 }}>
            <Typography sx={{ color: 'gray' }}>{t('setting.tenant.domain')}:</Typography>
            <Typography>{tenantDetail?.domain ?? ''}</Typography>
          </Grid>
          <Grid sx={{ marginBottom: 2 }}>
            <Typography sx={{ color: 'gray' }}>{t('setting.tenant.workflowLimit')}:</Typography>
            <Typography>{tenantDetail?.workflowLimit === 0 ? t('setting.tenant.unLimited') : tenantDetail?.workflowLimit}</Typography>
          </Grid>
          <Grid sx={{ marginBottom: 2 }}>
            <Typography sx={{ color: 'gray' }}>{t('setting.tenant.ticketLimit')}:</Typography>
            <Typography>{tenantDetail?.ticketLimit === 0 ? t('setting.tenant.unLimited') : tenantDetail?.ticketLimit}</Typography>
          </Grid>

        </Grid>
      </Grid>
    </Container>
  );
}

export default Tenant;

