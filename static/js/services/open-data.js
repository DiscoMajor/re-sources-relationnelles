export async function fetchHealthFacilities(type = null) {
    try {
        let url = 'https://public.opendatasoft.com/api/records/1.0/search/';

        let params = {
            dataset: 'osm-france-healthcare',
            rows: 1000
        };

        if (type) {
            params.q = `type:"${type}"`;
        } else {
            const allowedTypes = ['hospital', 'pharmacy', 'doctors', 'clinic'];
            const queryParts = allowedTypes.map(t => `type:"${t}"`);
            params.q = queryParts.join(' OR ');
        }

        const queryString = new URLSearchParams(params).toString();
        const fullUrl = `${url}?${queryString}`;

        const response = await fetch(fullUrl);
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