import React from 'react';
import { GithubOutlined } from '@ant-design/icons';
import { DefaultFooter } from '@ant-design/pro-layout';

export default () => (
  <DefaultFooter
    copyright="2018-2021 loonflow 2.0.5"
    links={[

      {
        key: 'github',
        title: <GithubOutlined />,
        href: 'https://github.com/blackholll/loonflow',
        blankTarget: true,
      },

    ]}
  />
);
