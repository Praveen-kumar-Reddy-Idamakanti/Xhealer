import pandas as pd
import numpy as np
import random
from collections import defaultdict
import json

class DiseaseSymptomAugmenter:
    def __init__(self, processed_data_path='processed_data'):
        self.processed_data_path = processed_data_path
        self.df = None
        self.symptom_variations = {}
        self.body_system_symptoms = {}
        
    def load_processed_data(self):
        """Load the preprocessed data"""
        print("Loading preprocessed data...")
        self.df = pd.read_csv(f'{self.processed_data_path}/preprocessed_data.csv')
        
        # Load metadata
        with open(f'{self.processed_data_path}/metadata.json', 'r') as f:
            self.metadata = json.load(f)
        
        print(f"Loaded {len(self.df)} diseases")
        return self.df
    
    def create_symptom_variations(self):
        """Create variations of common symptoms"""
        print("Creating symptom variations...")
        
        # Common symptom variations
        self.symptom_variations = {
            'pain': ['ache', 'discomfort', 'soreness', 'tenderness'],
            'fever': ['high temperature', 'elevated temperature', 'pyrexia'],
            'nausea': ['feeling sick', 'queasy', 'sick to stomach'],
            'vomiting': ['throwing up', 'puking', 'emesis'],
            'fatigue': ['tiredness', 'exhaustion', 'weakness', 'lethargy'],
            'headache': ['head pain', 'cephalgia', 'head ache'],
            'cough': ['coughing', 'hacking', 'productive cough', 'dry cough'],
            'shortness of breath': ['difficulty breathing', 'trouble breathing', 'dyspnea'],
            'chest pain': ['chest discomfort', 'chest pressure', 'thoracic pain'],
            'abdominal pain': ['stomach pain', 'belly ache', 'tummy pain'],
            'diarrhea': ['loose stools', 'watery stools', 'frequent bowel movements'],
            'constipation': ['hard stools', 'difficulty passing stool', 'infrequent bowel movements'],
            'rash': ['skin rash', 'eruption', 'skin irritation'],
            'itching': ['pruritus', 'scratching', 'itchy sensation'],
            'swelling': ['edema', 'inflammation', 'puffiness'],
            'bleeding': ['hemorrhage', 'blood loss', 'hemorrhaging'],
            'dizziness': ['lightheadedness', 'vertigo', 'feeling faint'],
            'weight loss': ['unintended weight loss', 'weight reduction', 'slimming'],
            'weight gain': ['weight increase', 'weight addition', 'gaining weight'],
            'loss of appetite': ['decreased appetite', 'poor appetite', 'anorexia']
        }
        
        print(f"Created variations for {len(self.symptom_variations)} symptoms")
        return self.symptom_variations
    
    def create_body_system_symptoms(self):
        """Create body system symptom mappings"""
        print("Creating body system symptom mappings...")
        
        self.body_system_symptoms = {
            'respiratory': [
                'cough', 'shortness of breath', 'chest pain', 'wheezing', 'sneezing',
                'runny nose', 'stuffy nose', 'sore throat', 'nasal congestion'
            ],
            'cardiovascular': [
                'chest pain', 'shortness of breath', 'palpitations', 'dizziness',
                'fatigue', 'swelling in legs', 'rapid heartbeat'
            ],
            'gastrointestinal': [
                'abdominal pain', 'nausea', 'vomiting', 'diarrhea', 'constipation',
                'loss of appetite', 'bloating', 'belching', 'heartburn'
            ],
            'genitourinary': [
                'painful urination', 'frequent urination', 'blood in urine',
                'pelvic pain', 'genital discharge', 'vaginal bleeding'
            ],
            'neurological': [
                'headache', 'dizziness', 'confusion', 'numbness', 'weakness',
                'seizures', 'memory problems', 'difficulty concentrating'
            ],
            'dermatological': [
                'rash', 'itching', 'skin lesions', 'swelling', 'redness',
                'dry skin', 'skin discoloration'
            ],
            'musculoskeletal': [
                'joint pain', 'muscle pain', 'back pain', 'stiffness',
                'swelling', 'limited range of motion'
            ],
            'endocrine': [
                'weight changes', 'fatigue', 'thirst', 'frequent urination',
                'temperature intolerance', 'mood changes'
            ]
        }
        
        print(f"Created mappings for {len(self.body_system_symptoms)} body systems")
        return self.body_system_symptoms
    
    def augment_symptom_list(self, symptoms_list, augmentation_factor=2):
        """Augment a single symptom list"""
        augmented_lists = [symptoms_list]  # Start with original
        
        for _ in range(augmentation_factor):
            new_symptoms = []
            
            for symptom in symptoms_list:
                # Sometimes replace with variation
                if random.random() < 0.3 and symptom in self.symptom_variations:
                    variation = random.choice(self.symptom_variations[symptom])
                    new_symptoms.append(variation)
                else:
                    new_symptoms.append(symptom)
            
            # Sometimes add related symptoms from same body system
            if random.random() < 0.4:
                # Find which body systems are affected
                affected_systems = []
                for system, system_symptoms in self.body_system_symptoms.items():
                    if any(symptom in system_symptoms for symptom in symptoms_list):
                        affected_systems.append(system)
                
                # Add a related symptom
                if affected_systems:
                    system = random.choice(affected_systems)
                    related_symptoms = [s for s in self.body_system_symptoms[system] 
                                      if s not in new_symptoms]
                    if related_symptoms:
                        new_symptoms.append(random.choice(related_symptoms))
            
            # Sometimes remove a symptom (partial symptom lists)
            if len(new_symptoms) > 3 and random.random() < 0.2:
                new_symptoms.remove(random.choice(new_symptoms))
            
            # Sometimes reorder symptoms
            if random.random() < 0.3:
                random.shuffle(new_symptoms)
            
            augmented_lists.append(new_symptoms)
        
        return augmented_lists
    
    def augment_dataset(self, augmentation_factor=3):
        """Augment the entire dataset"""
        print(f"Augmenting dataset with factor {augmentation_factor}...")
        
        augmented_data = []
        
        for idx, row in self.df.iterrows():
            disease = row['Disease']
            symptoms_list = eval(row['symptoms_list'])  # Convert string back to list
            
            # Create augmented versions
            augmented_lists = self.augment_symptom_list(symptoms_list, augmentation_factor)
            
            for i, aug_symptoms in enumerate(augmented_lists):
                if i == 0:  # Original
                    augmented_data.append({
                        'Disease': disease,
                        'Symptoms': '; '.join(aug_symptoms),
                        'symptoms_list': str(aug_symptoms),
                        'symptoms_text': ' '.join(aug_symptoms),
                        'symptom_count': len(aug_symptoms),
                        'is_augmented': False,
                        'original_index': idx
                    })
                else:  # Augmented
                    augmented_data.append({
                        'Disease': disease,
                        'Symptoms': '; '.join(aug_symptoms),
                        'symptoms_list': str(aug_symptoms),
                        'symptoms_text': ' '.join(aug_symptoms),
                        'symptom_count': len(aug_symptoms),
                        'is_augmented': True,
                        'original_index': idx
                    })
        
        self.augmented_df = pd.DataFrame(augmented_data)
        print(f"Dataset augmented: {len(self.augmented_df)} total samples")
        print(f"  Original: {len(self.augmented_df[~self.augmented_df['is_augmented']])}")
        print(f"  Augmented: {len(self.augmented_df[self.augmented_df['is_augmented']])}")
        
        return self.augmented_df
    
    def create_partial_symptom_sets(self, partial_factors=[0.6, 0.7, 0.8]):
        """Create partial symptom sets for more realistic scenarios"""
        print("Creating partial symptom sets...")
        
        partial_data = []
        
        for idx, row in self.df.iterrows():
            disease = row['Disease']
            symptoms_list = eval(row['symptoms_list'])
            
            for factor in partial_factors:
                # Select a subset of symptoms
                num_symptoms = max(2, int(len(symptoms_list) * factor))
                partial_symptoms = random.sample(symptoms_list, num_symptoms)
                
                partial_data.append({
                    'Disease': disease,
                    'Symptoms': '; '.join(partial_symptoms),
                    'symptoms_list': str(partial_symptoms),
                    'symptoms_text': ' '.join(partial_symptoms),
                    'symptom_count': len(partial_symptoms),
                    'is_augmented': True,
                    'is_partial': True,
                    'partial_factor': factor,
                    'original_index': idx
                })
        
        self.partial_df = pd.DataFrame(partial_data)
        print(f"Created {len(self.partial_df)} partial symptom sets")
        
        return self.partial_df
    
    def create_noisy_symptoms(self, noise_probability=0.1):
        """Create noisy versions with typos and variations"""
        print("Creating noisy symptom versions...")
        
        # Common typos and variations
        noise_patterns = {
            'pain': ['pian', 'pane', 'pian'],
            'fever': ['fevr', 'fever', 'fevre'],
            'nausea': ['nausia', 'nausa', 'nasea'],
            'vomiting': ['vomitting', 'vomiting', 'vomiting'],
            'fatigue': ['fatige', 'fatigue', 'fatigue'],
            'headache': ['headach', 'headache', 'head ache'],
            'cough': ['cough', 'coughing', 'cough'],
            'abdominal': ['abdomnal', 'abdominal', 'abdominal'],
            'chest': ['chest', 'chest', 'chest'],
            'shortness': ['shortnes', 'shortness', 'shortness']
        }
        
        noisy_data = []
        
        for idx, row in self.df.iterrows():
            disease = row['Disease']
            symptoms_list = eval(row['symptoms_list'])
            
            # Create noisy version
            noisy_symptoms = []
            for symptom in symptoms_list:
                if random.random() < noise_probability and symptom in noise_patterns:
                    noisy_symptoms.append(random.choice(noise_patterns[symptom]))
                else:
                    noisy_symptoms.append(symptom)
            
            noisy_data.append({
                'Disease': disease,
                'Symptoms': '; '.join(noisy_symptoms),
                'symptoms_list': str(noisy_symptoms),
                'symptoms_text': ' '.join(noisy_symptoms),
                'symptom_count': len(noisy_symptoms),
                'is_augmented': True,
                'is_noisy': True,
                'original_index': idx
            })
        
        self.noisy_df = pd.DataFrame(noisy_data)
        print(f"Created {len(self.noisy_df)} noisy symptom versions")
        
        return self.noisy_df
    
    def combine_all_augmentations(self):
        """Combine all augmentation strategies"""
        print("Combining all augmentation strategies...")
        
        # Start with original data
        combined_df = self.df.copy()
        combined_df['is_augmented'] = False
        combined_df['augmentation_type'] = 'original'
        
        # Add augmented data
        if hasattr(self, 'augmented_df'):
            aug_df = self.augmented_df[self.augmented_df['is_augmented']].copy()
            aug_df['augmentation_type'] = 'symptom_variation'
            combined_df = pd.concat([combined_df, aug_df], ignore_index=True)
        
        # Add partial data
        if hasattr(self, 'partial_df'):
            partial_df = self.partial_df.copy()
            partial_df['augmentation_type'] = 'partial_symptoms'
            combined_df = pd.concat([combined_df, partial_df], ignore_index=True)
        
        # Add noisy data
        if hasattr(self, 'noisy_df'):
            noisy_df = self.noisy_df.copy()
            noisy_df['augmentation_type'] = 'noisy_symptoms'
            combined_df = pd.concat([combined_df, noisy_df], ignore_index=True)
        
        self.combined_df = combined_df
        print(f"Combined dataset: {len(self.combined_df)} total samples")
        print("Augmentation breakdown:")
        print(combined_df['augmentation_type'].value_counts())
        
        return self.combined_df
    
    def save_augmented_data(self, output_dir='augmented_data'):
        """Save augmented dataset"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"Saving augmented data to {output_dir}/...")
        
        # Save combined dataset
        self.combined_df.to_csv(f'{output_dir}/augmented_dataset.csv', index=False)
        
        # Save individual augmentation types
        if hasattr(self, 'augmented_df'):
            self.augmented_df.to_csv(f'{output_dir}/symptom_variations.csv', index=False)
        
        if hasattr(self, 'partial_df'):
            self.partial_df.to_csv(f'{output_dir}/partial_symptoms.csv', index=False)
        
        if hasattr(self, 'noisy_df'):
            self.noisy_df.to_csv(f'{output_dir}/noisy_symptoms.csv', index=False)
        
        # Save augmentation metadata
        augmentation_metadata = {
            'original_samples': len(self.df),
            'total_augmented_samples': len(self.combined_df),
            'augmentation_factor': len(self.combined_df) / len(self.df),
            'augmentation_types': {
                'symptom_variations': len(self.combined_df[self.combined_df['augmentation_type'] == 'symptom_variation']),
                'partial_symptoms': len(self.combined_df[self.combined_df['augmentation_type'] == 'partial_symptoms']),
                'noisy_symptoms': len(self.combined_df[self.combined_df['augmentation_type'] == 'noisy_symptoms']),
                'original': len(self.combined_df[self.combined_df['augmentation_type'] == 'original'])
            },
            'symptom_variations': self.symptom_variations,
            'body_system_symptoms': self.body_system_symptoms
        }
        
        with open(f'{output_dir}/augmentation_metadata.json', 'w') as f:
            json.dump(augmentation_metadata, f, indent=2)
        
        print("Augmented data saved successfully!")
        print(f"Files saved:")
        print(f"  - {output_dir}/augmented_dataset.csv (complete augmented dataset)")
        print(f"  - {output_dir}/symptom_variations.csv (symptom variation augmentations)")
        print(f"  - {output_dir}/partial_symptoms.csv (partial symptom sets)")
        print(f"  - {output_dir}/noisy_symptoms.csv (noisy symptom versions)")
        print(f"  - {output_dir}/augmentation_metadata.json (augmentation metadata)")
    
    def run_full_augmentation(self, augmentation_factor=3):
        """Run the complete augmentation pipeline"""
        print("=" * 60)
        print("DISEASE-SYMPTOM DATA AUGMENTATION PIPELINE")
        print("=" * 60)
        
        # Load data
        self.load_processed_data()
        
        # Create variations and mappings
        self.create_symptom_variations()
        self.create_body_system_symptoms()
        
        # Apply augmentation strategies
        self.augment_dataset(augmentation_factor)
        self.create_partial_symptom_sets()
        self.create_noisy_symptoms()
        
        # Combine all augmentations
        self.combine_all_augmentations()
        
        # Save augmented data
        self.save_augmented_data()
        
        return self.combined_df

def main():
    """Main function to run augmentation"""
    augmenter = DiseaseSymptomAugmenter()
    
    # Run augmentation
    augmented_df = augmenter.run_full_augmentation(augmentation_factor=3)
    
    print("\n" + "=" * 60)
    print("AUGMENTATION SUMMARY")
    print("=" * 60)
    print(f"Original dataset: {len(augmenter.df)} diseases")
    print(f"Augmented dataset: {len(augmented_df)} total samples")
    print(f"Augmentation factor: {len(augmented_df) / len(augmenter.df):.2f}x")
    print("\nAugmentation breakdown:")
    print(augmented_df['augmentation_type'].value_counts())
    
    return augmenter, augmented_df

if __name__ == "__main__":
    augmenter, augmented_df = main()

