"""
Free Open-Source Medical API Integrations
Integrates with various free medical and health APIs to enhance the medical dictionary
"""

import requests
import json
import time
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MedicalAPIIntegrations:
    """
    Class to handle integrations with free medical APIs
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Medical-Dictionary-Bot/1.0'
        })
        
        # API endpoints and configurations
        self.apis = {
            'openfda': {
                'base_url': 'https://api.fda.gov',
                'rate_limit': 1000,  # requests per hour
                'last_request': None,
                'request_count': 0,
                'reset_time': None
            },
            'disease_ontology': {
                'base_url': 'http://www.disease-ontology.org/api',
                'rate_limit': None,  # No official limit
                'last_request': None,
                'request_count': 0,
                'reset_time': None
            },
            'usda_food': {
                'base_url': 'https://api.nal.usda.gov/fdc/v1',
                'rate_limit': 1000,  # requests per hour
                'api_key': None,  # Free tier doesn't require key
                'last_request': None,
                'request_count': 0,
                'reset_time': None
            },
            'openfoodfacts': {
                'base_url': 'https://world.openfoodfacts.org/api/v0',
                'rate_limit': None,  # No official limit
                'last_request': None,
                'request_count': 0,
                'reset_time': None
            }
        }
    
    def _rate_limit_check(self, api_name: str) -> bool:
        """
        Check if we can make a request based on rate limits
        
        Args:
            api_name: Name of the API
            
        Returns:
            True if request is allowed, False otherwise
        """
        api_config = self.apis.get(api_name)
        if not api_config:
            return False
        
        # No rate limit
        if not api_config.get('rate_limit'):
            return True
        
        current_time = datetime.now()
        
        # Reset counter if hour has passed
        if (api_config.get('reset_time') and 
            current_time >= api_config['reset_time']):
            api_config['request_count'] = 0
            api_config['reset_time'] = current_time + timedelta(hours=1)
        
        # Check if we've exceeded rate limit
        if api_config['request_count'] >= api_config['rate_limit']:
            return False
        
        return True
    
    def _make_request(self, api_name: str, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """
        Make a rate-limited request to an API
        
        Args:
            api_name: Name of the API
            endpoint: API endpoint
            params: Request parameters
            
        Returns:
            API response as dictionary or None if failed
        """
        if not self._rate_limit_check(api_name):
            logger.warning(f"Rate limit exceeded for {api_name}")
            return None
        
        api_config = self.apis[api_name]
        url = f"{api_config['base_url']}{endpoint}"
        
        try:
            # Add delay between requests to be respectful
            if api_config.get('last_request'):
                time_since_last = time.time() - api_config['last_request']
                if time_since_last < 1:  # 1 second delay
                    time.sleep(1 - time_since_last)
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            # Update rate limiting info
            api_config['last_request'] = time.time()
            api_config['request_count'] += 1
            
            if not api_config.get('reset_time'):
                api_config['reset_time'] = datetime.now() + timedelta(hours=1)
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed for {api_name}: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error for {api_name}: {e}")
            return None
    
    def get_drug_info(self, drug_name: str) -> Optional[Dict]:
        """
        Get drug information from OpenFDA API
        
        Args:
            drug_name: Name of the drug
            
        Returns:
            Drug information dictionary
        """
        endpoint = '/drug/label.json'
        params = {
            'search': f'openfda.brand_name:"{drug_name}" OR openfda.generic_name:"{drug_name}"',
            'limit': 1
        }
        
        response = self._make_request('openfda', endpoint, params)
        if not response or not response.get('results'):
            return None
        
        drug_data = response['results'][0]
        
        return {
            'name': drug_name,
            'brand_names': drug_data.get('openfda', {}).get('brand_name', []),
            'generic_name': drug_data.get('openfda', {}).get('generic_name', []),
            'manufacturer': drug_data.get('openfda', {}).get('manufacturer_name', []),
            'indications': drug_data.get('indications_and_usage', []),
            'warnings': drug_data.get('warnings', []),
            'side_effects': drug_data.get('adverse_reactions', []),
            'dosage': drug_data.get('dosage_and_administration', []),
            'source': 'OpenFDA API'
        }
    
    def get_disease_ontology_info(self, disease_name: str) -> Optional[Dict]:
        """
        Get disease information from Disease Ontology API
        
        Args:
            disease_name: Name of the disease
            
        Returns:
            Disease ontology information
        """
        # Note: Disease Ontology API is more complex, this is a simplified version
        # In practice, you'd need to search by ID or use their SPARQL endpoint
        
        endpoint = '/metadata/doid'
        params = {'format': 'json'}
        
        response = self._make_request('disease_ontology', endpoint, params)
        if not response:
            return None
        
        return {
            'name': disease_name,
            'ontology_id': response.get('id'),
            'definition': response.get('definition'),
            'synonyms': response.get('synonyms', []),
            'parents': response.get('parents', []),
            'children': response.get('children', []),
            'source': 'Disease Ontology'
        }
    
    def get_food_nutrition(self, food_name: str) -> Optional[Dict]:
        """
        Get nutrition information from Open Food Facts (free alternative to USDA)
        
        Args:
            food_name: Name of the food
            
        Returns:
            Nutrition information
        """
        # Use Open Food Facts instead of USDA (no API key required)
        endpoint = '/cgi/search.pl'
        params = {
            'search_terms': food_name,
            'search_simple': 1,
            'action': 'process',
            'json': 1,
            'page_size': 1
        }
        
        response = self._make_request('openfoodfacts', endpoint, params)
        if not response or not response.get('products'):
            return None
        
        product = response['products'][0]
        nutriments = product.get('nutriments', {})
        
        # Extract key nutrition information
        nutrients = {}
        nutrition_mapping = {
            'energy-kcal_100g': 'Calories (per 100g)',
            'proteins_100g': 'Protein (per 100g)',
            'carbohydrates_100g': 'Carbohydrates (per 100g)',
            'fat_100g': 'Fat (per 100g)',
            'fiber_100g': 'Fiber (per 100g)',
            'sugars_100g': 'Sugars (per 100g)',
            'sodium_100g': 'Sodium (per 100g)',
            'vitamin-c_100g': 'Vitamin C (per 100g)',
            'calcium_100g': 'Calcium (per 100g)',
            'iron_100g': 'Iron (per 100g)'
        }
        
        for key, label in nutrition_mapping.items():
            if key in nutriments:
                nutrients[label] = {
                    'amount': nutriments[key],
                    'unit': 'g' if '100g' in key else 'kcal'
                }
        
        return {
            'name': product.get('product_name', food_name),
            'description': product.get('generic_name', ''),
            'brand': product.get('brands', ''),
            'categories': product.get('categories', ''),
            'ingredients': product.get('ingredients_text', ''),
            'nutrition_grade': product.get('nutrition_grade_fr', ''),
            'nutrients': nutrients,
            'source': 'Open Food Facts'
        }
    
    def get_food_product_info(self, product_name: str) -> Optional[Dict]:
        """
        Get food product information from Open Food Facts
        
        Args:
            product_name: Name of the food product
            
        Returns:
            Food product information
        """
        endpoint = '/cgi/search.pl'
        params = {
            'search_terms': product_name,
            'search_simple': 1,
            'action': 'process',
            'json': 1,
            'page_size': 1
        }
        
        response = self._make_request('openfoodfacts', endpoint, params)
        if not response or not response.get('products'):
            return None
        
        product = response['products'][0]
        
        return {
            'name': product.get('product_name', product_name),
            'brand': product.get('brands', ''),
            'categories': product.get('categories', ''),
            'ingredients': product.get('ingredients_text', ''),
            'nutrition_grade': product.get('nutrition_grade_fr', ''),
            'allergens': product.get('allergens_tags', []),
            'additives': product.get('additives_tags', []),
            'nutrients': product.get('nutriments', {}),
            'source': 'Open Food Facts'
        }
    
    def get_medication_interactions(self, drug_names: List[str]) -> Optional[Dict]:
        """
        Get drug interaction information from OpenFDA
        
        Args:
            drug_names: List of drug names to check interactions for
            
        Returns:
            Interaction information
        """
        if len(drug_names) < 2:
            return None
        
        # Search for drug interactions
        endpoint = '/drug/event.json'
        search_terms = ' OR '.join([f'patient.drug.medicinalproduct:"{drug}"' for drug in drug_names])
        params = {
            'search': search_terms,
            'limit': 10
        }
        
        response = self._make_request('openfda', endpoint, params)
        if not response:
            return None
        
        # Analyze interactions (simplified)
        interactions = []
        for result in response.get('results', []):
            drugs = result.get('patient', {}).get('drug', [])
            if len(drugs) >= 2:
                interaction = {
                    'drugs': [drug.get('medicinalproduct', '') for drug in drugs],
                    'reaction': result.get('patient', {}).get('reaction', []),
                    'seriousness': result.get('seriousness', [])
                }
                interactions.append(interaction)
        
        return {
            'drugs_checked': drug_names,
            'interactions': interactions,
            'source': 'OpenFDA API'
        }
    
    def get_health_tips(self, condition: str) -> List[str]:
        """
        Generate health tips based on condition (using static data for now)
        This could be enhanced with AI or more APIs in the future
        
        Args:
            condition: Health condition
            
        Returns:
            List of health tips
        """
        tips_database = {
            'cold': [
                'Get plenty of rest to help your immune system fight the virus',
                'Stay hydrated with water, herbal teas, or clear broths',
                'Use a humidifier to ease congestion and coughing',
                'Gargle with warm salt water to soothe a sore throat',
                'Wash your hands frequently to prevent spreading the virus'
            ],
            'flu': [
                'Stay home and rest completely to avoid spreading the virus',
                'Drink plenty of fluids to prevent dehydration',
                'Use fever-reducing medications as directed by your doctor',
                'Apply cool compresses to help reduce fever',
                'Avoid close contact with others until symptoms improve'
            ],
            'pneumonia': [
                'Get plenty of rest and avoid overexertion',
                'Stay hydrated with water and clear fluids',
                'Use a humidifier to help with breathing',
                'Take prescribed medications exactly as directed',
                'Monitor your symptoms and seek medical attention if they worsen'
            ],
            'diabetes': [
                'Monitor your blood sugar levels regularly',
                'Follow a balanced diet with controlled carbohydrates',
                'Exercise regularly as recommended by your doctor',
                'Take medications as prescribed',
                'Keep regular appointments with your healthcare team'
            ],
            'hypertension': [
                'Reduce sodium intake in your diet',
                'Exercise regularly (at least 150 minutes per week)',
                'Maintain a healthy weight',
                'Limit alcohol consumption',
                'Take blood pressure medications as prescribed'
            ]
        }
        
        condition_lower = condition.lower()
        for key, tips in tips_database.items():
            if key in condition_lower:
                return tips
        
        # Default tips
        return [
            'Maintain a healthy diet with plenty of fruits and vegetables',
            'Get regular exercise as recommended by your doctor',
            'Stay hydrated by drinking plenty of water',
            'Get adequate sleep (7-9 hours per night)',
            'Follow your doctor\'s treatment plan and take medications as prescribed'
        ]


# Example usage and testing
if __name__ == "__main__":
    api = MedicalAPIIntegrations()
    
    print("=== Testing Medical API Integrations ===")
    
    # Test drug information
    print("\n1. Testing OpenFDA Drug Information:")
    drug_info = api.get_drug_info("aspirin")
    if drug_info:
        print(f"Drug: {drug_info['name']}")
        print(f"Generic names: {drug_info.get('generic_name', [])}")
        print(f"Manufacturers: {drug_info.get('manufacturer', [])}")
    
    # Test food nutrition
    print("\n2. Testing USDA Food Nutrition:")
    nutrition_info = api.get_food_nutrition("apple")
    if nutrition_info:
        print(f"Food: {nutrition_info['name']}")
        print(f"Description: {nutrition_info.get('description', '')}")
        if nutrition_info.get('nutrients'):
            print("Key nutrients:")
            for nutrient, info in list(nutrition_info['nutrients'].items())[:5]:
                print(f"  - {nutrient}: {info.get('amount', 0)} {info.get('unit', '')}")
    
    # Test health tips
    print("\n3. Testing Health Tips:")
    tips = api.get_health_tips("cold")
    print("Health tips for cold:")
    for tip in tips:
        print(f"  - {tip}")
    
    print("\n=== API Integration Test Complete ===")
