from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from disease_predictor import DiseasePredictor
from medical_dictionary import MedicalDictionary
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the disease predictor
predictor = DiseasePredictor()

# Initialize the medical dictionary
medical_dict = MedicalDictionary()

# Load models on startup
if not predictor.load_models():
    print("Warning: Failed to load models. API may not work correctly.")

print(f"Medical Dictionary loaded with {len(medical_dict.get_all_diseases())} diseases")

def _determine_urgency_level(confidence_percentage, disease_name):
    """
    Determine urgency level based on confidence and disease type
    
    Args:
        confidence_percentage: Confidence percentage (0-100)
        disease_name: Name of the disease
        
    Returns:
        Urgency level: 'low', 'moderate', 'high', or 'emergency'
    """
    # High-risk diseases that require immediate attention
    emergency_diseases = ['pneumonia', 'heart_attack', 'stroke', 'severe_allergic_reaction']
    high_risk_diseases = ['influenza', 'bronchitis', 'asthma', 'diabetes', 'hypertension']
    
    disease_lower = disease_name.lower()
    
    # Emergency conditions
    if any(emerg_disease in disease_lower for emerg_disease in emergency_diseases):
        return 'emergency'
    
    # High-risk conditions with high confidence
    if any(high_disease in disease_lower for high_disease in high_risk_diseases) and confidence_percentage > 70:
        return 'high'
    
    # High confidence predictions
    if confidence_percentage > 80:
        return 'high'
    elif confidence_percentage > 60:
        return 'moderate'
    else:
        return 'low'

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Disease Prediction System</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #34495e;
        }
        textarea {
            width: 100%;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
            resize: vertical;
            min-height: 100px;
        }
        textarea:focus {
            outline: none;
            border-color: #3498db;
        }
        button {
            background-color: #3498db;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
        }
        button:hover {
            background-color: #2980b9;
        }
        button:disabled {
            background-color: #bdc3c7;
            cursor: not-allowed;
        }
        .result {
            margin-top: 30px;
            padding: 20px;
            border-radius: 5px;
            display: none;
        }
        .success {
            background-color: #d5f4e6;
            border: 1px solid #27ae60;
        }
        .error {
            background-color: #fadbd8;
            border: 1px solid #e74c3c;
        }
        .prediction-item {
            background: white;
            margin: 10px 0;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #3498db;
        }
        .prediction-item.rank-1 {
            border-left-color: #e74c3c;
            background-color: #fdf2f2;
        }
        .prediction-item.rank-2 {
            border-left-color: #f39c12;
            background-color: #fef9e7;
        }
        .prediction-item.rank-3 {
            border-left-color: #27ae60;
            background-color: #eafaf1;
        }
        .confidence-bar {
            width: 100%;
            height: 20px;
            background-color: #ecf0f1;
            border-radius: 10px;
            overflow: hidden;
            margin: 5px 0;
        }
        .confidence-fill {
            height: 100%;
            background: linear-gradient(90deg, #e74c3c, #f39c12, #27ae60);
            transition: width 0.3s ease;
        }
        .loading {
            text-align: center;
            color: #7f8c8d;
        }
        .disclaimer {
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
            font-size: 14px;
            color: #856404;
        }
        .example {
            background-color: #e8f4fd;
            border: 1px solid #bee5eb;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .example h3 {
            margin-top: 0;
            color: #0c5460;
        }
        .example p {
            margin: 5px 0;
            color: #0c5460;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏥 Disease Prediction System</h1>
        
        <div class="example">
            <h3>📝 How to use:</h3>
            <p>Enter your symptoms separated by semicolons (;). For example:</p>
            <p><strong>fever; headache; fatigue; muscle aches</strong></p>
            <p><strong>abdominal pain; nausea; vomiting; loss of appetite</strong></p>
        </div>
        
        <form id="predictionForm">
            <div class="form-group">
                <label for="symptoms">Enter your symptoms:</label>
                <textarea 
                    id="symptoms" 
                    name="symptoms" 
                    placeholder="Enter symptoms separated by semicolons (;)..."
                    required
                ></textarea>
            </div>
            
            <button type="submit" id="submitBtn">🔍 Predict Disease</button>
        </form>
        
        <div id="result" class="result"></div>
        
        <div class="disclaimer">
            <strong>⚠️ Medical Disclaimer:</strong><br>
            This system is for educational and informational purposes only. 
            It should not be used as a substitute for professional medical advice, 
            diagnosis, or treatment. Always consult with a qualified healthcare 
            provider for proper medical care.
        </div>
    </div>

    <script>
        document.getElementById('predictionForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const symptoms = document.getElementById('symptoms').value.trim();
            const submitBtn = document.getElementById('submitBtn');
            const resultDiv = document.getElementById('result');
            
            if (!symptoms) {
                showResult('Please enter at least one symptom.', 'error');
                return;
            }
            
            // Show loading state
            submitBtn.disabled = true;
            submitBtn.textContent = '🔄 Analyzing...';
            resultDiv.style.display = 'none';
            
            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ symptoms: symptoms })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    displayResults(data);
                } else {
                    showResult(data.error || 'An error occurred', 'error');
                }
            } catch (error) {
                showResult('Network error. Please try again.', 'error');
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = '🔍 Predict Disease';
            }
        });
        
        function displayResults(data) {
            const resultDiv = document.getElementById('result');
            resultDiv.className = 'result success';
            resultDiv.style.display = 'block';
            
            let html = `
                <h3>🎯 Prediction Results</h3>
                <p><strong>Input Symptoms:</strong> ${data.input_symptoms.join(', ')}</p>
                <p><strong>Most Likely Disease:</strong> ${data.predicted_disease}</p>
                <p><strong>Confidence:</strong> ${(data.confidence * 100).toFixed(1)}%</p>
                
                <h4>📊 Top Predictions:</h4>
            `;
            
            data.top_k_predictions.forEach(pred => {
                const rankClass = `rank-${pred.rank}`;
                html += `
                    <div class="prediction-item ${rankClass}">
                        <strong>#${pred.rank} ${pred.disease}</strong>
                        <div class="confidence-bar">
                            <div class="confidence-fill" style="width: ${pred.percentage}%"></div>
                        </div>
                        <small>Confidence: ${pred.percentage.toFixed(1)}%</small>
                    </div>
                `;
            });
            
            html += `
                <p><small>Analysis completed at: ${new Date(data.timestamp).toLocaleString()}</small></p>
            `;
            
            resultDiv.innerHTML = html;
        }
        
        function showResult(message, type) {
            const resultDiv = document.getElementById('result');
            resultDiv.className = `result ${type}`;
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = `<p>${message}</p>`;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve the main web interface"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/predict', methods=['POST'])
def predict():
    """API endpoint for disease prediction with medical dictionary integration"""
    try:
        # DEBUG: Log incoming request
        print(f"\n🔍 DEBUG: Received request to /predict")
        print(f"🔍 DEBUG: Request method: {request.method}")
        print(f"🔍 DEBUG: Request headers: {dict(request.headers)}")
        print(f"🔍 DEBUG: Request content type: {request.content_type}")
        
        data = request.get_json()
        print(f"🔍 DEBUG: Request JSON data: {data}")
        
        if not data or 'symptoms' not in data:
            print(f"❌ DEBUG: Missing symptoms in request data")
            return jsonify({'error': 'Symptoms are required'}), 400
        
        symptoms = data['symptoms'].strip()
        print(f"🔍 DEBUG: Extracted symptoms: '{symptoms}'")
        
        if not symptoms:
            print(f"❌ DEBUG: Empty symptoms after stripping")
            return jsonify({'error': 'Symptoms cannot be empty'}), 400
        
        # Validate symptoms
        validation = predictor.validate_symptoms(symptoms)
        if not validation['valid']:
            return jsonify({
                'error': validation['message'],
                'suggestions': validation['suggestions']
            }), 400
        
        # Get top-k parameter (default to 5)
        top_k = data.get('top_k', 5)
        if not isinstance(top_k, int) or top_k < 1 or top_k > 10:
            top_k = 5
        
        print(f"🔍 DEBUG: Using top_k: {top_k}")
        
        # Make prediction
        print(f"🔍 DEBUG: Calling predictor.predict_disease...")
        prediction_result = predictor.predict_disease(symptoms, top_k=top_k)
        print(f"🔍 DEBUG: Prediction result: {prediction_result}")
        
        # Enhance with medical dictionary information
        enhanced_predictions = []
        for pred in prediction_result.get('top_k_predictions', []):
            disease_name = pred['disease']
            
            # Get comprehensive medical information
            medical_info = medical_dict.get_comprehensive_info(disease_name)
            
            enhanced_pred = {
                'rank': pred['rank'],
                'disease': disease_name,
                'percentage': pred['percentage'],
                'confidence': pred['percentage'] / 100.0,
                'medical_info': medical_info.get('disease_info'),
                'care_plan': medical_info.get('care_plan'),
                'urgency_level': _determine_urgency_level(pred['percentage'], disease_name)
            }
            
            enhanced_predictions.append(enhanced_pred)
        
        # Create enhanced result
        enhanced_result = {
            'input_symptoms': prediction_result.get('input_symptoms', []),
            'predicted_disease': prediction_result.get('predicted_disease', ''),
            'confidence': prediction_result.get('confidence', 0.0),
            'top_k_predictions': enhanced_predictions,
            'timestamp': prediction_result.get('timestamp', datetime.now().isoformat()),
            'medical_disclaimer': 'This analysis is for informational purposes only. Always consult with a healthcare professional for proper diagnosis and treatment.',
            'version': '2.0 - Enhanced with Medical Dictionary'
        }
        
        print(f"🔍 DEBUG: Enhanced result: {enhanced_result}")
        print(f"✅ DEBUG: Sending response with {len(enhanced_predictions)} predictions")
        
        return jsonify(enhanced_result)
        
    except Exception as e:
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'models_loaded': len(predictor.models) > 0,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/models')
def models():
    """Get information about loaded models"""
    return jsonify({
        'models': list(predictor.models.keys()),
        'disease_classes': predictor.disease_classes,
        'total_diseases': len(predictor.disease_classes)
    })

@app.route('/validate', methods=['POST'])
def validate_symptoms():
    """Validate symptom input"""
    try:
        data = request.get_json()
        
        if not data or 'symptoms' not in data:
            return jsonify({'error': 'Symptoms are required'}), 400
        
        symptoms = data['symptoms'].strip()
        validation = predictor.validate_symptoms(symptoms)
        
        return jsonify(validation)
        
    except Exception as e:
        return jsonify({'error': f'Validation failed: {str(e)}'}), 500

@app.route('/disease/<disease_name>', methods=['GET'])
def get_disease_info(disease_name):
    """Get comprehensive disease information"""
    try:
        disease_info = medical_dict.get_comprehensive_info(disease_name)
        
        if not disease_info.get('disease_info'):
            return jsonify({'error': f'Disease "{disease_name}" not found'}), 404
        
        return jsonify(disease_info)
        
    except Exception as e:
        return jsonify({'error': f'Failed to get disease information: {str(e)}'}), 500

@app.route('/diseases', methods=['GET'])
def get_all_diseases():
    """Get list of all available diseases"""
    try:
        diseases = medical_dict.get_all_diseases()
        return jsonify({
            'diseases': diseases,
            'count': len(diseases),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get diseases list: {str(e)}'}), 500

@app.route('/search', methods=['POST'])
def search_diseases():
    """Search diseases by symptoms or name"""
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({'error': 'Search query is required'}), 400
        
        query = data['query'].strip()
        if not query:
            return jsonify({'error': 'Search query cannot be empty'}), 400
        
        results = medical_dict.search_diseases(query)
        
        return jsonify({
            'query': query,
            'results': results,
            'count': len(results),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': f'Search failed: {str(e)}'}), 500

@app.route('/care-plan/<disease_name>', methods=['GET'])
def get_care_plan(disease_name):
    """Get care plan for a specific disease"""
    try:
        care_plan = medical_dict.get_care_plan(disease_name)
        
        if not care_plan:
            return jsonify({'error': f'Care plan for "{disease_name}" not found'}), 404
        
        return jsonify({
            'disease': disease_name,
            'care_plan': care_plan,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get care plan: {str(e)}'}), 500


@app.route('/nutrition/<food_name>', methods=['GET'])
def get_food_nutrition(food_name):
    """Get nutrition information from Open Food Facts API"""
    try:
        nutrition_info = medical_dict.get_food_nutrition(food_name)
        
        if not nutrition_info:
            return jsonify({'error': f'Nutrition information for "{food_name}" not found'}), 404
        
        return jsonify(nutrition_info)
        
    except Exception as e:
        return jsonify({'error': f'Failed to get nutrition information: {str(e)}'}), 500

@app.route('/health-tips/<condition>', methods=['GET'])
def get_health_tips(condition):
    """Get health tips for a specific condition"""
    try:
        tips = medical_dict.get_health_tips(condition)
        
        return jsonify({
            'condition': condition,
            'tips': tips,
            'count': len(tips),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get health tips: {str(e)}'}), 500

@app.route('/nutritional-recommendations/<disease_name>', methods=['GET'])
def get_nutritional_recommendations(disease_name):
    """Get nutritional recommendations for a disease"""
    try:
        recommendations = medical_dict.get_nutritional_recommendations(disease_name)
        
        return jsonify(recommendations)
        
    except Exception as e:
        return jsonify({'error': f'Failed to get nutritional recommendations: {str(e)}'}), 500

@app.route('/enhanced-disease/<disease_name>', methods=['GET'])
def get_enhanced_disease_info(disease_name):
    """Get enhanced disease information with API data"""
    try:
        enhanced_info = medical_dict.get_enhanced_disease_info(disease_name)
        
        if not enhanced_info.get('disease_info'):
            return jsonify({'error': f'Enhanced information for "{disease_name}" not found'}), 404
        
        return jsonify(enhanced_info)
        
    except Exception as e:
        return jsonify({'error': f'Failed to get enhanced disease information: {str(e)}'}), 500

@app.route('/comprehensive-analysis', methods=['POST'])
def comprehensive_analysis():
    """Get comprehensive analysis with predicted disease, nutrition, and medical terminology"""
    try:
        data = request.get_json()
        
        if not data or 'symptoms' not in data:
            return jsonify({'error': 'Symptoms are required'}), 400
        
        symptoms = data['symptoms'].strip()
        
        if not symptoms:
            return jsonify({'error': 'Symptoms cannot be empty'}), 400
        
        # Get disease prediction
        prediction_result = predictor.predict_disease(symptoms, top_k=3)
        
        # Get comprehensive information for top prediction
        top_disease = prediction_result.get('predicted_disease', '')
        comprehensive_result = {
            'input_symptoms': prediction_result.get('input_symptoms', []),
            'prediction': {
                'disease': top_disease,
                'confidence': prediction_result.get('confidence', 0.0),
                'all_predictions': prediction_result.get('top_k_predictions', [])
            },
            'disease_information': {},
            'nutritional_recommendations': {},
            'medical_terminology': {},
            'timestamp': datetime.now().isoformat(),
            'version': '2.0 - Comprehensive Analysis'
        }
        
        if top_disease:
            # Get disease information
            disease_info = medical_dict.get_comprehensive_info(top_disease)
            comprehensive_result['disease_information'] = disease_info.get('disease_info', {})
            
            # Get nutritional recommendations
            nutrition_recs = medical_dict.get_nutritional_recommendations(top_disease)
            comprehensive_result['nutritional_recommendations'] = nutrition_recs
            
            # Get medical terminology for the disease
            medical_terms = {}
            if disease_info.get('disease_info'):
                disease_data = disease_info['disease_info']
                # Extract medical terms from disease information
                medical_terms = {
                    'disease_name': disease_data.get('disease_name', ''),
                    'medical_definition': disease_data.get('medical_definition', ''),
                    'body_system': disease_data.get('body_system', ''),
                    'severity_level': disease_data.get('severity_level', ''),
                    'common_symptoms': disease_data.get('common_symptoms', []),
                    'causes': disease_data.get('causes', []),
                    'risk_factors': disease_data.get('risk_factors', [])
                }
            
            comprehensive_result['medical_terminology'] = medical_terms
        
        # Save to output.json
        output_file = 'output.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(comprehensive_result, f, indent=2, ensure_ascii=False)
        
        return jsonify(comprehensive_result)
        
    except Exception as e:
        return jsonify({'error': f'Comprehensive analysis failed: {str(e)}'}), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("=" * 80)
    print("ENHANCED DISEASE PREDICTION API v2.0 - WITH FREE OPEN-SOURCE APIs")
    print("=" * 80)
    print("Starting Flask server...")
    print("Web interface: http://localhost:5000")
    print("API endpoints:")
    print("  Core Prediction:")
    print("    - Predict: http://localhost:5000/predict")
    print("    - Health check: http://localhost:5000/health")
    print("    - All diseases: http://localhost:5000/diseases")
    print("    - Disease info: http://localhost:5000/disease/<name>")
    print("    - Search: http://localhost:5000/search")
    print("    - Care plan: http://localhost:5000/care-plan/<name>")
    print("  Enhanced Features (with Free APIs):")
    print("    - Nutrition: http://localhost:5000/nutrition/<food> (Open Food Facts)")
    print("    - Health tips: http://localhost:5000/health-tips/<condition>")
    print("    - Nutritional recommendations: http://localhost:5000/nutritional-recommendations/<disease>")
    print("    - Enhanced disease info: http://localhost:5000/enhanced-disease/<name>")
    print("    - Comprehensive analysis: http://localhost:5000/comprehensive-analysis (POST)")
    print("=" * 80)
    print("Integrated Free APIs:")
    print("  - Open Food Facts: Nutrition information")
    print("  - Disease Ontology: Medical terminology")
    print("  - Output: Saves results to output.json")
    print("=" * 80)
    
    app.run(debug=True, host='0.0.0.0', port=5000)

