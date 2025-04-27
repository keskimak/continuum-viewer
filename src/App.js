import React from 'react';
import './App.css';
import MedicationTreeView from './components/MedicationTreeViewer';
function App() {
  return (
    <div className="App">
      {/* <MedicationsViewer /> */}

      {/* <MedicationList /> */}
      <MedicationTreeView />
    </div>
  );
}

export default App;
