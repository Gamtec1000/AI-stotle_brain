import React from 'react';
import AristotleWidget from './components/AristotleWidget';

function App() {
  return (
    <AristotleWidget
      apiUrl="http://localhost:8000"
      studentAge={10}
      theme="dark"
      position="bottom-right"
    />
  );
}

export default App;
