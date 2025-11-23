// API Client with mock data fallbacks

const API_BASE = '/api';

// Mock data generators
const generateMockFiles = (count, type = 'file') => {
    const fileTypes = ['PDF', 'MP4', 'ZIP', 'MOV', 'JPG', 'ISO'];
    return Array.from({ length: count }, (_, i) => ({
        id: `file-${i}`,
        name: type === 'photo' ? `IMG_${20240000 + i}.JPG` : `Project_Backup_${i}.${fileTypes[i % fileTypes.length].toLowerCase()}`,
        size: Math.floor(Math.random() * 500000000) + 10000000,
        size_fmt: `${Math.floor(Math.random() * 500) + 10} MB`,
        path: type === 'photo' ? '/Google Photos/2024' : '/My Drive/Work/Projects',
        type: fileTypes[i % fileTypes.length],
        modified: new Date(Date.now() - Math.random() * 365 * 24 * 60 * 60 * 1000).toISOString(),
        link: '#',
        ...(type === 'photo' && {
            filename: `IMG_${20240000 + i}.JPG`,
            dimensions: `${Math.floor(Math.random() * 2000) + 1920}x${Math.floor(Math.random() * 2000) + 1080}`,
            created: new Date(Date.now() - Math.random() * 365 * 24 * 60 * 60 * 1000).toISOString(),
            url: '#'
        })
    }));
};

const generateMockDuplicates = (count, type = 'file') => {
    return Array.from({ length: count }, (_, i) => ({
        id: `dup-group-${i}`,
        name: type === 'photo' ? `Vacation_Hawaii_${i}.JPG` : `Q3_Report_Final_${i}.pdf`,
        size: 15400000,
        size_fmt: '15.4 MB',
        count: Math.floor(Math.random() * 3) + 2,
        files: Array.from({ length: Math.floor(Math.random() * 3) + 2 }, (_, j) => ({
            path: `/Path/To/Copy_${j + 1}/${type === 'photo' ? `Vacation_Hawaii_${i}.JPG` : `Q3_Report_Final_${i}.pdf`}`,
            modified: new Date(Date.now() - Math.random() * 365 * 24 * 60 * 60 * 1000).toISOString(),
            ...(type === 'photo' && {
                dimensions: '1920x1080',
                created: new Date(Date.now() - Math.random() * 365 * 24 * 60 * 60 * 1000).toISOString(),
                url: '#'
            })
        }))
    }));
};

// API functions with fallbacks
export const api = {
    async getStats() {
        try {
            const response = await fetch(`${API_BASE}/stats`);
            if (!response.ok) throw new Error('API not available');
            return await response.json();
        } catch (error) {
            console.warn('Using mock stats data:', error.message);
            return {
                drive: {
                    count: 452109,
                    size: '1.4 TB',
                    age: 'Today at 9:41 AM'
                },
                photos: {
                    count: 89201,
                    size: '245 GB',
                    age: 'Today at 9:41 AM'
                }
            };
        }
    },

    async getDriveLargest() {
        try {
            const response = await fetch(`${API_BASE}/drive/largest`);
            if (!response.ok) throw new Error('API not available');
            return await response.json();
        } catch (error) {
            console.warn('Using mock Drive largest files:', error.message);
            return generateMockFiles(100, 'file');
        }
    },

    async getDriveDuplicates() {
        try {
            const response = await fetch(`${API_BASE}/drive/duplicates`);
            if (!response.ok) throw new Error('API not available');
            return await response.json();
        } catch (error) {
            console.warn('Using mock Drive duplicates:', error.message);
            return generateMockDuplicates(5, 'file');
        }
    },

    async getPhotosLargest() {
        try {
            const response = await fetch(`${API_BASE}/photos/largest`);
            if (!response.ok) throw new Error('API not available');
            return await response.json();
        } catch (error) {
            console.warn('Using mock Photos largest items:', error.message);
            return generateMockFiles(100, 'photo');
        }
    },

    async getPhotosDuplicates() {
        try {
            const response = await fetch(`${API_BASE}/photos/duplicates`);
            if (!response.ok) throw new Error('API not available');
            return await response.json();
        } catch (error) {
            console.warn('Using mock Photos duplicates:', error.message);
            return generateMockDuplicates(5, 'photo');
        }
    }
};
