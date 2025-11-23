import React, { useState, useEffect } from 'react';
import {
    HardDrive,
    Image as ImageIcon,
    FileText,
    Trash2,
    BarChart2,
    Settings,
    RefreshCw,
    Download,
    Folder,
    CheckCircle,
    File,
    Database,
    Zap
} from 'lucide-react';
import { api } from './api';
import { Card, Badge, ProgressBar, StatCard } from './components/UI';

export default function App() {
    const [activeTab, setActiveTab] = useState('drive');
    const [isScanning, setIsScanning] = useState(false);
    const [scanProgress, setScanProgress] = useState(0);
    const [scanResult, setScanResult] = useState(null);
    const [cachingEnabled, setCachingEnabled] = useState(true);
    const [showToast, setShowToast] = useState(false);
    const [toastMsg, setToastMsg] = useState('');
    const [stats, setStats] = useState(null);
    const [largestFiles, setLargestFiles] = useState([]);
    const [duplicates, setDuplicates] = useState([]);

    useEffect(() => {
        loadStats();
    }, []);

    const loadStats = async () => {
        const data = await api.getStats();
        setStats(data);
    };

    const startScan = async (type) => {
        if (isScanning) return;
        setIsScanning(true);
        setScanProgress(0);
        setScanResult(null);

        let progress = 0;
        const interval = setInterval(() => {
            progress += Math.floor(Math.random() * 15) + 5;
            if (progress >= 100) {
                progress = 100;
                clearInterval(interval);
            }
            setScanProgress(progress);
        }, 200);

        try {
            if (type === 'largest') {
                const data = activeTab === 'drive' ? await api.getDriveLargest() : await api.getPhotosLargest();
                setLargestFiles(data);
            } else if (type === 'duplicates') {
                const data = activeTab === 'drive' ? await api.getDriveDuplicates() : await api.getPhotosDuplicates();
                setDuplicates(data);
            }
        } catch (error) {
            console.error('Scan error:', error);
        } finally {
            clearInterval(interval);
            setScanProgress(100);
            setTimeout(() => {
                setIsScanning(false);
                setScanResult(type);
            }, 300);
        }
    };

    const handleExport = (format) => {
        setToastMsg(`Exporting results to ${format}...`);
        setShowToast(true);
        setTimeout(() => setShowToast(false), 3000);
    };

    return (
        <div className="min-h-screen bg-slate-50 text-slate-900 font-sans">
            {showToast && (
                <div className="fixed bottom-6 right-6 bg-slate-900 text-white px-6 py-3 rounded-lg shadow-xl z-50 flex items-center gap-3">
                    <CheckCircle className="w-5 h-5 text-emerald-400" />
                    <span>{toastMsg}</span>
                </div>
            )}

            <header className="bg-white border-b border-slate-200 sticky top-0 z-40">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between items-center h-16">
                        <div className="flex items-center gap-3">
                            <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg flex items-center justify-center text-white font-bold shadow-lg shadow-blue-500/30">
                                U
                            </div>
                            <span className="text-xl font-bold tracking-tight text-slate-900">
                                Drive<span className="text-blue-600">Utility</span>
                            </span>
                        </div>

                        <div className="flex items-center gap-6">
                            <div className="hidden md:flex items-center gap-2 cursor-pointer" onClick={() => setCachingEnabled(!cachingEnabled)}>
                                <div className={`w-8 h-4 rounded-full p-0.5 transition-colors duration-300 ${cachingEnabled ? 'bg-emerald-500' : 'bg-slate-300'}`}>
                                    <div className={`w-3 h-3 bg-white rounded-full shadow-sm transform transition-transform duration-300 ${cachingEnabled ? 'translate-x-4' : 'translate-x-0'}`} />
                                </div>
                                <div className="flex flex-col">
                                    <span className="text-xs font-bold text-slate-700">Smart Cache</span>
                                    <span className="text-[10px] text-slate-400 uppercase tracking-wider">{cachingEnabled ? 'Active' : 'Paused'}</span>
                                </div>
                            </div>
                            <div className="h-6 w-px bg-slate-200 hidden md:block"></div>
                            <div className="flex items-center gap-4">
                                <button className="p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-full transition-all">
                                    <Settings className="w-5 h-5" />
                                </button>
                                <div className="w-8 h-8 bg-indigo-100 rounded-full flex items-center justify-center text-indigo-700 font-bold text-sm border border-indigo-200">
                                    JD
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </header>

            <div className="bg-white border-b border-slate-200 shadow-sm">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex space-x-8 -mb-px">
                        <button
                            onClick={() => { setActiveTab('drive'); setScanResult(null); }}
                            className={`group inline-flex items-center py-4 px-1 border-b-2 font-medium text-sm transition-all ${activeTab === 'drive' ? 'border-blue-500 text-blue-600' : 'border-transparent text-slate-500 hover:text-slate-700'
                                }`}
                        >
                            <HardDrive className={`w-5 h-5 mr-2 ${activeTab === 'drive' ? 'text-blue-500' : 'text-slate-400'}`} />
                            Google Drive
                        </button>
                        <button
                            onClick={() => { setActiveTab('photos'); setScanResult(null); }}
                            className={`group inline-flex items-center py-4 px-1 border-b-2 font-medium text-sm transition-all ${activeTab === 'photos' ? 'border-pink-500 text-pink-600' : 'border-transparent text-slate-500 hover:text-slate-700'
                                }`}
                        >
                            <ImageIcon className={`w-5 h-5 mr-2 ${activeTab === 'photos' ? 'text-pink-500' : 'text-slate-400'}`} />
                            Google Photos
                        </button>
                    </div>
                </div>
            </div>

            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-slate-900">
                        {activeTab === 'drive' ? 'Drive Overview' : 'Photos Library'}
                    </h1>
                    <p className="text-slate-500 mt-2 flex items-center gap-2">
                        <RefreshCw className="w-4 h-4" />
                        Last analyzed: {activeTab === 'drive' ? (stats?.drive?.age || 'Loading...') : (stats?.photos?.age || 'Loading...')}
                        <span className="text-slate-300">•</span>
                        <span className="text-red-600 font-medium">
                            {activeTab === 'drive' ? '15 GB Free (MOCK)' : 'Unlimited High Quality (MOCK)'}
                        </span>
                    </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
                    <StatCard
                        title="Storage Used"
                        value={activeTab === 'drive' ? (stats?.drive?.size || '...') : (stats?.photos?.size || '...')}
                        subtext={activeTab === 'drive' ? 'Total Drive Usage' : 'Total Photos Usage'}
                        icon={Database}
                        color="bg-blue-500"
                    />
                    <StatCard
                        title={activeTab === 'drive' ? "Files Scanned" : "Photos Scanned"}
                        value={activeTab === 'drive' ? (stats?.drive?.count?.toLocaleString() || '...') : (stats?.photos?.count?.toLocaleString() || '...')}
                        subtext={`Last scan: ${activeTab === 'drive' ? (stats?.drive?.age || '...') : (stats?.photos?.age || '...')}`}
                        icon={activeTab === 'drive' ? FileText : ImageIcon}
                        color="bg-emerald-500"
                    />
                    <StatCard
                        title={<span className="flex items-center gap-2">Duplicate Space <span className="text-[10px] bg-red-100 text-red-600 px-1.5 py-0.5 rounded font-bold">MOCK</span></span>}
                        value={<span className="text-red-600">145 GB</span>}
                        subtext="Potential savings"
                        icon={Trash2}
                        color="bg-amber-500"
                    />
                    <StatCard
                        title={<span className="flex items-center gap-2">Largest Items <span className="text-[10px] bg-red-100 text-red-600 px-1.5 py-0.5 rounded font-bold">MOCK</span></span>}
                        value={<span className="text-red-600">500+</span>}
                        subtext="Files > 1GB"
                        icon={BarChart2}
                        color="bg-purple-500"
                    />
                </div>

                <div className="border-t border-slate-200 my-8"></div>

                <h2 className="text-lg font-bold text-slate-900 mb-4 flex items-center gap-2">
                    <Zap className="w-5 h-5 text-amber-500" />
                    Quick Actions
                </h2>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                    <Card className="p-6 hover:border-blue-300 transition-colors cursor-pointer group">
                        <div className="flex items-center justify-between mb-4">
                            <div className="p-3 bg-blue-50 rounded-lg group-hover:bg-blue-100 transition-colors">
                                <BarChart2 className="w-6 h-6 text-blue-600" />
                            </div>
                            <Badge color="blue">Analysis</Badge>
                        </div>
                        <h3 className="text-lg font-bold text-slate-800 mb-2">Find Largest Items</h3>
                        <p className="text-slate-500 text-sm mb-4">
                            Locate the top 100 files consuming the most space in your {activeTab === 'drive' ? 'Drive' : 'Library'}.
                        </p>
                        <button
                            onClick={() => startScan('largest')}
                            disabled={isScanning}
                            className="w-full py-2 bg-white border border-slate-300 text-slate-700 font-medium rounded-lg hover:bg-slate-50 transition-all disabled:opacity-50"
                        >
                            {isScanning ? 'Scanning...' : 'Analyze Size'}
                        </button>
                    </Card>

                    <Card className="p-6 hover:border-amber-300 transition-colors cursor-pointer group">
                        <div className="flex items-center justify-between mb-4">
                            <div className="p-3 bg-amber-50 rounded-lg group-hover:bg-amber-100 transition-colors">
                                <Trash2 className="w-6 h-6 text-amber-600" />
                            </div>
                            <Badge color="amber">Cleanup</Badge>
                        </div>
                        <h3 className="text-lg font-bold text-slate-800 mb-2">Detect Duplicates</h3>
                        <p className="text-slate-500 text-sm mb-4">
                            Find files with identical names and sizes across {activeTab === 'drive' ? 'folders' : 'albums'}.
                        </p>
                        <button
                            onClick={() => startScan('duplicates')}
                            disabled={isScanning}
                            className="w-full py-2 bg-white border border-slate-300 text-slate-700 font-medium rounded-lg hover:bg-slate-50 transition-all disabled:opacity-50"
                        >
                            {isScanning ? 'Scanning...' : 'Find Duplicates'}
                        </button>
                    </Card>

                    <Card className="p-6 hover:border-emerald-300 transition-colors cursor-pointer group">
                        <div className="flex items-center justify-between mb-4">
                            <div className="p-3 bg-emerald-50 rounded-lg group-hover:bg-emerald-100 transition-colors">
                                <Folder className="w-6 h-6 text-emerald-600" />
                            </div>
                            <Badge color="green">Export</Badge>
                        </div>
                        <h3 className="text-lg font-bold text-slate-800 mb-2">
                            {activeTab === 'drive' ? 'Export Tree' : 'Export Metadata'}
                        </h3>
                        <p className="text-slate-500 text-sm mb-4">
                            {activeTab === 'drive' ? 'Generate a CSV map of your entire folder structure.' : 'Export a JSON report of your photo metadata.'}
                        </p>
                        <div className="flex gap-2">
                            <button
                                onClick={() => handleExport('CSV')}
                                className="flex-1 py-2 bg-white border border-slate-300 text-slate-700 font-medium rounded-lg hover:bg-slate-50 flex items-center justify-center gap-2"
                            >
                                <Download className="w-4 h-4" /> CSV
                            </button>
                            <button
                                onClick={() => handleExport('JSON')}
                                className="flex-1 py-2 bg-white border border-slate-300 text-slate-700 font-medium rounded-lg hover:bg-slate-50 flex items-center justify-center gap-2"
                            >
                                <Download className="w-4 h-4" /> JSON
                            </button>
                        </div>
                    </Card>
                </div>

                {isScanning && (
                    <Card className="p-12 flex flex-col items-center justify-center text-center">
                        <div className="w-full max-w-md">
                            <div className="flex justify-between text-sm font-medium text-slate-600 mb-2">
                                <span>Analyzing metadata...</span>
                                <span>{scanProgress}%</span>
                            </div>
                            <ProgressBar progress={scanProgress} color={activeTab === 'drive' ? 'bg-blue-600' : 'bg-pink-600'} />
                            <p className="text-slate-400 text-sm mt-4">
                                Using smart cache for faster retrieval. Please wait.
                            </p>
                        </div>
                    </Card>
                )}

                {!isScanning && scanResult === 'largest' && (
                    <div>
                        <div className="flex items-center justify-between mb-4">
                            <h3 className="text-xl font-bold text-slate-800">Top Largest Files</h3>
                        </div>
                        <Card>
                            <table className="w-full text-left text-sm text-slate-600">
                                <thead className="bg-slate-50 text-slate-700 font-medium border-b border-slate-200">
                                    <tr>
                                        <th className="px-6 py-4">Name</th>
                                        <th className="px-6 py-4">Location</th>
                                        <th className="px-6 py-4">Type</th>
                                        <th className="px-6 py-4 text-right">Size</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-slate-100">
                                    {largestFiles.slice(0, 10).map((file, idx) => (
                                        <tr key={idx} className="hover:bg-slate-50 transition-colors">
                                            <td className="px-6 py-4 font-medium text-slate-900 flex items-center gap-3">
                                                {activeTab === 'drive' ? <File className="w-4 h-4 text-slate-400" /> : <ImageIcon className="w-4 h-4 text-purple-400" />}
                                                <span className="truncate max-w-xs">{file.name || file.filename}</span>
                                            </td>
                                            <td className="px-6 py-4 text-slate-500 truncate max-w-xs">{file.path || file.dimensions}</td>
                                            <td className="px-6 py-4"><Badge color="blue">{file.type || 'JPG'}</Badge></td>
                                            <td className="px-6 py-4 text-right font-mono text-slate-700">{file.size_fmt}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </Card>
                    </div>
                )}

                {!isScanning && scanResult === 'duplicates' && (
                    <div>
                        <div className="flex items-center justify-between mb-4">
                            <h3 className="text-xl font-bold text-slate-800">Duplicate Groups Found</h3>
                        </div>
                        <div className="space-y-4">
                            {duplicates.length === 0 ? (
                                <Card className="p-12 text-center">
                                    <CheckCircle className="w-12 h-12 text-emerald-500 mx-auto mb-4" />
                                    <h3 className="text-lg font-bold text-slate-900">No Duplicates Found</h3>
                                    <p className="text-slate-500">Your {activeTab === 'drive' ? 'drive' : 'library'} is clean!</p>
                                </Card>
                            ) : (
                                duplicates.map((group, idx) => (
                                    <Card key={idx} className="p-4 border-l-4 border-l-amber-400">
                                        <div className="flex items-center justify-between mb-3">
                                            <div className="flex items-center gap-3">
                                                <div className="p-2 bg-amber-50 rounded text-amber-600">
                                                    <Folder className="w-5 h-5" />
                                                </div>
                                                <div>
                                                    <h4 className="font-bold text-slate-800">{group.name}</h4>
                                                    <p className="text-xs text-slate-500">{group.count} copies found</p>
                                                </div>
                                            </div>
                                            <Badge color="red">Duplicate</Badge>
                                        </div>
                                    </Card>
                                ))
                            )}
                        </div>
                    </div>
                )}
            </main>
        </div>
    );
}
