import React, { useState, useEffect } from 'react';
import './DataViewer.css';

const DataViewer = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            const response = await fetch('/sample_data.json');
            if (!response.ok) {
                throw new Error('Failed to fetch data');
            }
            const jsonData = await response.json();
            setData(jsonData);
            setLoading(false);
        } catch (err) {
            setError(err.message);
            setLoading(false);
        }
    };

    if (loading) return <div className="loading">Loading...</div>;
    if (error) return <div className="error">Error: {error}</div>;
    if (!data) return <div className="no-data">No data available</div>;

    return (
        <div className="data-viewer">
            <h1>Project Dashboard</h1>
            <div className="metadata">
                <h2>Metadata</h2>
                <p>Version: {data.metadata.version}</p>
                <p>Last Sync: {new Date(data.metadata.lastSync).toLocaleString()}</p>
                <p>Total Projects: {data.metadata.totalProjects}</p>
            </div>
            <div className="projects">
                <h2>Projects</h2>
                <div className="project-grid">
                    {data.items.map((project) => (
                        <div key={project.id} className="project-card">
                            <h3>{project.name}</h3>
                            <div className="project-status">
                                <span className={`status ${project.status.toLowerCase()}`}>
                                    {project.status}
                                </span>
                                <div className="progress-bar">
                                    <div
                                        className="progress"
                                        style={{ width: `${project.progress}%` }}
                                    />
                                </div>
                            </div>
                            <div className="team-members">
                                <h4>Team Members:</h4>
                                <ul>
                                    {project.team.map((member, index) => (
                                        <li key={index}>{member}</li>
                                    ))}
                                </ul>
                            </div>
                            <p className="last-updated">
                                Last Updated: {project.lastUpdated}
                            </p>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default DataViewer; 