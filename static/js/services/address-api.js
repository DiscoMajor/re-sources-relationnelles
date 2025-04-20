// static/js/services/address-api.js
export async function searchAddress(query) {
    try {
        const url = `https://api-adresse.data.gouv.fr/search/?q=${encodeURIComponent(query)}&limit=5`;
        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error(`Erreur HTTP: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error("Erreur lors de la requête à l'API adresse:", error);
        throw error;
    }
}