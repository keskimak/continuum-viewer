import React, { useState, useEffect } from 'react';
import './DataViewer.css';

const MedicationsViewer = () => {
    const [data, setData] = useState(null);
    const [showIndications, setShowIndications] = useState(false);
    const [showAdverseEffects, setShowAdverseEffects] = useState(false);

    useEffect(() => {
        fetch('http://localhost:5000/api/medications')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                setData(data);
                console.log(data);
            })
            .catch(error => console.error('Error fetching medications:', error));
    }, []);


    if (!data) return <div className="no-data">No data available</div>;

    return (
        <div className="data-viewer">
            <h1>Project Dashboard</h1>
            <div className="medication-list">
                {data.map((medication) => (
                    <div key={medication.id} className="medication-item">
                        <div className="medication-details">
                            <div className="detail-row">
                                <span className="detail-label">Date:</span>
                                <span className="detail-value">{medication.authored_on}</span>
                            </div>
                            <div className="detail-row">
                                <span className="detail-label">ATC Code:</span>
                                <span className="detail-value">{medication.medication.atc.display}</span>
                            </div>
                            <div className="detail-row">
                                <span className="detail-label">Strength:</span>
                                <span className="detail-value">{medication.medication.strength}</span>
                            </div>
                        </div>

                        {showIndications && (
                            <div className="detail-section">
                                <h3>Indications</h3>
                                <ul>
                                    {medication.indications.map((indication, index) => (
                                        <li key={`indication-${medication.id}-${index}`}>
                                            {indication.code} {indication.display}
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        )}

                        {showAdverseEffects && (
                            <div className="detail-section">
                                <h3>Adverse Effects</h3>
                                <ul>
                                    {medication.adverse_effects.map((effect, index) => (
                                        <li key={`effect-${medication.id}-${index}`}>
                                            {effect.code} {effect.display}
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        )}
                    </div>
                ))}
            </div>

            <div className="action-buttons">
                <button
                    className={`action-button ${showIndications ? 'active' : ''}`}
                    onClick={() => setShowIndications(!showIndications)}
                >
                    {showIndications ? 'Hide Indications' : 'Show All Indications'}
                </button>
                <button
                    className={`action-button ${showAdverseEffects ? 'active' : ''}`}
                    onClick={() => setShowAdverseEffects(!showAdverseEffects)}
                >
                    {showAdverseEffects ? 'Hide Adverse Effects' : 'Show All Adverse Effects'}
                </button>
            </div>
        </div>
    );
};

export default MedicationsViewer; 