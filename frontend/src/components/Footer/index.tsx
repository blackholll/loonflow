import React from 'react';
import { GithubOutlined } from '@ant-design/icons';
import { DefaultFooter } from '@ant-design/pro-layout';

export default () => (
  <DefaultFooter
    copyright="2020 loonflow"
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
