import pandas as pd
import numpy as np
import pickle
import json
from sklearn.preprocessing import StandardScaler
import re
from datetime import datetime

class DiseasePredictor:
    def __init__(self, model_path='trained_models', data_path='augmented_data'):
        self.model_path = model_path
        self.data_path = data_path
        self.models = {}
        self.scaler = None
        self.label_encoder = None
        self.tfidf_vectorizer = None
        self.disease_classes = []
        
        # Medical term standardization dictionary
        self.medical_synonyms = {
            'stomach pain': 'abdominal pain',
            'belly pain': 'abdominal pain',
            'tummy ache': 'abdominal pain',
            'throwing up': 'vomiting',
            'puking': 'vomiting',
            'feeling sick': 'nausea',
            'queasy': 'nausea',
            'high temperature': 'fever',
            'temp': 'fever',
            'runny nose': 'nasal discharge',
            'stuffy nose': 'nasal congestion',
            'sore throat': 'throat pain',
            'trouble breathing': 'shortness of breath',
            'hard to breathe': 'shortness of breath',
            'can\'t breathe': 'shortness of breath',
            'tired': 'fatigue',
            'exhausted': 'fatigue',
            'weak': 'fatigue',
            'dizzy': 'dizziness',
            'lightheaded': 'dizziness'
        }
        
        # Body system classification
        self.body_systems = {
            'respiratory': ['cough', 'breath', 'chest', 'lung', 'nasal', 'throat', 'sneezing'],
            'cardiovascular': ['chest pain', 'heart', 'blood pressure', 'palpitation'],
            'gastrointestinal': ['abdominal', 'stomach', 'nausea', 'vomiting', 'diarrhea', 'constipation', 'appetite'],
            'genitourinary': ['urination', 'urine', 'pelvic', 'genital', 'kidney', 'bladder'],
            'neurological': ['headache', 'dizziness', 'confusion', 'seizure', 'numbness', 'weakness'],
            'dermatological': ['rash', 'itching', 'skin', 'lesion', 'swelling'],
            'musculoskeletal': ['joint', 'muscle', 'bone', 'back', 'neck', 'limb'],
            'endocrine': ['weight', 'thirst', 'urination', 'fatigue', 'temperature']
        }
        
        # Severity indicators
        self.severity_indicators = {
            'severe': ['severe', 'intense', 'acute', 'sudden', 'high fever', 'profound'],
            'mild': ['mild', 'low-grade', 'slight', 'minor', 'mild fever'],
            'chronic': ['chronic', 'persistent', 'recurrent', 'ongoing', 'long-term']
        }
    
    def load_models(self):
        """Load all trained models and preprocessors"""
        print("Loading trained models...")
        
        try:
            # Load individual models
            model_files = {
                'Naive_Bayes': 'naive_bayes_model.pkl',
                'SVM': 'svm_model.pkl',
                'Random_Forest': 'random_forest_model.pkl',
                'Logistic_Regression': 'logistic_regression_model.pkl',
                'Neural_Network': 'neural_network_model.pkl'
            }
            
            for model_name, filename in model_files.items():
                try:
                    with open(f'{self.model_path}/{filename}', 'rb') as f:
                        self.models[model_name] = pickle.load(f)
                    print(f"  ✓ {model_name} loaded successfully")
                except FileNotFoundError:
                    print(f"  ✗ {model_name} not found - skipping")
            
            # Load scaler
            with open(f'{self.model_path}/scaler.pkl', 'rb') as f:
                self.scaler = pickle.load(f)
            print("  ✓ Scaler loaded successfully")
            
            # Load label encoder
            with open(f'{self.data_path}/label_encoder.pkl', 'rb') as f:
                self.label_encoder = pickle.load(f)
            self.disease_classes = list(self.label_encoder.classes_)
            print("  ✓ Label encoder loaded successfully")
            
            # Load TF-IDF vectorizer
            with open(f'{self.data_path}/tfidf_vectorizer.pkl', 'rb') as f:
                self.tfidf_vectorizer = pickle.load(f)
            print("  ✓ TF-IDF vectorizer loaded successfully")
            
            print(f"Models loaded successfully! {len(self.models)} models available.")
            return True
            
        except Exception as e:
            print(f"Error loading models: {e}")
            return False
    
    def clean_text(self, text):
        """Clean and normalize text"""
        if pd.isna(text) or not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep medical terms
        text = re.sub(r'[^\w\s;]', ' ', text)
        
        # Remove extra spaces
        text = text.strip()
        
        return text
    
    def standardize_medical_terms(self, text):
        """Standardize medical terms using synonym dictionary"""
        for synonym, standard_term in self.medical_synonyms.items():
            text = re.sub(r'\b' + re.escape(synonym) + r'\b', standard_term, text)
        return text
    
    def preprocess_symptoms(self, symptoms_text):
        """Preprocess symptoms text into features"""
        # Clean the text
        cleaned_text = self.clean_text(symptoms_text)
        cleaned_text = self.standardize_medical_terms(cleaned_text)
        
        # Split symptoms by semicolon
        symptoms_list = [s.strip() for s in cleaned_text.split(';') if s.strip()]
        
        # Create combined text for TF-IDF
        symptoms_combined = ' '.join(symptoms_list)
        
        # Create TF-IDF features
        tfidf_features = self.tfidf_vectorizer.transform([symptoms_combined])
        
        # Create additional features
        additional_features = []
        
        # Symptom count
        symptom_count = len(symptoms_list)
        additional_features.append(symptom_count)
        
        # Body system features
        for system, keywords in self.body_systems.items():
            has_system = any(keyword in symptoms_combined for keyword in keywords)
            additional_features.append(int(has_system))
        
        # Severity features
        for severity, keywords in self.severity_indicators.items():
            has_severity = any(keyword in symptoms_combined for keyword in keywords)
            additional_features.append(int(has_severity))
        
        # Symptom diversity (number of body systems affected)
        system_columns = [f'has_{system}_symptoms' for system in self.body_systems.keys()]
        symptom_diversity = sum(additional_features[1:9])  # Body system features
        additional_features.append(symptom_diversity)
        
        # Combine TF-IDF and additional features
        tfidf_array = tfidf_features.toarray().flatten()
        feature_vector = np.concatenate([tfidf_array, additional_features])
        
        return feature_vector, symptoms_list
    
    def predict_disease(self, symptoms_text, top_k=5):
        """Predict disease from symptoms"""
        if not self.models:
            raise ValueError("Models not loaded. Call load_models() first.")
        
        # Preprocess symptoms
        feature_vector, symptoms_list = self.preprocess_symptoms(symptoms_text)
        feature_vector = feature_vector.reshape(1, -1)
        
        # Get predictions from all models
        predictions = {}
        probabilities = {}
        
        # Naive Bayes and Random Forest use original features
        for model_name in ['Naive_Bayes', 'Random_Forest']:
            if model_name in self.models:
                pred = self.models[model_name].predict(feature_vector)[0]
                pred_proba = self.models[model_name].predict_proba(feature_vector)[0]
                predictions[model_name] = pred
                probabilities[model_name] = pred_proba
        
        # SVM, LR, and MLP use scaled features
        feature_vector_scaled = self.scaler.transform(feature_vector)
        for model_name in ['SVM', 'Logistic_Regression', 'Neural_Network']:
            if model_name in self.models:
                pred = self.models[model_name].predict(feature_vector_scaled)[0]
                pred_proba = self.models[model_name].predict_proba(feature_vector_scaled)[0]
                predictions[model_name] = pred
                probabilities[model_name] = pred_proba
        
        # Ensemble prediction (majority voting)
        if predictions:
            votes = list(predictions.values())
            ensemble_pred = max(set(votes), key=votes.count)
            
            # Ensemble probabilities (average)
            if probabilities:
                ensemble_proba = np.mean(list(probabilities.values()), axis=0)
            else:
                ensemble_proba = np.zeros(len(self.disease_classes))
                ensemble_proba[ensemble_pred] = 1.0
        else:
            raise ValueError("No models available for prediction")
        
        # Get top-k predictions
        top_k_indices = np.argsort(ensemble_proba)[-top_k:][::-1]
        top_k_diseases = []
        
        for i, idx in enumerate(top_k_indices):
            disease_name = self.disease_classes[idx]
            confidence = ensemble_proba[idx]
            top_k_diseases.append({
                'rank': i + 1,
                'disease': disease_name,
                'confidence': float(confidence),
                'percentage': float(confidence * 100)
            })
        
        return {
            'input_symptoms': symptoms_list,
            'predicted_disease': self.disease_classes[ensemble_pred],
            'confidence': float(ensemble_proba[ensemble_pred]),
            'top_k_predictions': top_k_diseases,
            'individual_predictions': {name: self.disease_classes[pred] for name, pred in predictions.items()},
            'timestamp': datetime.now().isoformat()
        }
    
    def get_disease_info(self, disease_name):
        """Get information about a specific disease"""
        # This could be expanded with more detailed disease information
        return {
            'name': disease_name,
            'description': f"Information about {disease_name}",
            'note': "This is a prediction based on symptoms. Please consult a healthcare professional for proper diagnosis."
        }
    
    def validate_symptoms(self, symptoms_text):
        """Validate and provide feedback on symptom input"""
        if not symptoms_text or not symptoms_text.strip():
            return {
                'valid': False,
                'message': 'Please enter at least one symptom.',
                'suggestions': []
            }
        
        symptoms_list = [s.strip() for s in symptoms_text.split(';') if s.strip()]
        
        if len(symptoms_list) < 2:
            return {
                'valid': False,
                'message': 'Please enter at least 2 symptoms for better accuracy.',
                'suggestions': ['Add more specific symptoms', 'Include severity indicators (mild, severe, etc.)']
            }
        
        if len(symptoms_list) > 15:
            return {
                'valid': False,
                'message': 'Too many symptoms. Please limit to 15 symptoms for better accuracy.',
                'suggestions': ['Focus on the most prominent symptoms', 'Remove less relevant symptoms']
            }
        
        return {
            'valid': True,
            'message': f'Valid input with {len(symptoms_list)} symptoms.',
            'suggestions': []
        }

