import { useState } from 'react';
import ChatInterface from './components/ChatInterface';
import PatientSummaryCard from './components/PatientSummaryCard';
import WardBadge from './components/WardBadge';

function App() {
  const [sessionId] = useState(() => crypto.randomUUID()); // unique per browser tab
  const [patientData, setPatientData] = useState({
    name: '',
    age: '',
    query: '',
    ward: '',
    collected: false,
  });

  const updatePatient = (newData) => {
    setPatientData(prev => ({ ...prev, ...newData }));
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center p-4">
      {/* Header */}
      <h1 className="text-3xl font-bold text-blue-700 mb-4">
        🏥 AI Hospital Receptionist
      </h1>

      {/* Ward Badge (appears once ward is known) */}
      {patientData.ward && <WardBadge ward={patientData.ward} />}

      {/* Patient Summary Card (appears when all data collected) */}
      {patientData.collected && (
        <PatientSummaryCard
          name={patientData.name}
          age={patientData.age}
          query={patientData.query}
          ward={patientData.ward}
        />
      )}

      {/* Chat Interface */}
      <ChatInterface sessionId={sessionId} onUpdatePatient={updatePatient} />
    </div>
  );
}

export default App;