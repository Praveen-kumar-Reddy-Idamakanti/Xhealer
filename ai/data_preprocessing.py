import pandas as pd
import numpy as np
import re
import string
from collections import Counter
import pickle
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

class DiseaseSymptomPreprocessor:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        # Medical terms that should not be removed as stop words
        self.medical_terms = {
            'pain', 'fever', 'nausea', 'vomiting', 'cough', 'headache', 'fatigue',
            'swelling', 'bleeding', 'discharge', 'rash', 'itching', 'burning',
            'shortness', 'breath', 'chest', 'abdominal', 'pelvic', 'urination',
            'diarrhea', 'constipation', 'appetite', 'weight', 'blood', 'urine'
        }
        self.stop_words = self.stop_words - self.medical_terms
        
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
            'lightheaded': 'dizziness',
            'throwing up blood': 'hematemesis',
            'blood in stool': 'hematochezia',
            'blood in urine': 'hematuria',
            'peeing blood': 'hematuria',
            'can\'t pee': 'urinary retention',
            'hard to pee': 'dysuria',
            'painful urination': 'dysuria',
            'burning when peeing': 'dysuria'
        }
        
        self.tfidf_vectorizer = None
        self.label_encoder = None
        
    def load_data(self, file_path):
        """Load the disease and symptom dataset"""
        print("Loading dataset...")
        self.df = pd.read_csv(file_path)
        print(f"Dataset loaded: {len(self.df)} diseases")
        print(f"Columns: {list(self.df.columns)}")
        return self.df
    
    def clean_text(self, text):
        """Clean and normalize text"""
        if pd.isna(text):
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
    
    def tokenize_symptoms(self, symptom_text):
        """Split symptoms by semicolon and clean each symptom"""
        if pd.isna(symptom_text):
            return []
        
        # Split by semicolon
        symptoms = [s.strip() for s in symptom_text.split(';')]
        
        # Clean each symptom
        cleaned_symptoms = []
        for symptom in symptoms:
            if symptom:  # Skip empty symptoms
                cleaned = self.clean_text(symptom)
                cleaned = self.standardize_medical_terms(cleaned)
                if cleaned:  # Only add non-empty symptoms
                    cleaned_symptoms.append(cleaned)
        
        return cleaned_symptoms
    
    def preprocess_symptoms(self):
        """Preprocess all symptoms in the dataset"""
        print("Preprocessing symptoms...")
        
        # Tokenize symptoms
        self.df['symptoms_list'] = self.df['Symptoms'].apply(self.tokenize_symptoms)
        
        # Create symptom count feature
        self.df['symptom_count'] = self.df['symptoms_list'].apply(len)
        
        # Create combined symptom text for TF-IDF
        self.df['symptoms_text'] = self.df['symptoms_list'].apply(' '.join)
        
        print(f"Average symptoms per disease: {self.df['symptom_count'].mean():.2f}")
        print(f"Min symptoms: {self.df['symptom_count'].min()}")
        print(f"Max symptoms: {self.df['symptom_count'].max()}")
        
        return self.df
    
    def create_tfidf_features(self, max_features=1000, min_df=1, max_df=0.95):
        """Create TF-IDF features from symptoms"""
        print("Creating TF-IDF features...")
        
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=max_features,
            min_df=min_df,
            max_df=max_df,
            stop_words=list(self.stop_words),
            ngram_range=(1, 2),  # Include unigrams and bigrams
            lowercase=True
        )
        
        # Fit and transform symptoms
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.df['symptoms_text'])
        
        # Convert to DataFrame for easier handling
        feature_names = self.tfidf_vectorizer.get_feature_names_out()
        self.tfidf_df = pd.DataFrame(
            tfidf_matrix.toarray(),
            columns=[f'tfidf_{name}' for name in feature_names],
            index=self.df.index
        )
        
        print(f"TF-IDF features created: {tfidf_matrix.shape}")
        print(f"Top 10 most important features:")
        feature_importance = np.mean(tfidf_matrix.toarray(), axis=0)
        top_features_idx = np.argsort(feature_importance)[-10:][::-1]
        for idx in top_features_idx:
            print(f"  {feature_names[idx]}: {feature_importance[idx]:.4f}")
        
        return self.tfidf_df
    
    def encode_labels(self):
        """Encode disease labels"""
        print("Encoding disease labels...")
        
        self.label_encoder = LabelEncoder()
        self.df['disease_encoded'] = self.label_encoder.fit_transform(self.df['Disease'])
        
        print(f"Number of unique diseases: {len(self.label_encoder.classes_)}")
        print("Disease classes:")
        for i, disease in enumerate(self.label_encoder.classes_):
            print(f"  {i}: {disease}")
        
        return self.df['disease_encoded']
    
    def create_additional_features(self):
        """Create additional engineered features"""
        print("Creating additional features...")
        
        # Body system classification based on symptoms
        body_systems = {
            'respiratory': ['cough', 'breath', 'chest', 'lung', 'nasal', 'throat', 'sneezing'],
            'cardiovascular': ['chest pain', 'heart', 'blood pressure', 'palpitation'],
            'gastrointestinal': ['abdominal', 'stomach', 'nausea', 'vomiting', 'diarrhea', 'constipation', 'appetite'],
            'genitourinary': ['urination', 'urine', 'pelvic', 'genital', 'kidney', 'bladder'],
            'neurological': ['headache', 'dizziness', 'confusion', 'seizure', 'numbness', 'weakness'],
            'dermatological': ['rash', 'itching', 'skin', 'lesion', 'swelling'],
            'musculoskeletal': ['joint', 'muscle', 'bone', 'back', 'neck', 'limb'],
            'endocrine': ['weight', 'thirst', 'urination', 'fatigue', 'temperature']
        }
        
        # Create body system features
        for system, keywords in body_systems.items():
            self.df[f'has_{system}_symptoms'] = self.df['symptoms_text'].apply(
                lambda x: any(keyword in x for keyword in keywords)
            ).astype(int)
        
        # Severity indicators
        severity_indicators = {
            'severe': ['severe', 'intense', 'acute', 'sudden', 'high fever', 'profound'],
            'mild': ['mild', 'low-grade', 'slight', 'minor', 'mild fever'],
            'chronic': ['chronic', 'persistent', 'recurrent', 'ongoing', 'long-term']
        }
        
        for severity, keywords in severity_indicators.items():
            self.df[f'has_{severity}_indicators'] = self.df['symptoms_text'].apply(
                lambda x: any(keyword in x for keyword in keywords)
            ).astype(int)
        
        # Symptom diversity (number of different body systems affected)
        system_columns = [col for col in self.df.columns if col.startswith('has_') and col.endswith('_symptoms')]
        self.df['symptom_diversity'] = self.df[system_columns].sum(axis=1)
        
        print("Additional features created:")
        print(f"  Body system features: {len(system_columns)}")
        print(f"  Severity features: {len(severity_indicators)}")
        print(f"  Average symptom diversity: {self.df['symptom_diversity'].mean():.2f}")
        
        return self.df
    
    def create_training_data(self):
        """Create final training dataset"""
        print("Creating training dataset...")
        
        # Combine all features
        feature_columns = []
        
        # Add TF-IDF features
        if hasattr(self, 'tfidf_df'):
            feature_columns.extend(self.tfidf_df.columns)
        
        # Add engineered features
        engineered_features = [
            'symptom_count', 'symptom_diversity',
            'has_respiratory_symptoms', 'has_cardiovascular_symptoms',
            'has_gastrointestinal_symptoms', 'has_genitourinary_symptoms',
            'has_neurological_symptoms', 'has_dermatological_symptoms',
            'has_musculoskeletal_symptoms', 'has_endocrine_symptoms',
            'has_severe_indicators', 'has_mild_indicators', 'has_chronic_indicators'
        ]
        
        # Create feature matrix
        if hasattr(self, 'tfidf_df'):
            X = pd.concat([self.tfidf_df, self.df[engineered_features]], axis=1)
        else:
            X = self.df[engineered_features]
        
        # Create labels
        y = self.df['disease_encoded']
        
        print(f"Training data shape: {X.shape}")
        print(f"Number of features: {X.shape[1]}")
        print(f"Number of classes: {len(np.unique(y))}")
        
        return X, y
    
    def save_processed_data(self, X, y, output_dir='processed_data'):
        """Save processed data and preprocessors"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"Saving processed data to {output_dir}/...")
        
        # Save feature matrix and labels
        X.to_csv(f'{output_dir}/features.csv', index=False)
        y.to_csv(f'{output_dir}/labels.csv', index=False)
        
        # Save preprocessed dataframe
        self.df.to_csv(f'{output_dir}/preprocessed_data.csv', index=False)
        
        # Save preprocessors
        if self.tfidf_vectorizer:
            with open(f'{output_dir}/tfidf_vectorizer.pkl', 'wb') as f:
                pickle.dump(self.tfidf_vectorizer, f)
        
        if self.label_encoder:
            with open(f'{output_dir}/label_encoder.pkl', 'wb') as f:
                pickle.dump(self.label_encoder, f)
        
        # Save preprocessing metadata
        metadata = {
            'num_diseases': len(self.df),
            'num_features': X.shape[1],
            'feature_names': list(X.columns),
            'disease_classes': list(self.label_encoder.classes_) if self.label_encoder else [],
            'medical_synonyms': self.medical_synonyms,
            'body_systems': {
                'respiratory': ['cough', 'breath', 'chest', 'lung', 'nasal', 'throat', 'sneezing'],
                'cardiovascular': ['chest pain', 'heart', 'blood pressure', 'palpitation'],
                'gastrointestinal': ['abdominal', 'stomach', 'nausea', 'vomiting', 'diarrhea', 'constipation', 'appetite'],
                'genitourinary': ['urination', 'urine', 'pelvic', 'genital', 'kidney', 'bladder'],
                'neurological': ['headache', 'dizziness', 'confusion', 'seizure', 'numbness', 'weakness'],
                'dermatological': ['rash', 'itching', 'skin', 'lesion', 'swelling'],
                'musculoskeletal': ['joint', 'muscle', 'bone', 'back', 'neck', 'limb'],
                'endocrine': ['weight', 'thirst', 'urination', 'fatigue', 'temperature']
            }
        }
        
        with open(f'{output_dir}/metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print("Data preprocessing completed successfully!")
        print(f"Files saved:")
        print(f"  - {output_dir}/features.csv (feature matrix)")
        print(f"  - {output_dir}/labels.csv (encoded labels)")
        print(f"  - {output_dir}/preprocessed_data.csv (full preprocessed dataset)")
        print(f"  - {output_dir}/tfidf_vectorizer.pkl (TF-IDF vectorizer)")
        print(f"  - {output_dir}/label_encoder.pkl (label encoder)")
        print(f"  - {output_dir}/metadata.json (preprocessing metadata)")
    
    def run_full_preprocessing(self, input_file, output_dir='processed_data'):
        """Run the complete preprocessing pipeline"""
        print("=" * 60)
        print("DISEASE-SYMPTOM DATA PREPROCESSING PIPELINE")
        print("=" * 60)
        
        # Load data
        self.load_data(input_file)
        
        # Preprocess symptoms
        self.preprocess_symptoms()
        
        # Create TF-IDF features
        self.create_tfidf_features()
        
        # Encode labels
        self.encode_labels()
        
        # Create additional features
        self.create_additional_features()
        
        # Create training data
        X, y = self.create_training_data()
        
        # Save processed data
        self.save_processed_data(X, y, output_dir)
        
        return X, y

def main():
    """Main function to run preprocessing"""
    preprocessor = DiseaseSymptomPreprocessor()
    
    # Run preprocessing
    X, y = preprocessor.run_full_preprocessing('disesaseandsymptom.csv')
    
    print("\n" + "=" * 60)
    print("PREPROCESSING SUMMARY")
    print("=" * 60)
    print(f"Original dataset: {len(preprocessor.df)} diseases")
    print(f"Feature matrix shape: {X.shape}")
    print(f"Number of classes: {len(np.unique(y))}")
    print(f"Average symptoms per disease: {preprocessor.df['symptom_count'].mean():.2f}")
    print(f"Feature types:")
    print(f"  - TF-IDF features: {len([col for col in X.columns if col.startswith('tfidf_')])}")
    print(f"  - Engineered features: {len([col for col in X.columns if not col.startswith('tfidf_')])}")
    
    return preprocessor, X, y

if __name__ == "__main__":
    preprocessor, X, y = main()

