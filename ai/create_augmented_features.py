import pandas as pd
import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
import json

def create_features_for_augmented_data():
    """Create TF-IDF features for the augmented dataset"""
    print("=" * 60)
    print("CREATING FEATURES FOR AUGMENTED DATASET")
    print("=" * 60)
    
    # Load augmented dataset
    print("Loading augmented dataset...")
    augmented_df = pd.read_csv('augmented_data/augmented_dataset.csv')
    print(f"Augmented dataset shape: {augmented_df.shape}")
    
    # Load original preprocessors
    print("Loading original preprocessors...")
    with open('processed_data/tfidf_vectorizer.pkl', 'rb') as f:
        tfidf_vectorizer = pickle.load(f)
    
    with open('processed_data/label_encoder.pkl', 'rb') as f:
        label_encoder = pickle.load(f)
    
    # Create TF-IDF features for augmented data
    print("Creating TF-IDF features for augmented data...")
    tfidf_matrix = tfidf_vectorizer.transform(augmented_df['symptoms_text'])
    
    # Convert to DataFrame
    feature_names = tfidf_vectorizer.get_feature_names_out()
    tfidf_df = pd.DataFrame(
        tfidf_matrix.toarray(),
        columns=[f'tfidf_{name}' for name in feature_names],
        index=augmented_df.index
    )
    
    print(f"TF-IDF features shape: {tfidf_df.shape}")
    
    # Create additional features for augmented data
    print("Creating additional features...")
    
    # Body system features
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
        augmented_df[f'has_{system}_symptoms'] = augmented_df['symptoms_text'].apply(
            lambda x: any(keyword in x for keyword in keywords)
        ).astype(int)
    
    # Severity indicators
    severity_indicators = {
        'severe': ['severe', 'intense', 'acute', 'sudden', 'high fever', 'profound'],
        'mild': ['mild', 'low-grade', 'slight', 'minor', 'mild fever'],
        'chronic': ['chronic', 'persistent', 'recurrent', 'ongoing', 'long-term']
    }
    
    for severity, keywords in severity_indicators.items():
        augmented_df[f'has_{severity}_indicators'] = augmented_df['symptoms_text'].apply(
            lambda x: any(keyword in x for keyword in keywords)
        ).astype(int)
    
    # Symptom diversity
    system_columns = [col for col in augmented_df.columns if col.startswith('has_') and col.endswith('_symptoms')]
    augmented_df['symptom_diversity'] = augmented_df[system_columns].sum(axis=1)
    
    # Encode labels
    print("Encoding labels...")
    augmented_df['disease_encoded'] = label_encoder.transform(augmented_df['Disease'])
    
    # Create final feature matrix
    print("Creating final feature matrix...")
    engineered_features = [
        'symptom_count', 'symptom_diversity',
        'has_respiratory_symptoms', 'has_cardiovascular_symptoms',
        'has_gastrointestinal_symptoms', 'has_genitourinary_symptoms',
        'has_neurological_symptoms', 'has_dermatological_symptoms',
        'has_musculoskeletal_symptoms', 'has_endocrine_symptoms',
        'has_severe_indicators', 'has_mild_indicators', 'has_chronic_indicators'
    ]
    
    # Combine TF-IDF and engineered features
    X = pd.concat([tfidf_df, augmented_df[engineered_features]], axis=1)
    y = augmented_df['disease_encoded']
    
    print(f"Final feature matrix shape: {X.shape}")
    print(f"Number of classes: {len(np.unique(y))}")
    
    # Save augmented features
    print("Saving augmented features...")
    import os
    os.makedirs('augmented_data', exist_ok=True)
    
    X.to_csv('augmented_data/features.csv', index=False)
    y.to_csv('augmented_data/labels.csv', index=False)
    augmented_df.to_csv('augmented_data/processed_augmented_data.csv', index=False)
    
    # Save preprocessors
    with open('augmented_data/tfidf_vectorizer.pkl', 'wb') as f:
        pickle.dump(tfidf_vectorizer, f)
    
    with open('augmented_data/label_encoder.pkl', 'wb') as f:
        pickle.dump(label_encoder, f)
    
    # Create metadata
    metadata = {
        'num_samples': len(augmented_df),
        'num_features': X.shape[1],
        'num_classes': len(np.unique(y)),
        'augmentation_breakdown': augmented_df['augmentation_type'].value_counts().to_dict(),
        'feature_names': list(X.columns),
        'disease_classes': list(label_encoder.classes_)
    }
    
    with open('augmented_data/metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("Augmented features created successfully!")
    print(f"Files saved:")
    print(f"  - augmented_data/features.csv (feature matrix)")
    print(f"  - augmented_data/labels.csv (encoded labels)")
    print(f"  - augmented_data/processed_augmented_data.csv (full dataset)")
    print(f"  - augmented_data/tfidf_vectorizer.pkl (TF-IDF vectorizer)")
    print(f"  - augmented_data/label_encoder.pkl (label encoder)")
    print(f"  - augmented_data/metadata.json (metadata)")
    
    return X, y, augmented_df

if __name__ == "__main__":
    X, y, augmented_df = create_features_for_augmented_data()
    
    print("\n" + "=" * 60)
    print("AUGMENTED FEATURES SUMMARY")
    print("=" * 60)
    print(f"Total samples: {len(augmented_df)}")
    print(f"Feature matrix shape: {X.shape}")
    print(f"Number of classes: {len(np.unique(y))}")
    print(f"Augmentation breakdown:")
    print(augmented_df['augmentation_type'].value_counts())

