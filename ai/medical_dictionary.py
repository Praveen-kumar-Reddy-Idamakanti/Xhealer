"""
Medical Dictionary and Patient Care System
Phase 1: Medical Dictionary Foundation

This module provides comprehensive disease information, natural language descriptions,
and patient care recommendations for the disease prediction system.
"""

import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
from api_integrations import MedicalAPIIntegrations

class MedicalDictionary:
    """
    Medical Dictionary class that provides comprehensive disease information,
    care plans, and patient-friendly explanations.
    """
    
    def __init__(self, data_path: str = 'medical_data'):
        """
        Initialize the Medical Dictionary
        
        Args:
            data_path: Path to store medical data files
        """
        self.data_path = data_path
        self.disease_database = {}
        self.medical_to_layman = {}
        self.care_plans = {}
        
        # Initialize API integrations
        self.api_integrations = MedicalAPIIntegrations()
        
        # Create data directory if it doesn't exist
        os.makedirs(data_path, exist_ok=True)
        
        # Load existing data
        self.load_disease_database()
        self.load_medical_translations()
        self.load_care_plans()
        
        # Initialize with default data if empty
        if not self.disease_database:
            self.initialize_default_data()
    
    def load_disease_database(self):
        """Load disease database from JSON file"""
        db_path = os.path.join(self.data_path, 'disease_database.json')
        if os.path.exists(db_path):
            try:
                with open(db_path, 'r', encoding='utf-8') as f:
                    self.disease_database = json.load(f)
                print(f"Loaded {len(self.disease_database)} diseases from database")
            except Exception as e:
                print(f"Error loading disease database: {e}")
                self.disease_database = {}
    
    def load_medical_translations(self):
        """Load medical-to-layman translations"""
        trans_path = os.path.join(self.data_path, 'medical_translations.json')
        if os.path.exists(trans_path):
            try:
                with open(trans_path, 'r', encoding='utf-8') as f:
                    self.medical_to_layman = json.load(f)
                print(f"Loaded {len(self.medical_to_layman)} medical translations")
            except Exception as e:
                print(f"Error loading medical translations: {e}")
                self.medical_to_layman = {}
    
    def load_care_plans(self):
        """Load care plans from JSON file"""
        care_path = os.path.join(self.data_path, 'care_plans.json')
        if os.path.exists(care_path):
            try:
                with open(care_path, 'r', encoding='utf-8') as f:
                    self.care_plans = json.load(f)
                print(f"Loaded {len(self.care_plans)} care plans")
            except Exception as e:
                print(f"Error loading care plans: {e}")
                self.care_plans = {}
    
    def save_disease_database(self):
        """Save disease database to JSON file"""
        db_path = os.path.join(self.data_path, 'disease_database.json')
        try:
            with open(db_path, 'w', encoding='utf-8') as f:
                json.dump(self.disease_database, f, indent=2, ensure_ascii=False)
            print(f"Saved {len(self.disease_database)} diseases to database")
        except Exception as e:
            print(f"Error saving disease database: {e}")
    
    def save_medical_translations(self):
        """Save medical translations to JSON file"""
        trans_path = os.path.join(self.data_path, 'medical_translations.json')
        try:
            with open(trans_path, 'w', encoding='utf-8') as f:
                json.dump(self.medical_to_layman, f, indent=2, ensure_ascii=False)
            print(f"Saved {len(self.medical_to_layman)} medical translations")
        except Exception as e:
            print(f"Error saving medical translations: {e}")
    
    def save_care_plans(self):
        """Save care plans to JSON file"""
        care_path = os.path.join(self.data_path, 'care_plans.json')
        try:
            with open(care_path, 'w', encoding='utf-8') as f:
                json.dump(self.care_plans, f, indent=2, ensure_ascii=False)
            print(f"Saved {len(self.care_plans)} care plans")
        except Exception as e:
            print(f"Error saving care plans: {e}")
    
    def initialize_default_data(self):
        """Initialize with default disease data"""
        print("Initializing default medical dictionary data...")
        
        # Initialize medical translations
        self.medical_to_layman = {
            "rhinovirus": "common cold virus",
            "upper respiratory tract": "nose and throat area",
            "viral infection": "sickness caused by a virus",
            "mucous membrane": "the lining inside your nose and throat",
            "inflammation": "swelling and irritation",
            "pathogen": "germ or virus that causes disease",
            "immune system": "your body's defense system",
            "contagious": "can be spread from person to person",
            "chronic": "long-lasting or recurring",
            "acute": "sudden and severe",
            "symptom": "sign that you're sick",
            "diagnosis": "finding out what's wrong",
            "prognosis": "expected outcome of your illness",
            "treatment": "way to help you get better",
            "medication": "medicine or drug",
            "dosage": "how much medicine to take",
            "side effects": "unwanted effects from medicine",
            "allergic reaction": "bad response to something",
            "hypertension": "high blood pressure",
            "diabetes": "high blood sugar disease",
            "pneumonia": "lung infection",
            "bronchitis": "inflammation of the breathing tubes",
            "asthma": "breathing problem that comes and goes",
            "migraine": "severe headache",
            "arthritis": "joint pain and stiffness",
            "depression": "feeling very sad for a long time",
            "anxiety": "feeling worried or nervous",
            "fatigue": "feeling very tired",
            "nausea": "feeling like you want to throw up",
            "dizziness": "feeling like you might fall over",
            "fever": "body temperature higher than normal",
            "cough": "forceful breathing out to clear throat",
            "sore throat": "pain in your throat",
            "runny nose": "liquid coming out of your nose",
            "congestion": "blocked or stuffy feeling",
            "headache": "pain in your head",
            "body aches": "pain in your muscles",
            "chills": "feeling cold and shivering",
            "sweating": "producing liquid from your skin",
            "rash": "red, irritated skin",
            "swelling": "part of body getting bigger",
            "bruising": "dark mark on skin from injury",
            "bleeding": "losing blood",
            "infection": "sickness caused by germs",
            "bacteria": "tiny living things that can cause disease",
            "virus": "tiny thing that can make you sick",
            "fungus": "type of germ that can cause infections",
            "parasite": "tiny living thing that lives off another",
            "antibiotic": "medicine that kills bacteria",
            "antiviral": "medicine that fights viruses",
            "pain reliever": "medicine that reduces pain",
            "anti-inflammatory": "medicine that reduces swelling",
            "decongestant": "medicine that helps with stuffy nose",
            "cough suppressant": "medicine that stops coughing",
            "expectorant": "medicine that helps cough up mucus",
            "antihistamine": "medicine for allergies",
            "bronchodilator": "medicine that opens breathing tubes",
            "steroid": "medicine that reduces inflammation",
            "immunosuppressant": "medicine that weakens immune system",
            "chemotherapy": "strong medicine to treat cancer",
            "radiation": "treatment using energy waves",
            "surgery": "operation to fix a problem",
            "biopsy": "taking a small piece of tissue to test",
            "x-ray": "picture of inside your body",
            "mri": "detailed picture of inside your body",
            "ct scan": "detailed x-ray pictures",
            "ultrasound": "picture using sound waves",
            "blood test": "testing your blood for problems",
            "urine test": "testing your urine for problems",
            "stool test": "testing your poop for problems",
            "culture": "growing germs to identify them",
            "sensitivity": "testing which medicines work on germs"
        }
        
        # Initialize disease database with common diseases
        self.disease_database = {
            "common_cold": {
                "disease_name": "Common Cold",
                "medical_definition": "Viral infection of the upper respiratory tract, most commonly caused by rhinoviruses",
                "layman_explanation": "A common cold is like your body's way of fighting off a tiny virus that got into your nose or throat. It's your immune system working hard to get rid of the invader, which causes all those annoying symptoms like a runny nose and cough.",
                "causes": ["Rhinovirus (most common)", "Coronavirus", "Adenovirus", "Respiratory syncytial virus"],
                "risk_factors": ["Weakened immune system", "Close contact with infected person", "Seasonal changes", "Stress", "Lack of sleep"],
                "body_system": "Respiratory",
                "severity_level": "Mild to Moderate",
                "duration": "7-10 days typically",
                "common_symptoms": ["Runny nose", "Sore throat", "Cough", "Sneezing", "Mild fever", "Fatigue", "Headache"],
                "when_to_see_doctor": [
                    "Fever above 101°F for more than 3 days",
                    "Difficulty breathing",
                    "Severe headache or neck stiffness",
                    "Symptoms lasting more than 10 days",
                    "Worsening symptoms after initial improvement"
                ]
            },
            
            "influenza": {
                "disease_name": "Influenza (Flu)",
                "medical_definition": "Acute viral infection of the respiratory tract caused by influenza viruses",
                "layman_explanation": "The flu is like a really bad cold that comes on suddenly and makes you feel much worse. It's caused by a different virus that's more powerful than the common cold virus, which is why you feel so terrible.",
                "causes": ["Influenza A virus", "Influenza B virus", "Influenza C virus"],
                "risk_factors": ["Weakened immune system", "Age (very young or elderly)", "Chronic health conditions", "Pregnancy", "Close contact with infected person"],
                "body_system": "Respiratory",
                "severity_level": "Moderate to Severe",
                "duration": "1-2 weeks",
                "common_symptoms": ["High fever", "Severe body aches", "Fatigue", "Dry cough", "Headache", "Chills", "Sore throat", "Runny nose"],
                "when_to_see_doctor": [
                    "Difficulty breathing or shortness of breath",
                    "Persistent chest pain",
                    "Severe dehydration",
                    "High fever that doesn't respond to medication",
                    "Confusion or dizziness",
                    "Symptoms improve then worsen again"
                ]
            },
            
            "pneumonia": {
                "disease_name": "Pneumonia",
                "medical_definition": "Inflammation of the lungs caused by infection, resulting in fluid or pus filling the air sacs",
                "layman_explanation": "Pneumonia is when your lungs get infected and filled with fluid, making it hard to breathe. It's like your lungs are trying to fight off an infection, but they get so full of fluid that breathing becomes difficult.",
                "causes": ["Bacteria (most common)", "Viruses", "Fungi", "Mycoplasma", "Aspiration of foreign material"],
                "risk_factors": ["Age (very young or elderly)", "Weakened immune system", "Chronic lung disease", "Smoking", "Recent viral infection"],
                "body_system": "Respiratory",
                "severity_level": "Moderate to Severe",
                "duration": "1-3 weeks",
                "common_symptoms": ["Cough with phlegm", "Fever", "Difficulty breathing", "Chest pain", "Fatigue", "Sweating", "Chills", "Nausea"],
                "when_to_see_doctor": [
                    "Difficulty breathing",
                    "Chest pain",
                    "High fever (above 102°F)",
                    "Coughing up blood",
                    "Confusion (especially in elderly)",
                    "Blue lips or fingernails"
                ]
            },
            
            "bronchitis": {
                "disease_name": "Bronchitis",
                "medical_definition": "Inflammation of the bronchial tubes that carry air to and from the lungs",
                "layman_explanation": "Bronchitis is when the tubes that carry air to your lungs get irritated and swollen. It's like having a sore throat, but in your chest, which makes you cough a lot to try to clear out the irritation.",
                "causes": ["Viral infection (most common)", "Bacterial infection", "Irritants (smoke, dust, pollution)", "Gastroesophageal reflux"],
                "risk_factors": ["Smoking", "Exposure to secondhand smoke", "Weakened immune system", "Chronic lung disease", "Age (very young or elderly)"],
                "body_system": "Respiratory",
                "severity_level": "Mild to Moderate",
                "duration": "1-3 weeks",
                "common_symptoms": ["Persistent cough", "Mucus production", "Chest discomfort", "Mild fever", "Fatigue", "Wheezing", "Shortness of breath"],
                "when_to_see_doctor": [
                    "Cough lasting more than 3 weeks",
                    "High fever",
                    "Coughing up blood",
                    "Difficulty breathing",
                    "Wheezing that doesn't improve",
                    "Chest pain"
                ]
            },
            
            "asthma": {
                "disease_name": "Asthma",
                "medical_definition": "Chronic inflammatory disease of the airways characterized by reversible airflow obstruction and bronchospasm",
                "layman_explanation": "Asthma is when your breathing tubes get swollen and tight, making it hard to breathe. It's like trying to breathe through a straw that keeps getting smaller. This can happen when you're around things that irritate your lungs.",
                "causes": ["Genetic factors", "Environmental triggers", "Allergies", "Respiratory infections", "Exercise", "Stress"],
                "risk_factors": ["Family history of asthma", "Allergies", "Exposure to tobacco smoke", "Obesity", "Respiratory infections in childhood"],
                "body_system": "Respiratory",
                "severity_level": "Mild to Severe",
                "duration": "Chronic (lifelong)",
                "common_symptoms": ["Wheezing", "Shortness of breath", "Chest tightness", "Coughing (especially at night)", "Difficulty breathing during exercise"],
                "when_to_see_doctor": [
                    "Frequent asthma attacks",
                    "Symptoms that interfere with daily activities",
                    "Emergency inhaler use more than twice a week",
                    "Symptoms that wake you up at night",
                    "Severe breathing difficulty"
                ]
            }
        }
        
        # Initialize care plans
        self.care_plans = {
            "common_cold": {
                "immediate_care": [
                    "Get plenty of rest to help your body fight the virus",
                    "Stay hydrated with water, herbal teas, or clear broths",
                    "Use a humidifier or steam to ease congestion",
                    "Gargle with warm salt water for sore throat relief"
                ],
                "medications": [
                    "Acetaminophen or ibuprofen for fever and body aches",
                    "Decongestant nasal sprays (use sparingly, no more than 3 days)",
                    "Cough suppressants if cough is disruptive to sleep",
                    "Throat lozenges for sore throat relief"
                ],
                "home_remedies": [
                    "Chicken soup (helps with congestion and provides nutrients)",
                    "Honey and lemon in warm water (soothes throat)",
                    "Ginger tea (reduces inflammation)",
                    "Steam inhalation with eucalyptus oil"
                ],
                "warning_signs": [
                    "Fever above 101°F for more than 3 days",
                    "Difficulty breathing or shortness of breath",
                    "Severe headache or neck stiffness",
                    "Symptoms lasting more than 10 days",
                    "Worsening symptoms after initial improvement"
                ]
            },
            
            "influenza": {
                "immediate_care": [
                    "Stay home and rest completely",
                    "Drink plenty of fluids to prevent dehydration",
                    "Use fever-reducing medications as directed",
                    "Apply cool compresses for fever relief"
                ],
                "medications": [
                    "Antiviral medications (if started within 48 hours)",
                    "Acetaminophen or ibuprofen for fever and pain",
                    "Cough suppressants for dry cough",
                    "Decongestants for nasal congestion"
                ],
                "home_remedies": [
                    "Warm fluids like tea with honey",
                    "Chicken soup for nutrition and hydration",
                    "Rest in a comfortable, well-ventilated room",
                    "Use a humidifier to ease breathing"
                ],
                "warning_signs": [
                    "Difficulty breathing or shortness of breath",
                    "Persistent chest pain or pressure",
                    "Severe dehydration (dry mouth, no urination)",
                    "High fever that doesn't respond to medication",
                    "Confusion or dizziness",
                    "Symptoms improve then worsen again"
                ]
            }
        }
        
        # Save all data
        self.save_disease_database()
        self.save_medical_translations()
        self.save_care_plans()
        
        print("Default medical dictionary data initialized successfully!")
    
    def get_disease_info(self, disease_name: str) -> Optional[Dict[str, Any]]:
        """
        Get comprehensive disease information
        
        Args:
            disease_name: Name of the disease (can be medical or common name)
            
        Returns:
            Dictionary containing disease information or None if not found
        """
        # Normalize disease name
        normalized_name = self._normalize_disease_name(disease_name)
        
        if normalized_name in self.disease_database:
            disease_info = self.disease_database[normalized_name].copy()
            
            # Translate medical terms to layman terms
            disease_info['layman_explanation'] = self._translate_medical_terms(
                disease_info.get('layman_explanation', '')
            )
            
            return disease_info
        
        return None
    
    def get_care_plan(self, disease_name: str) -> Optional[Dict[str, List[str]]]:
        """
        Get care plan for a specific disease
        
        Args:
            disease_name: Name of the disease
            
        Returns:
            Dictionary containing care plan or None if not found
        """
        normalized_name = self._normalize_disease_name(disease_name)
        return self.care_plans.get(normalized_name)
    
    def get_comprehensive_info(self, disease_name: str) -> Dict[str, Any]:
        """
        Get comprehensive information including disease info and care plan
        
        Args:
            disease_name: Name of the disease
            
        Returns:
            Dictionary containing all available information
        """
        disease_info = self.get_disease_info(disease_name)
        care_plan = self.get_care_plan(disease_name)
        
        result = {
            "disease_info": disease_info,
            "care_plan": care_plan,
            "timestamp": datetime.now().isoformat(),
            "source": "Medical Dictionary v1.0"
        }
        
        return result
    
    def _normalize_disease_name(self, disease_name: str) -> str:
        """
        Normalize disease name for consistent lookup
        
        Args:
            disease_name: Original disease name
            
        Returns:
            Normalized disease name
        """
        # Convert to lowercase and replace spaces with underscores
        normalized = disease_name.lower().strip()
        normalized = normalized.replace(' ', '_')
        normalized = normalized.replace('-', '_')
        
        # Handle common variations
        variations = {
            'flu': 'influenza',
            'cold': 'common_cold',
            'chest_cold': 'bronchitis',
            'stomach_flu': 'gastroenteritis'
        }
        
        return variations.get(normalized, normalized)
    
    def _translate_medical_terms(self, text: str) -> str:
        """
        Translate medical terms to layman terms in text
        
        Args:
            text: Text containing medical terms
            
        Returns:
            Text with medical terms translated
        """
        translated_text = text
        
        # Sort terms by length (longest first) to avoid partial replacements
        sorted_terms = sorted(self.medical_to_layman.items(), key=lambda x: len(x[0]), reverse=True)
        
        for medical_term, layman_term in sorted_terms:
            # Replace whole words only (case insensitive)
            import re
            pattern = r'\b' + re.escape(medical_term) + r'\b'
            translated_text = re.sub(pattern, layman_term, translated_text, flags=re.IGNORECASE)
        
        return translated_text
    
    def add_disease(self, disease_key: str, disease_info: Dict[str, Any]):
        """
        Add a new disease to the database
        
        Args:
            disease_key: Unique key for the disease
            disease_info: Dictionary containing disease information
        """
        self.disease_database[disease_key] = disease_info
        self.save_disease_database()
        print(f"Added disease: {disease_info.get('disease_name', disease_key)}")
    
    def add_care_plan(self, disease_key: str, care_plan: Dict[str, List[str]]):
        """
        Add a care plan for a disease
        
        Args:
            disease_key: Unique key for the disease
            care_plan: Dictionary containing care plan information
        """
        self.care_plans[disease_key] = care_plan
        self.save_care_plans()
        print(f"Added care plan for: {disease_key}")
    
    def search_diseases(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for diseases by name or symptoms
        
        Args:
            query: Search query
            
        Returns:
            List of matching diseases
        """
        query = query.lower()
        matches = []
        
        for disease_key, disease_info in self.disease_database.items():
            # Search in disease name
            if query in disease_info.get('disease_name', '').lower():
                matches.append(disease_info)
                continue
            
            # Search in symptoms
            symptoms = disease_info.get('common_symptoms', [])
            if any(query in symptom.lower() for symptom in symptoms):
                matches.append(disease_info)
                continue
            
            # Search in causes
            causes = disease_info.get('causes', [])
            if any(query in cause.lower() for cause in causes):
                matches.append(disease_info)
        
        return matches
    
    def get_all_diseases(self) -> List[str]:
        """
        Get list of all available diseases
        
        Returns:
            List of disease names
        """
        return [info['disease_name'] for info in self.disease_database.values()]
    
    def get_diseases_by_system(self, body_system: str) -> List[Dict[str, Any]]:
        """
        Get diseases by body system
        
        Args:
            body_system: Body system (e.g., 'Respiratory', 'Cardiovascular')
            
        Returns:
            List of diseases in the specified body system
        """
        return [
            disease_info for disease_info in self.disease_database.values()
            if disease_info.get('body_system', '').lower() == body_system.lower()
        ]
    
    
    def get_food_nutrition(self, food_name: str) -> Optional[Dict]:
        """
        Get nutrition information from Open Food Facts API
        
        Args:
            food_name: Name of the food
            
        Returns:
            Nutrition information dictionary
        """
        return self.api_integrations.get_food_nutrition(food_name)
    
    def get_health_tips(self, condition: str) -> List[str]:
        """
        Get health tips for a specific condition
        
        Args:
            condition: Health condition
            
        Returns:
            List of health tips
        """
        return self.api_integrations.get_health_tips(condition)
    
    
    def get_enhanced_disease_info(self, disease_name: str) -> Dict[str, Any]:
        """
        Get enhanced disease information with API data
        
        Args:
            disease_name: Name of the disease
            
        Returns:
            Enhanced disease information with API data
        """
        # Get basic disease information
        basic_info = self.get_comprehensive_info(disease_name)
        
        # Get health tips from API
        health_tips = self.get_health_tips(disease_name)
        
        # Enhance with API data
        enhanced_info = basic_info.copy()
        enhanced_info['health_tips'] = health_tips
        enhanced_info['api_enhanced'] = True
        enhanced_info['last_updated'] = datetime.now().isoformat()
        
        return enhanced_info
    
    def get_nutritional_recommendations(self, disease_name: str) -> Dict[str, Any]:
        """
        Get nutritional recommendations for a disease
        
        Args:
            disease_name: Name of the disease
            
        Returns:
            Nutritional recommendations with food information
        """
        # Get disease-specific foods from care plan
        care_plan = self.get_care_plan(disease_name)
        recommended_foods = []
        foods_to_avoid = []
        
        if care_plan:
            # Extract food recommendations from care plan
            for care_type, recommendations in care_plan.items():
                for rec in recommendations:
                    if 'food' in rec.lower() or 'eat' in rec.lower():
                        recommended_foods.append(rec)
                    elif 'avoid' in rec.lower() or 'don\'t' in rec.lower():
                        foods_to_avoid.append(rec)
        
        # Get nutrition information for recommended foods
        food_nutrition = {}
        for food_rec in recommended_foods[:3]:  # Limit to first 3 foods
            # Extract food name from recommendation
            food_name = self._extract_food_name(food_rec)
            if food_name:
                nutrition_info = self.get_food_nutrition(food_name)
                if nutrition_info:
                    food_nutrition[food_name] = nutrition_info
        
        return {
            'disease': disease_name,
            'recommended_foods': recommended_foods,
            'foods_to_avoid': foods_to_avoid,
            'food_nutrition': food_nutrition,
            'general_nutrition_tips': [
                'Eat a balanced diet with plenty of fruits and vegetables',
                'Stay hydrated by drinking plenty of water',
                'Limit processed foods and added sugars',
                'Include lean proteins and whole grains',
                'Consult with a nutritionist for personalized advice'
            ],
            'source': 'Medical Dictionary + Open Food Facts API'
        }
    
    def _extract_food_name(self, recommendation: str) -> Optional[str]:
        """
        Extract food name from a recommendation string
        
        Args:
            recommendation: Recommendation text
            
        Returns:
            Extracted food name or None
        """
        # Simple extraction - look for common food words
        food_keywords = [
            'chicken', 'soup', 'broth', 'tea', 'honey', 'lemon', 'ginger',
            'apple', 'banana', 'orange', 'vegetables', 'fruits', 'water',
            'yogurt', 'rice', 'bread', 'milk', 'cheese', 'eggs'
        ]
        
        recommendation_lower = recommendation.lower()
        for keyword in food_keywords:
            if keyword in recommendation_lower:
                return keyword
        
        return None


# Example usage and testing
if __name__ == "__main__":
    # Initialize medical dictionary
    md = MedicalDictionary()
    
    # Test getting disease information
    print("=== Testing Medical Dictionary ===")
    
    # Test common cold
    cold_info = md.get_comprehensive_info("common cold")
    if cold_info['disease_info']:
        print(f"\nDisease: {cold_info['disease_info']['disease_name']}")
        print(f"Explanation: {cold_info['disease_info']['layman_explanation']}")
        print(f"Common symptoms: {', '.join(cold_info['disease_info']['common_symptoms'])}")
    
    # Test care plan
    if cold_info['care_plan']:
        print(f"\nImmediate care:")
        for care in cold_info['care_plan']['immediate_care']:
            print(f"  - {care}")
    
    # Test search functionality
    print(f"\n=== Search Results for 'cough' ===")
    cough_diseases = md.search_diseases("cough")
    for disease in cough_diseases:
        print(f"- {disease['disease_name']}")
    
    print(f"\n=== All Available Diseases ===")
    all_diseases = md.get_all_diseases()
    for disease in all_diseases:
        print(f"- {disease}")
