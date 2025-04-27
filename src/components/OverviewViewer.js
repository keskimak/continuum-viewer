import React, { useState, useEffect } from 'react';
import './DataViewer.css';

const OverviewViewer = () => {
    const [data, setData] = useState(null);
    const [showIndications, setShowIndications] = useState(false);
    const [showAdverseEffects, setShowAdverseEffects] = useState(false);

    useEffect(() => {
        fetch('http://localhost:5000/api/medication-history')
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
            <h1>Medication History</h1>
            <div className="medication-list">
                {data.map((medicationlist) => (
                    <div key={medicationlist.medicine_id} className="medication-item">
                        <div className="medication-item">
                            <span className="detail-label">Date:</span>
                            <span className="detail-value">{medicationlist.medicine_id}</span>
                            {medicationlist.continuums.map((continuum) => (
                                <div key={continuum.medicine_id_part} className="medication-item">
                                </div>
                            ))}
                        </div>

                    </div>
                ))}
            </div>
        </div>
    );
};

export default OverviewViewer; 