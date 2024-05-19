import { GithubOutlined } from '@ant-design/icons';
import { DefaultFooter } from '@ant-design/pro-layout';

export default () => (
  <DefaultFooter
    copyright="2018-2024 loonflow 3.0.0"
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
