import React from 'react';
import OriginalLayout from '@theme-original/Layout';
import ChatInterface from '../components/ChatInterface';

const Layout = (props) => {
  return (
    <>
      <OriginalLayout {...props}>
        {props.children}
      </OriginalLayout>
      <ChatInterface />
    </>
  );
};

export default Layout;