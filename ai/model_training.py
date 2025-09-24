import pandas as pd
import numpy as np
import pickle
import json
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    classification_report, confusion_matrix, accuracy_score,
    precision_score, recall_score, f1_score, top_k_accuracy_score
)
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class DiseasePredictionTrainer:
    def __init__(self, data_path='augmented_data'):
        self.data_path = data_path
        self.models = {}
        self.results = {}
        self.scaler = StandardScaler()
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.X_val = None
        self.y_val = None
        
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
        print(f"  Class distribution:")
        
        unique, counts = np.unique(self.y, return_counts=True)
        for i, (cls, count) in enumerate(zip(unique, counts)):
            if i < 10:  # Show first 10 classes
                print(f"    Class {cls}: {count} samples")
        
        return self.X, self.y
    
    def split_data(self, test_size=0.2, val_size=0.2, random_state=42):
        """Split data into train/validation/test sets"""
        print("Splitting data into train/validation/test sets...")
        
        # First split: train+val vs test
        X_temp, self.X_test, y_temp, self.y_test = train_test_split(
            self.X, self.y, test_size=test_size, random_state=random_state, stratify=self.y
        )
        
        # Second split: train vs val
        self.X_train, self.X_val, self.y_train, self.y_val = train_test_split(
            X_temp, y_temp, test_size=val_size/(1-test_size), 
            random_state=random_state, stratify=y_temp
        )
        
        print(f"Data split completed:")
        print(f"  Training set: {self.X_train.shape[0]} samples")
        print(f"  Validation set: {self.X_val.shape[0]} samples")
        print(f"  Test set: {self.X_test.shape[0]} samples")
        
        return self.X_train, self.X_val, self.X_test, self.y_train, self.y_val, self.y_test
    
    def scale_features(self):
        """Scale features for models that require it"""
        print("Scaling features...")
        
        # Fit scaler on training data
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_val_scaled = self.scaler.transform(self.X_val)
        self.X_test_scaled = self.scaler.transform(self.X_test)
        
        print("Features scaled successfully!")
        
        return self.X_train_scaled, self.X_val_scaled, self.X_test_scaled
    
    def train_baseline_models(self):
        """Train baseline models"""
        print("=" * 60)
        print("TRAINING BASELINE MODELS")
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
        
        print("Baseline models trained successfully!")
        
        return self.models
    
    def train_neural_network(self):
        """Train neural network model"""
        print("=" * 60)
        print("TRAINING NEURAL NETWORK")
        print("=" * 60)
        
        # Multi-layer Perceptron
        print("Training Multi-layer Perceptron...")
        mlp_model = MLPClassifier(
            hidden_layer_sizes=(512, 256, 128),
            activation='relu',
            solver='adam',
            alpha=0.001,
            batch_size=32,
            learning_rate='adaptive',
            max_iter=500,
            random_state=42,
            early_stopping=True,
            validation_fraction=0.1
        )
        
        mlp_model.fit(self.X_train_scaled, self.y_train)
        self.models['Neural_Network'] = mlp_model
        
        print("Neural network trained successfully!")
        
        return mlp_model
    
    def create_ensemble_model(self):
        """Create ensemble model combining best models"""
        print("=" * 60)
        print("CREATING ENSEMBLE MODEL")
        print("=" * 60)
        
        # Create a custom ensemble that handles different feature types
        class CustomEnsemble:
            def __init__(self, models, scaler):
                self.models = models
                self.scaler = scaler
                
            def predict(self, X):
                predictions = []
                
                # Naive Bayes and Random Forest use original features
                nb_pred = self.models['Naive_Bayes'].predict(X)
                rf_pred = self.models['Random_Forest'].predict(X)
                
                # SVM, LR, and MLP use scaled features
                X_scaled = self.scaler.transform(X)
                svm_pred = self.models['SVM'].predict(X_scaled)
                lr_pred = self.models['Logistic_Regression'].predict(X_scaled)
                mlp_pred = self.models['Neural_Network'].predict(X_scaled)
                
                # Combine predictions using majority voting
                for i in range(len(X)):
                    votes = [nb_pred[i], rf_pred[i], svm_pred[i], lr_pred[i], mlp_pred[i]]
                    prediction = max(set(votes), key=votes.count)
                    predictions.append(prediction)
                
                return np.array(predictions)
            
            def predict_proba(self, X):
                # Get probabilities from models that support it
                X_scaled = self.scaler.transform(X)
                
                # Get probabilities from models that support it
                probas = []
                if hasattr(self.models['Naive_Bayes'], 'predict_proba'):
                    probas.append(self.models['Naive_Bayes'].predict_proba(X))
                if hasattr(self.models['Random_Forest'], 'predict_proba'):
                    probas.append(self.models['Random_Forest'].predict_proba(X))
                if hasattr(self.models['SVM'], 'predict_proba'):
                    probas.append(self.models['SVM'].predict_proba(X_scaled))
                if hasattr(self.models['Logistic_Regression'], 'predict_proba'):
                    probas.append(self.models['Logistic_Regression'].predict_proba(X_scaled))
                if hasattr(self.models['Neural_Network'], 'predict_proba'):
                    probas.append(self.models['Neural_Network'].predict_proba(X_scaled))
                
                # Average the probabilities
                if probas:
                    return np.mean(probas, axis=0)
                else:
                    # Fallback to predictions
                    predictions = self.predict(X)
                    # Convert to one-hot encoding
                    n_classes = len(np.unique(predictions))
                    proba = np.zeros((len(predictions), n_classes))
                    for i, pred in enumerate(predictions):
                        proba[i, pred] = 1.0
                    return proba
        
        ensemble_model = CustomEnsemble(self.models, self.scaler)
        self.models['Ensemble'] = ensemble_model
        
        print("Ensemble model created successfully!")
        
        return ensemble_model
    
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
        top3_accuracy = top_k_accuracy_score(y_test, y_pred_proba, k=3) if y_pred_proba is not None else 0
        top5_accuracy = top_k_accuracy_score(y_test, y_pred_proba, k=5) if y_pred_proba is not None else 0
        
        # Cross-validation score (use fewer folds due to small dataset)
        try:
            cv_scores = cross_val_score(model, X_test, y_test, cv=3, scoring='accuracy')
        except ValueError:
            # If still too few samples, use 2-fold or skip CV
            try:
                cv_scores = cross_val_score(model, X_test, y_test, cv=2, scoring='accuracy')
            except ValueError:
                cv_scores = np.array([accuracy])  # Use test accuracy as fallback
        
        results = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'top3_accuracy': top3_accuracy,
            'top5_accuracy': top5_accuracy,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'predictions': y_pred,
            'probabilities': y_pred_proba
        }
        
        print(f"  Accuracy: {accuracy:.4f}")
        print(f"  Precision: {precision:.4f}")
        print(f"  Recall: {recall:.4f}")
        print(f"  F1-Score: {f1:.4f}")
        print(f"  Top-3 Accuracy: {top3_accuracy:.4f}")
        print(f"  Top-5 Accuracy: {top5_accuracy:.4f}")
        print(f"  CV Score: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        
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
            'Neural_Network': (self.X_test_scaled, self.y_test),
            'Ensemble': (self.X_test, self.y_test)  # Custom ensemble uses original features
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
                'Top-5 Accuracy': results['top5_accuracy'],
                'CV Score': results['cv_mean']
            })
        
        comparison_df = pd.DataFrame(comparison_data)
        comparison_df = comparison_df.sort_values('Accuracy', ascending=False)
        
        print("\nModel Performance Comparison:")
        print(comparison_df.to_string(index=False, float_format='%.4f'))
        
        return comparison_df
    
    def plot_model_comparison(self, comparison_df):
        """Plot model comparison"""
        print("Creating model comparison plots...")
        
        # Set up the plotting style
        plt.style.use('default')
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Model Performance Comparison', fontsize=16, fontweight='bold')
        
        # Accuracy comparison
        axes[0, 0].bar(comparison_df['Model'], comparison_df['Accuracy'], color='skyblue')
        axes[0, 0].set_title('Accuracy Comparison')
        axes[0, 0].set_ylabel('Accuracy')
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # F1-Score comparison
        axes[0, 1].bar(comparison_df['Model'], comparison_df['F1-Score'], color='lightgreen')
        axes[0, 1].set_title('F1-Score Comparison')
        axes[0, 1].set_ylabel('F1-Score')
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # Top-k Accuracy comparison
        x = np.arange(len(comparison_df))
        width = 0.35
        axes[1, 0].bar(x - width/2, comparison_df['Top-3 Accuracy'], width, label='Top-3', color='orange')
        axes[1, 0].bar(x + width/2, comparison_df['Top-5 Accuracy'], width, label='Top-5', color='red')
        axes[1, 0].set_title('Top-K Accuracy Comparison')
        axes[1, 0].set_ylabel('Accuracy')
        axes[1, 0].set_xticks(x)
        axes[1, 0].set_xticklabels(comparison_df['Model'], rotation=45)
        axes[1, 0].legend()
        
        # Cross-validation score comparison
        axes[1, 1].bar(comparison_df['Model'], comparison_df['CV Score'], color='purple')
        axes[1, 1].set_title('Cross-Validation Score Comparison')
        axes[1, 1].set_ylabel('CV Score')
        axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('model_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("Model comparison plots saved as 'model_comparison.png'")
    
    def create_confusion_matrix(self, model_name, model, X_test, y_test):
        """Create confusion matrix for a model"""
        y_pred = model.predict(X_test)
        
        plt.figure(figsize=(12, 10))
        cm = confusion_matrix(y_test, y_pred)
        
        # Get class names
        class_names = self.metadata['disease_classes']
        
        # Plot confusion matrix
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=class_names, yticklabels=class_names)
        plt.title(f'Confusion Matrix - {model_name}')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        plt.savefig(f'confusion_matrix_{model_name.lower().replace(" ", "_")}.png', 
                   dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"Confusion matrix saved for {model_name}")
    
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
                'top5_accuracy': results['top5_accuracy'],
                'cv_mean': results['cv_mean'],
                'cv_std': results['cv_std']
            }
        
        with open(f'{output_dir}/model_results.json', 'w') as f:
            json.dump(results_to_save, f, indent=2)
        
        # Save training metadata
        training_metadata = {
            'training_date': datetime.now().isoformat(),
            'data_path': self.data_path,
            'train_samples': len(self.X_train),
            'val_samples': len(self.X_val),
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
        self.train_baseline_models()
        self.train_neural_network()
        self.create_ensemble_model()
        
        # Evaluate models
        self.evaluate_all_models()
        
        # Create comparison
        comparison_df = self.create_model_comparison()
        
        # Plot results
        self.plot_model_comparison(comparison_df)
        
        # Save models and results
        self.save_models_and_results()
        
        print("\n" + "=" * 80)
        print("TRAINING COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        
        return self.models, self.results, comparison_df

def main():
    """Main function to run training"""
    trainer = DiseasePredictionTrainer()
    
    # Run full training pipeline
    models, results, comparison_df = trainer.run_full_training()
    
    # Print final summary
    print("\nFINAL TRAINING SUMMARY:")
    print("=" * 50)
    print(f"Models trained: {len(models)}")
    print(f"Best model: {max(results.items(), key=lambda x: x[1]['accuracy'])[0]}")
    print(f"Best accuracy: {max(results.items(), key=lambda x: x[1]['accuracy'])[1]['accuracy']:.4f}")
    
    return trainer, models, results, comparison_df

if __name__ == "__main__":
    trainer, models, results, comparison_df = main()
