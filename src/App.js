import React from 'react';
import './App.css';
import MedicationsViewer from './components/MedicationsViewer';
import OverviewViewer from './components/OverviewViewer';

function App() {
  return (
    <div className="App">
      {/* <MedicationsViewer /> */}
      <OverviewViewer />
    </div>
  );
}

export default App;
