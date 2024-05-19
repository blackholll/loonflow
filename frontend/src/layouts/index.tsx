import { Dropdown, message } from 'antd';
import Cookies from 'js-cookie';
import { history } from 'umi';
import { LogoutOutlined } from '@ant-design/icons';
import { ProLayout } from '@ant-design/pro-layout';
import { Link, Outlet, useAppData, useLocation } from 'umi';
import Footer from '@/components/Footer';
import Login from '@/pages/User/Login';

export default function Layout() {
  const { clientRoutes } = useAppData();
  const location = useLocation();
  console.log('clientRoutes:', clientRoutes);
  console.log('location:', location);
  const isLoginPage = location.pathname === '/user/login';

  const handleLogout = () => {
    Cookies.remove('jwt');
    message.success('Logout successfully');
    history.push('/user/login');
  };


  return isLoginPage? (
      <Login/>
    ): (<ProLayout
      route={clientRoutes[0]}
      location={location}
      title="Loonflow"
      layout="mix"
      avatarProps={{
        src: 'default_avator.png',
        size: 'small',
        title: 'admin',
        render: (props, dom) => {
          return (
            <Dropdown
              menu={{
                items: [
                  {
                    key: 'logout',
                    icon: <LogoutOutlined />,
                    label: 'logout',
                    onClick: handleLogout,
                  },
                ],
              }}
            >
              {dom}
            </Dropdown>
          );
        },
      }}
      
      menuItemRender={(menuItemProps, defaultDom) => {
        if (menuItemProps.isUrl || menuItemProps.children) {
          return defaultDom;
        }
        if (menuItemProps.path && location.pathname !== menuItemProps.path) {
          return (
            <Link to={menuItemProps.path} target={menuItemProps.target}>
              {defaultDom}
            </Link>
          );
        }
        return defaultDom;
      }}
    >
      <Outlet />
      <Footer />
      </ProLayout>
)}

