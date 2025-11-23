import React from 'react';

// UI Components from design.txt

export const Card = ({ children, className = "" }) => (
    <div className={`bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden ${className}`}>
        {children}
    </div>
);

export const Badge = ({ children, color = "blue" }) => {
    const colors = {
        blue: "bg-blue-100 text-blue-700",
        green: "bg-emerald-100 text-emerald-700",
        amber: "bg-amber-100 text-amber-700",
        red: "bg-rose-100 text-rose-700",
    };
    return (
        <span className={`px-2.5 py-0.5 rounded-full text-xs font-medium ${colors[color] || colors.blue}`}>
            {children}
        </span>
    );
};

export const ProgressBar = ({ progress, color = "bg-blue-600" }) => (
    <div className="w-full bg-slate-100 rounded-full h-2.5 mb-1">
        <div
            className={`${color} h-2.5 rounded-full transition-all duration-300 ease-out`}
            style={{ width: `${progress}%` }}
        ></div>
    </div>
);

export const StatCard = ({ title, value, subtext, icon: Icon, color }) => (
    <Card className="p-5 flex items-start justify-between">
        <div>
            <p className="text-slate-500 text-sm font-medium mb-1">{title}</p>
            <h3 className="text-2xl font-bold text-slate-900">{value}</h3>
            <p className="text-slate-400 text-xs mt-1">{subtext}</p>
        </div>
        <div className={`p-3 rounded-lg ${color}`}>
            <Icon className="w-5 h-5 text-white" />
        </div>
    </Card>
);
