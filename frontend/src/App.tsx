import { BrowserRouter, Route, Routes } from 'react-router-dom';
import React, { ReactNode } from 'react';
import PrivateRoute from './utils/PrivateRoute';
import SnackbarProvider from './components/commonComponents/Snackbar/SnackbarProvider';
import { useTranslation } from 'react-i18next';

import Layout from './components/layout';
import useMenuItems from './components/MenuItem';
import Home from './components/home/HomePage';
import SignIn from './SignIn';
import Home2 from './components/home2/HomePage';
import Workbench from './components/Workbench'
import DutyTicket from './components/Ticket/DutyTicket';
import OwerTicket from './components/Ticket/OwnerTicket';
import RelationTicket from './components/Ticket/RelationTicket';
import ViewTicket from './components/Ticket/ViewTicket';
import InterveneTicket from './components/Ticket/InterveneTicket';
import AllTicket from './components/Ticket/AllTicket';
import Tenant from './components/Setting/Tenant';
import {ApplicationList} from './components/Setting/Application';
import { NotificationList } from './components/Setting/Notification';


const App = () => {
  const routes: ReactNode[] = [
    <Route
      key={'signin'}
      path={'signIn'}
      element={< SignIn />}
    />,
    <Route
      key={'root'}
      path={'/'}
      element={<PrivateRoute element={<Layout children={<Workbench />} />} />}

    />,
    <Route
      key={'home'}
      path={'home'}
      element={<PrivateRoute element={<Layout children={<Workbench />} />} />}

    />,
    <Route
      key={'ticketManagement'}
      path={'/ticket'}
    >
      <Route key={'ticketDuty'}
        path={'/ticket/duty'}
        element={<PrivateRoute element={<Layout children={<DutyTicket />} />} />}
      />
      <Route key={'ticketOwner'}
        path={'/ticket/owner'}
        element={<PrivateRoute element={<Layout children={<OwerTicket />} />} />}
      />
      <Route key={'ticketRelation'}
        path={'/ticket/relation'}
        element={<PrivateRoute element={<Layout children={<RelationTicket />} />} />}
      />
      <Route key={'ticketView'}
        path={'/ticket/view'}
        element={<PrivateRoute element={<Layout children={<ViewTicket />} />} />}
      />
      <Route key={'ticketIntervene'}
        path={'/ticket/intervene'}
        element={<PrivateRoute element={<Layout children={<InterveneTicket />} />} />}
      />
      <Route key={'ticketAll'}
        path={'/ticket/all'}
        element={<PrivateRoute element={<Layout children={<AllTicket />} />} />}
      />
    </Route>,
    <Route
      key={'workflow'}
      path={'/workflow'}
      element={<PrivateRoute element={<Layout children={<Home />} />} />}
    />,
    <Route
      key={'organization'}
      path={'/organization'}
    >
      <Route key={'userAndDept'}
        path={'/organization/userdept'}
        element={<PrivateRoute element={<Layout children={<Home />} />} />}
      />
      <Route key={'role'}
        path={'/organization/role'}
        element={<PrivateRoute element={<Layout children={<Home />} />} />}
      />
    </Route>,
    <Route
    key={'setting'}
    path={'/setting'}
   >
    <Route key={'tenant'}
      path={'/setting/tenant'}
      element={<PrivateRoute element={<Layout children={<Tenant />} />} />}
    />
    <Route key={'application'}
      path={'/setting/application'}
      element={<PrivateRoute element={<Layout children={<ApplicationList />} />} />}
    />
    <Route key={'notification'}
      path={'/setting/notification'}
      element={<PrivateRoute element={<Layout children={<NotificationList />} />} />}
    />
    </Route>  
  ];



  console.log('生成的路由配置:', routes); // 打印最终生成的路由
  routes.map((child: any) => {
    console.log('childelement:', child.props.element);
  })


  return (
  <SnackbarProvider>
    <div className="App">
      <BrowserRouter>
        <Routes>
          {routes}
        </Routes>
      </BrowserRouter>
    </div>
    </SnackbarProvider>
  );
};

export default App;
