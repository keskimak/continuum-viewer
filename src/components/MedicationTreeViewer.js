import { useState, useEffect } from 'react';
import './MedicationTreeView.css'; // <-- Import the CSS

function MedicationTreeView() {
    const [data, setData] = useState(null);
    const [expandedMedicines, setExpandedMedicines] = useState({});
    const [expandedParts, setExpandedParts] = useState({});

    useEffect(() => {
        fetch('http://localhost:5000/api/medication-history')
            .then(response => response.json())
            .then(json => setData(json))
            .catch(error => console.error('Error fetching data:', error));
    }, []);

    if (!data) {
        return <div>Loading...</div>;
    }

    const { medicine_id, patient_id } = data;

    const toggleMedicine = (medId) => {
        setExpandedMedicines(prev => ({
            ...prev,
            [medId]: !prev[medId]
        }));
    };

    const togglePart = (medId, partId) => {
        const key = `${medId}_${partId}`;
        setExpandedParts(prev => ({
            ...prev,
            [key]: !prev[key]
        }));
    };

    return (
        <div className="medication-tree-container">
            <h2 className="patient-id">Patient ID: {patient_id}</h2>

            <div>
                {Object.entries(medicine_id).map(([medId, medData]) => (
                    <div key={medId} className="medicine-section">
                        <button onClick={() => toggleMedicine(medId)} className="medicine-button">
                            {expandedMedicines[medId] ? '🔽' : '▶️'} Medicine ID: {medId}
                        </button>

                        {expandedMedicines[medId] && (
                            <div className="medicine-details">
                                {Object.entries(medData.medicine_id_part).map(([partId, requests]) => (
                                    <div key={partId} className="part-section">
                                        <button onClick={() => togglePart(medId, partId)} className="part-button">
                                            {expandedParts[`${medId}_${partId}`] ? '🔽' : '▶️'} Medicine ID Part: {partId}
                                        </button>

                                        {expandedParts[`${medId}_${partId}`] && (
                                            <div className="requests-list">
                                                {requests.map((request, index) => (
                                                    <div key={index} className="request-card">
                                                        <p><strong>ID:</strong> {request.id}</p>
                                                        <p><strong>Authored On:</strong> {request.authored_on || "Not available"}</p>
                                                        <p><strong>Indications:</strong> {request.indications?.length ? request.indications.map((i, idx) => (
                                                            <span key={idx}>{i.code} ({i.system}) </span>
                                                        )) : "None"}</p>
                                                        <p><strong>Adverse Effects:</strong> {request.adverse_effects?.length ? request.adverse_effects.join(", ") : "None"}</p>
                                                    </div>
                                                ))}
                                            </div>
                                        )}
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
}

export default MedicationTreeView;
