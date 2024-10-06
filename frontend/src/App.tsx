import { BrowserRouter, Route, Routes } from 'react-router-dom';
import React, { ReactNode } from 'react';
import PrivateRoute from './utils/PrivateRoute';


import Layout from './components/layout';
import useMenuItems from './components/MenuItem';
import Home from './components/home/HomePage';
import SignIn from './SignIn';
import Home2 from './components/home2/HomePage';

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
      element={<PrivateRoute element={<Layout children={<Home />} />} />}

    />,
    <Route
      key={'home'}
      path={'home'}
      element={<PrivateRoute element={<Layout children={<Home />} />} />}

    />,
    <Route
      key={'ticketManagement'}
      path={'/ticket'}
    >
      <Route key={'ticketDuty'}
        path={'/ticket/duty'}
        element={<PrivateRoute element={<Layout children={<Home />} />} />}
      />
      <Route key={'ticketOwner'}
        path={'/ticket/owner'}
        element={<PrivateRoute element={<Layout children={<Home2 />} />} />}
      />
      <Route key={'ticketRelation'}
        path={'/ticket/relation'}
        element={<PrivateRoute element={<Layout children={<Home />} />} />}
      />
      <Route key={'ticketView'}
        path={'/ticket/view'}
        element={<PrivateRoute element={<Layout children={<Home />} />} />}
      />
      <Route key={'ticketIntervene'}
        path={'/ticket/intervene'}
        element={<PrivateRoute element={<Layout children={<Home />} />} />}
      />
      <Route key={'ticketAll'}
        path={'/ticket/all'}
        element={<PrivateRoute element={<Layout children={<Home />} />} />}
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
    key={'settings'}
    path={'/settings'}
   >
    <Route key={'tenant'}
      path={'/settings/tenant'}
      element={<PrivateRoute element={<Layout children={<Home />} />} />}
    />
    <Route key={'app'}
      path={'/settings/app'}
      element={<PrivateRoute element={<Layout children={<Home />} />} />}
    />
    <Route key={'notice'}
      path={'/settings/notice'}
      element={<PrivateRoute element={<Layout children={<Home />} />} />}
    />
    </Route>  
  ];



  console.log('生成的路由配置:', routes); // 打印最终生成的路由
  routes.map((child: any) => {
    console.log('childelement:', child.props.element);
  })


  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          {routes}
        </Routes>
      </BrowserRouter>
    </div>
  );
};

export default App;
