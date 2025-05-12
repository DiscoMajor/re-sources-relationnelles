export async function fetchHealthFacilities(type = null) {
    try {
        let url = 'https://public.opendatasoft.com/api/records/1.0/search/';

        if (!type) {
            console.log("Exploration des types disponibles...");
            const exploreResponse = await fetch(`${url}?dataset=osm-france-healthcare&rows=10`);
            const exploreData = await exploreResponse.json();

            console.log("Premiers résultats:", exploreData.records.slice(0, 3).map(r => {
                return {
                    type: r.fields.type,
                    name: r.fields.name,
                    tags: r.fields.tags
                };
            }));
        }

        let params = {
            dataset: 'osm-france-healthcare',
            rows: 1000
        };

        // Ne pas filtrer par type pour voir tout ce qui est disponible
        if (type) {
            if (type === 'hospital') {
                params.q = 'type:"hospital" OR name:"*hôpital*" OR name:"*hospital*" OR tags:"hospital"';
            } else if (type === 'pharmacy') {
                params.q = 'type:"pharmacy" OR type:"pharmacie" OR name:"*pharmac*" OR tags:"pharmacy"';
            } else if (type === 'doctors') {
                params.q = 'type:"doctors" OR type:"doctor" OR type:"médecin" OR name:"*médecin*" OR name:"*doctor*" OR tags:"doctor"';
            } else if (type === 'clinic') {
                params.q = 'type:"clinic" OR type:"clinique" OR name:"*clinic*" OR name:"*cliniqu*" OR tags:"clinic"';
            } else {
                params.q = `type:"${type}"`;
            }
        }

        const queryString = new URLSearchParams(params).toString();
        const fullUrl = `${url}?${queryString}`;

        const response = await fetch(fullUrl);
        const data = await response.json();

        const facilities = data.records.map(facility => {
            const fields = facility.fields || {};
            const geo_point = fields.meta_geo_point || [];

            let mappedType = 'default';
            const originalType = fields.type || '';

            if (originalType.includes('hospital') || (fields.name && fields.name.toLowerCase().includes('hôpital'))) {
                mappedType = 'hospital';
            } else if (originalType.includes('pharmac') || (fields.name && fields.name.toLowerCase().includes('pharmac'))) {
                mappedType = 'pharmacy';
            } else if (originalType.includes('doctor') || originalType.includes('médecin') ||
                (fields.name && (fields.name.toLowerCase().includes('médecin') || fields.name.toLowerCase().includes('doctor')))) {
                mappedType = 'doctors';
            } else if (originalType.includes('clinic') || (fields.name && fields.name.toLowerCase().includes('clinique'))) {
                mappedType = 'clinic';
            }

            return {
                id: facility.recordid,
                name: fields.name || 'Établissement sans nom',
                type: mappedType,
                originalType: fields.type,
                city: fields.meta_name_com,
                department: fields.meta_name_dep,
                phone: fields.phone,
                latitude: geo_point[0] || null,
                longitude: geo_point[1] || null,
                opening_hours: fields.opening_hours,
                wheelchair: fields.wheelchair
            };
        });

        // Log du nombre d'établissements par type mappé
        const typeCount = {};
        facilities.forEach(f => {
            typeCount[f.type] = (typeCount[f.type] || 0) + 1;
        });

        return facilities;
    } catch (error) {
        console.error("Erreur lors de la récupération des établissements:", error);
        return [];
    }
}

export async function fetchFacilitiesByGeoArea(lat, lon, distance = 5000, limit = 300) {
    try {
        let url = 'https://public.opendatasoft.com/api/records/1.0/search/';

        const allowedTypes = ['hospital', 'pharmacy', 'doctors', 'clinic'];
        const queryParts = allowedTypes.map(t => `type:"${t}"`);
        const query = queryParts.join(' OR ');

        let params = new URLSearchParams({
            dataset: 'osm-france-healthcare',
            rows: 10000,
            q: query,
            geofilter_distance: `${lat},${lon},${distance}`
        });

        const response = await fetch(`${url}?${params.toString()}`);
        const data = await response.json();

        return data.records.map(facility => {
            const fields = facility.fields || {};
            const geo_point = fields.meta_geo_point || [];

            return {
                id: facility.recordid,
                name: fields.name || 'Établissement sans nom',
                type: fields.type || 'Autre',
                city: fields.meta_name_com,
                department: fields.meta_name_dep,
                phone: fields.phone,
                latitude: geo_point[0] || null,
                longitude: geo_point[1] || null,
                opening_hours: fields.opening_hours,
                wheelchair: fields.wheelchair
            };
        });
    } catch (error) {
        console.error("Erreur lors de la récupération des établissements par région:", error);
        return [];
    }
}