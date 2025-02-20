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
  const [tenantDetail, setTenantDetail] = useState<ITenantDetailResEntity|null>(null);
  const { showMessage } = useSnackbar();
  const tenantId = useSelector((state:RootState)=>state.auth.user?.tenant_id??'');
  const { t } = useTranslation();
  
  useEffect(() => {
    const fetchTenantInfo = async () => {
      try {
        
        const res = await getTenantDetail(tenantId);
        if (res.code === 0){
          setTenantDetail(res.data.tenant_info);
        } else {
          showMessage( res.msg, 'error');
        }
      } catch (error:any) {
       showMessage( error.message, 'error');
      }
    };
    fetchTenantInfo();
  }, []);

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Grid container spacing={2} alignItems="center">
        <Grid size={{xs:12, sm:6, md:3}}>
          <Avatar alt={tenantDetail?.name??''} src={tenantDetail?.icon} sx={{ width: 100, height: 100 }} />
        </Grid>
        <Grid size={{xs:12, sm:6, md:3}}>
          <Grid sx={{marginBottom: 2}}>
          <Typography sx={{ color: 'gray'}}>{t('settings.tenant.name')}:</Typography>
          <Typography>{tenantDetail?.name??''}</Typography>
          </Grid>
          <Grid sx={{marginBottom: 2}}>
            <Typography sx={{ color: 'gray'}}>{t('settings.tenant.domain')}:</Typography>
            <Typography>{tenantDetail?.domain??''}</Typography>
          </Grid>
          <Grid sx={{marginBottom: 2}}>
            <Typography sx={{ color: 'gray'}}>{t('settings.tenant.workflow_limit')}:</Typography>
            <Typography>{tenantDetail?.workflow_limit ===0? t('settings.tenant.un_limited'):tenantDetail?.workflow_limit}</Typography>
          </Grid>
          <Grid sx={{marginBottom: 2}}>
            <Typography sx={{ color: 'gray'}}>{t('settings.tenant.ticket_limit')}:</Typography>
            <Typography>{tenantDetail?.ticket_limit === 0? t('settings.tenant.un_limited'):tenantDetail?.ticket_limit}</Typography>
          </Grid>
          
        </Grid>
      </Grid>
    </Container>
  );
}

export default Tenant;