def main():
    """Test the disease predictor"""
    print("=" * 60)
    print("DISEASE PREDICTION SYSTEM")
    print("=" * 60)
    
    # Initialize predictor
    predictor = DiseasePredictor()
    
    # Load models
    if not predictor.load_models():
        print("Failed to load models. Please ensure models are trained first.")
        return
    
    # Test with sample symptoms
    test_symptoms = [
        "fever; headache; fatigue; muscle aches; chills",
        "abdominal pain; nausea; vomiting; loss of appetite",
        "chest pain; shortness of breath; fatigue; sweating",
        "frequent urination; burning sensation; cloudy urine"
    ]
    
    print("\nTesting disease prediction system...")
    print("-" * 40)
    
    for i, symptoms in enumerate(test_symptoms, 1):
        print(f"\nTest {i}: {symptoms}")
        
        try:
            # Validate input
            validation = predictor.validate_symptoms(symptoms)
            if not validation['valid']:
                print(f"  Validation Error: {validation['message']}")
                continue
            
            # Make prediction
            result = predictor.predict_disease(symptoms, top_k=3)
            
            print(f"  Predicted Disease: {result['predicted_disease']}")
            print(f"  Confidence: {result['confidence']:.2%}")
            print(f"  Top 3 Predictions:")
            for pred in result['top_k_predictions']:
                print(f"    {pred['rank']}. {pred['disease']} ({pred['percentage']:.1f}%)")
            
        except Exception as e:
            print(f"  Error: {e}")
    
    print("\n" + "=" * 60)
    print("DISEASE PREDICTION SYSTEM READY!")
    print("=" * 60)
    
    return predictor

if __name__ == "__main__":
    predictor = main()

