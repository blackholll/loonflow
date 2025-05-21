import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Link from '@mui/material/Link';
import Box from '@mui/material/Box';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { login } from './services/authService';
import { setCookie } from './utils/cookie';
import { getJwtExpiration } from './utils/jwt';
import { loginState } from './store'
import { useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { getMyProfile } from './services/user';


function Copyright(props: any) {
  return (
    <Typography variant="body2" color="text.secondary" align="center" {...props}>
      {'Copyright © '}
      <Link color="inherit" href="https://wwww.loonapp.com/">
        loonflow
      </Link>{' '}
      {'2018-' + new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}


const defaultTheme = createTheme();

export default function SignIn() {
  const { t, i18n } = useTranslation();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleSubmit = async () => {
    try {
      const responseData = await login(email, password);
      const token = responseData.data.jwt;
      const expiration = getJwtExpiration(token);
      setCookie('jwtToken', token, {
        sameSite: 'strict',
        expires: expiration,
      });

      dispatch(loginState(token));
      try {
        const userProfileResponse = await getMyProfile();
        if (userProfileResponse.code === 0 && userProfileResponse.data.myProfile.lang) {
          const userLang = userProfileResponse.data.myProfile.lang;
          const localStorageLang = localStorage.getItem('i18nextLng');

          if (localStorageLang !== userLang) {
            i18n.changeLanguage(userLang);
          }
        }
      } catch (profileError) {
        console.error('get userprofile fail:', profileError);
      }

      navigate('/');
    } catch (error) {
      console.error('login fail:', error);
    }
  };

  return (
    <ThemeProvider theme={defaultTheme}>
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Box
          sx={{
            marginTop: 8,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
              <LockOutlinedIcon />
            </Avatar>
            <Typography variant="h5" sx={{ ml: 2 }}>
              {t('signIn.title')}
            </Typography>
          </Box>
          <Typography variant="body2" sx={{ textAlign: 'center', mt: 2, maxWidth: '100%' }}>
            {t('signIn.description')}
          </Typography>
          <Box component="form" noValidate sx={{ mt: 1 }}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="email"
              label={t('signIn.emailLabel')}
              name="email"
              autoComplete="email"
              autoFocus
              onChange={(e) => setEmail(e.target.value)}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label={t('signIn.passwordLabel')}
              type="password"
              id="password"
              autoComplete="current-password"
              onChange={(e) => setPassword(e.target.value)}
            />
            <Button

              fullWidth
              onClick={handleSubmit}
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              {t('signIn.signInButton')}
            </Button>
          </Box>
        </Box>
        <Copyright sx={{ mt: 8, mb: 4 }} />
      </Container>
    </ThemeProvider>
  );
}