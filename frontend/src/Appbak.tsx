import { BrowserRouter, Route, Routes } from 'react-router-dom';
import React, { ReactNode } from 'react';
import PrivateRoute from './utils/PrivateRoute';
import Layout from './components/layout';
import useMenuItems from './components/MenuItem';
import Home  from './components/home/HomePage' ;

const App = () => {
  const menuItems = useMenuItems();
  const routes: ReactNode[]= [];

  menuItems.forEach((item) => {
    // routes.push(<Route 
    //   key='/workflow' 
    //   path={item.path} 
    //   element={item.requireAuth ? <PrivateRoute element={item.component ? <item.component /> : null} /> : item.component ? <item.component /> : null}
    // />)
    if (item.isSingleLayout) {
      routes.push(
        <Route 
          key={item.path} 
          path={item.path} 
          element={item.requireAuth ? <PrivateRoute element={item.component ? <item.component /> : null} /> : item.component ? <item.component /> : null}
        />
      );
    } else {
      const layoutRoute = (
        <Route key={item.path} element={<Layout children={item.component ? <item.component /> : null} />}>
          {item.children?.map((child) => (
            <Route
              key={child.path}
              path={child.path}
              element={child.requireAuth ? <PrivateRoute element={child.component ? <child.component /> : null} /> : child.component ? <child.component /> : null}
            />
          ))}
        </Route>
      );
      routes.push(layoutRoute);
    }
  });

  console.log('生成的路由配置:', routes); // 打印最终生成的路由
  routes.map((child:any)=>{
    console.log('childelement:',child.props.element);
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
