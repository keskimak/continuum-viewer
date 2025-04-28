import { useEffect, useState } from 'react';

const MedicationTreeViewer = () => {
    const [data, setData] = useState(null);
    const [medicineObjects, setMedicineObjects] = useState({});
    const [medicineIdPartObjects, setMedicineIdPartObjects] = useState({});
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        // Fetch data from your API
        const fetchData = async () => {
            try {
                const response = await fetch('http://localhost:5000/api/medication-history'); // <-- Your API URL
                const result = await response.json();
                setData(result);
            } catch (error) {
                console.error('Error fetching medication data:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    useEffect(() => {
        if (data?.medicine_id) {
            const medObjs = {};
            const medPartObjs = {};

            Object.entries(data.medicine_id).forEach(([medicineId, medData]) => {
                medObjs[medicineId] = {
                    atc_code: medData.atc_code,
                    atc_display: medData.atc_display
                };

                if (medData.medicine_id_part) {
                    Object.entries(medData.medicine_id_part).forEach(([partId, requests]) => {
                        if (!medPartObjs[medicineId]) {
                            medPartObjs[medicineId] = {};
                        }
                        medPartObjs[medicineId][partId] = requests;
                    });
                }
            });

            setMedicineObjects(medObjs);
            setMedicineIdPartObjects(medPartObjs);
        }
    }, [data]);

    if (loading) {
        return <div>Loading medications...</div>;
    }

    if (!data) {
        return <div>No medication data found.</div>;
    }

    return (
        <div className="medication-list">
            {Object.entries(medicineObjects).map(([medicineId, medInfo]) => (
                <div key={medicineId} className="medicine-item">
                    <div className="medication-details">
                        <span>ATC Code: {medInfo.atc_code}</span>
                        <span>ATC Name: {medInfo.atc_display}</span>
                    </div>

                    {medicineIdPartObjects[medicineId] && (
                        Object.entries(medicineIdPartObjects[medicineId]).map(([partId, requests]) => (
                            <div key={partId}>
                                <strong>Part ID: {partId}</strong>
                                {requests.map((request, index) => (
                                    <div key={index} className="request-info">
                                        <span>MedicationRequest ID: {request.id ? request.id : 'N/A'}</span>
                                        <span>Authored On: {request.authoredOn ? request.authoredOn : 'N/A'}</span>
                                        <span>Dosage Text: {request.dosageInstruction?.[0]?.text ? request.dosageInstruction?.[0]?.text : 'N/A'}</span>
                                    </div>
                                ))}
                            </div>
                        ))
                    )}
                </div>
            ))}
        </div>
    );
}

export default MedicationTreeViewer;    
