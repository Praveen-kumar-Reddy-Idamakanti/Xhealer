import pandas as pd
import numpy as np
import pickle
import json
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    classification_report, accuracy_score,
    precision_score, recall_score, f1_score, top_k_accuracy_score
)
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class SimpleDiseaseTrainer:
    def __init__(self, data_path='augmented_data'):
        self.data_path = data_path
        self.models = {}
        self.results = {}
        self.scaler = StandardScaler()
        
    def load_data(self):
        """Load preprocessed features and labels"""
        print("Loading preprocessed data...")
        
        # Load features and labels
        self.X = pd.read_csv(f'{self.data_path}/features.csv')
        self.y = pd.read_csv(f'{self.data_path}/labels.csv').values.ravel()
        
        # Load metadata
        with open(f'{self.data_path}/metadata.json', 'r') as f:
            self.metadata = json.load(f)
        
        print(f"Data loaded successfully!")
        print(f"  Features shape: {self.X.shape}")
        print(f"  Labels shape: {self.y.shape}")
        print(f"  Number of classes: {len(np.unique(self.y))}")
        
        return self.X, self.y
    
    def split_data(self, test_size=0.2, random_state=42):
        """Split data into train/test sets"""
        print("Splitting data into train/test sets...")
        
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=test_size, random_state=random_state, stratify=self.y
        )
        
        print(f"Data split completed:")
        print(f"  Training set: {self.X_train.shape[0]} samples")
        print(f"  Test set: {self.X_test.shape[0]} samples")
        
        return self.X_train, self.X_test, self.y_train, self.y_test
    
    def scale_features(self):
        """Scale features for models that require it"""
        print("Scaling features...")
        
        # Fit scaler on training data
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)
        
        print("Features scaled successfully!")
        
        return self.X_train_scaled, self.X_test_scaled
    
    def train_models(self):
        """Train all models"""
        print("=" * 60)
        print("TRAINING MODELS")
        print("=" * 60)
        
        # 1. Naive Bayes (works well with TF-IDF features)
        print("Training Naive Bayes...")
        nb_model = MultinomialNB(alpha=1.0)
        nb_model.fit(self.X_train, self.y_train)
        self.models['Naive_Bayes'] = nb_model
        
        # 2. Support Vector Machine
        print("Training Support Vector Machine...")
        svm_model = SVC(kernel='linear', C=1.0, random_state=42, probability=True)
        svm_model.fit(self.X_train_scaled, self.y_train)
        self.models['SVM'] = svm_model
        
        # 3. Random Forest
        print("Training Random Forest...")
        rf_model = RandomForestClassifier(
            n_estimators=100, 
            max_depth=10, 
            random_state=42,
            class_weight='balanced'
        )
        rf_model.fit(self.X_train, self.y_train)
        self.models['Random_Forest'] = rf_model
        
        # 4. Logistic Regression
        print("Training Logistic Regression...")
        lr_model = LogisticRegression(
            C=1.0, 
            random_state=42, 
            max_iter=1000,
            class_weight='balanced'
        )
        lr_model.fit(self.X_train_scaled, self.y_train)
        self.models['Logistic_Regression'] = lr_model
        
        # 5. Neural Network
        print("Training Neural Network...")
        mlp_model = MLPClassifier(
            hidden_layer_sizes=(256, 128),
            activation='relu',
            solver='adam',
            alpha=0.001,
            batch_size=32,
            learning_rate='adaptive',
            max_iter=300,
            random_state=42,
            early_stopping=True,
            validation_fraction=0.1
        )
        mlp_model.fit(self.X_train_scaled, self.y_train)
        self.models['Neural_Network'] = mlp_model
        
        print("All models trained successfully!")
        
        return self.models
    
    def evaluate_model(self, model, model_name, X_test, y_test):
        """Evaluate a single model"""
        print(f"\nEvaluating {model_name}...")
        
        # Make predictions
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test) if hasattr(model, 'predict_proba') else None
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted')
        recall = recall_score(y_test, y_pred, average='weighted')
        f1 = f1_score(y_test, y_pred, average='weighted')
        
        # Top-k accuracy
        top3_accuracy = 0
        top5_accuracy = 0
        if y_pred_proba is not None:
            try:
                top3_accuracy = top_k_accuracy_score(y_test, y_pred_proba, k=3)
                top5_accuracy = top_k_accuracy_score(y_test, y_pred_proba, k=5)
            except:
                pass
        
        results = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'top3_accuracy': top3_accuracy,
            'top5_accuracy': top5_accuracy,
            'predictions': y_pred,
            'probabilities': y_pred_proba
        }
        
        print(f"  Accuracy: {accuracy:.4f}")
        print(f"  Precision: {precision:.4f}")
        print(f"  Recall: {recall:.4f}")
        print(f"  F1-Score: {f1:.4f}")
        print(f"  Top-3 Accuracy: {top3_accuracy:.4f}")
        print(f"  Top-5 Accuracy: {top5_accuracy:.4f}")
        
        return results
    
    def evaluate_all_models(self):
        """Evaluate all trained models"""
        print("=" * 60)
        print("EVALUATING ALL MODELS")
        print("=" * 60)
        
        # Determine which features to use for each model
        model_features = {
            'Naive_Bayes': (self.X_test, self.y_test),
            'Random_Forest': (self.X_test, self.y_test),
            'SVM': (self.X_test_scaled, self.y_test),
            'Logistic_Regression': (self.X_test_scaled, self.y_test),
            'Neural_Network': (self.X_test_scaled, self.y_test)
        }
        
        for model_name, model in self.models.items():
            X_test_model, y_test_model = model_features[model_name]
            self.results[model_name] = self.evaluate_model(model, model_name, X_test_model, y_test_model)
        
        return self.results
    
    def create_model_comparison(self):
        """Create comparison of all models"""
        print("=" * 60)
        print("MODEL COMPARISON")
        print("=" * 60)
        
        # Create comparison DataFrame
        comparison_data = []
        for model_name, results in self.results.items():
            comparison_data.append({
                'Model': model_name,
                'Accuracy': results['accuracy'],
                'Precision': results['precision'],
                'Recall': results['recall'],
                'F1-Score': results['f1_score'],
                'Top-3 Accuracy': results['top3_accuracy'],
                'Top-5 Accuracy': results['top5_accuracy']
            })
        
        comparison_df = pd.DataFrame(comparison_data)
        comparison_df = comparison_df.sort_values('Accuracy', ascending=False)
        
        print("\nModel Performance Comparison:")
        print(comparison_df.to_string(index=False, float_format='%.4f'))
        
        return comparison_df
    
    def save_models_and_results(self, output_dir='trained_models'):
        """Save all trained models and results"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"Saving models and results to {output_dir}/...")
        
        # Save individual models
        for model_name, model in self.models.items():
            filename = f'{output_dir}/{model_name.lower().replace(" ", "_")}_model.pkl'
            with open(filename, 'wb') as f:
                pickle.dump(model, f)
        
        # Save scaler
        with open(f'{output_dir}/scaler.pkl', 'wb') as f:
            pickle.dump(self.scaler, f)
        
        # Save results
        results_to_save = {}
        for model_name, results in self.results.items():
            results_to_save[model_name] = {
                'accuracy': results['accuracy'],
                'precision': results['precision'],
                'recall': results['recall'],
                'f1_score': results['f1_score'],
                'top3_accuracy': results['top3_accuracy'],
                'top5_accuracy': results['top5_accuracy']
            }
        
        with open(f'{output_dir}/model_results.json', 'w') as f:
            json.dump(results_to_save, f, indent=2)
        
        # Save training metadata
        training_metadata = {
            'training_date': datetime.now().isoformat(),
            'data_path': self.data_path,
            'train_samples': len(self.X_train),
            'test_samples': len(self.X_test),
            'num_features': self.X_train.shape[1],
            'num_classes': len(np.unique(self.y)),
            'models_trained': list(self.models.keys()),
            'best_model': max(self.results.items(), key=lambda x: x[1]['accuracy'])[0]
        }
        
        with open(f'{output_dir}/training_metadata.json', 'w') as f:
            json.dump(training_metadata, f, indent=2)
        
        print("Models and results saved successfully!")
        print(f"Files saved:")
        for model_name in self.models.keys():
            print(f"  - {output_dir}/{model_name.lower().replace(' ', '_')}_model.pkl")
        print(f"  - {output_dir}/scaler.pkl")
        print(f"  - {output_dir}/model_results.json")
        print(f"  - {output_dir}/training_metadata.json")
    
    def run_full_training(self):
        """Run the complete training pipeline"""
        print("=" * 80)
        print("DISEASE PREDICTION MODEL TRAINING PIPELINE")
        print("=" * 80)
        
        # Load data
        self.load_data()
        
        # Split data
        self.split_data()
        
        # Scale features
        self.scale_features()
        
        # Train models
        self.train_models()
        
        # Evaluate models
        self.evaluate_all_models()
        
        # Create comparison
        comparison_df = self.create_model_comparison()
        
        # Save models and results
        self.save_models_and_results()
        
        print("\n" + "=" * 80)
        print("TRAINING COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        
        return self.models, self.results, comparison_df

def main():
    """Main function to run training"""
    trainer = SimpleDiseaseTrainer()
    
    # Run full training pipeline
    models, results, comparison_df = trainer.run_full_training()
    
    # Print final summary
    print("\nFINAL TRAINING SUMMARY:")
    print("=" * 50)
    print(f"Models trained: {len(models)}")
    best_model_name = max(results.items(), key=lambda x: x[1]['accuracy'])[0]
    best_accuracy = max(results.items(), key=lambda x: x[1]['accuracy'])[1]['accuracy']
    print(f"Best model: {best_model_name}")
    print(f"Best accuracy: {best_accuracy:.4f}")
    
    return trainer, models, results, comparison_df

if __name__ == "__main__":
    trainer, models, results, comparison_df = main()

