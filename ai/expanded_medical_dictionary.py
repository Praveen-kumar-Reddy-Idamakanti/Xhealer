"""
Expanded Medical Dictionary with 10 Common Diseases
Comprehensive medical information for various body systems
"""

import json
import os
from typing import Dict, List, Optional, Any

class ExpandedMedicalDictionary:
    """
    Expanded medical dictionary with 10 common diseases covering different body systems
    """
    
    def __init__(self):
        self.disease_database = {}
        self.medical_translations = {}
        self.care_plans = {}
        self._initialize_disease_database()
        self._initialize_medical_translations()
        self._initialize_care_plans()
    
    def _initialize_disease_database(self):
        """
        Initialize comprehensive disease database with 10 common diseases
        """
        self.disease_database = {
            # Respiratory System
            "common_cold": {
                "disease_name": "Common Cold",
                "medical_definition": "Viral infection of the upper respiratory tract, most commonly caused by rhinoviruses",
                "layman_explanation": "A common cold is like your body's way of fighting off a tiny tiny thing that can make you sick that got into your nose or throat. It's your body's defense system working hard to get rid of the invader, which causes all those annoying symptoms like a liquid coming out of your nose and forceful breathing out to clear throat.",
                "causes": [
                    "Rhinovirus (most common)",
                    "Coronavirus",
                    "Adenovirus",
                    "Respiratory syncytial virus"
                ],
                "risk_factors": [
                    "Weakened immune system",
                    "Close contact with infected person",
                    "Seasonal changes",
                    "Stress",
                    "Lack of sleep"
                ],
                "body_system": "Respiratory",
                "severity_level": "Mild to Moderate",
                "duration": "7-10 days typically",
                "common_symptoms": [
                    "Runny nose",
                    "Sore throat",
                    "Cough",
                    "Sneezing",
                    "Mild fever",
                    "Fatigue",
                    "Headache"
                ],
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
                "medical_definition": "Viral infection of the respiratory system caused by influenza viruses",
                "layman_explanation": "The flu is like a really bad cold that makes you feel terrible all over your body. It's caused by a different type of tiny invader that attacks your breathing system and makes you feel very tired and achy.",
                "causes": [
                    "Influenza A virus",
                    "Influenza B virus",
                    "Influenza C virus"
                ],
                "risk_factors": [
                    "Weakened immune system",
                    "Chronic medical conditions",
                    "Pregnancy",
                    "Age (very young or elderly)",
                    "Close contact with infected person"
                ],
                "body_system": "Respiratory",
                "severity_level": "Moderate to Severe",
                "duration": "1-2 weeks",
                "common_symptoms": [
                    "High fever",
                    "Body aches",
                    "Chills",
                    "Fatigue",
                    "Headache",
                    "Cough",
                    "Sore throat",
                    "Runny nose"
                ],
                "when_to_see_doctor": [
                    "Difficulty breathing",
                    "Persistent chest pain",
                    "Severe dehydration",
                    "High fever that doesn't respond to medication",
                    "Worsening symptoms after initial improvement"
                ]
            },
            
            "asthma": {
                "disease_name": "Asthma",
                "medical_definition": "Chronic inflammatory disease of the airways causing reversible airflow obstruction",
                "layman_explanation": "Asthma is when the tubes that carry air to your lungs get swollen and tight, making it hard to breathe. It's like trying to breathe through a very narrow straw that keeps getting smaller.",
                "causes": [
                    "Genetic predisposition",
                    "Environmental allergens",
                    "Respiratory infections",
                    "Air pollution",
                    "Exercise",
                    "Stress"
                ],
                "risk_factors": [
                    "Family history of asthma",
                    "Allergies",
                    "Exposure to tobacco smoke",
                    "Obesity",
                    "Respiratory infections in childhood"
                ],
                "body_system": "Respiratory",
                "severity_level": "Mild to Severe",
                "duration": "Chronic condition",
                "common_symptoms": [
                    "Wheezing",
                    "Shortness of breath",
                    "Chest tightness",
                    "Coughing",
                    "Difficulty breathing",
                    "Rapid breathing"
                ],
                "when_to_see_doctor": [
                    "Severe breathing difficulty",
                    "Lips or fingernails turning blue",
                    "Rapid heartbeat",
                    "Inability to speak in full sentences",
                    "Emergency inhaler not working"
                ]
            },
            
            # Cardiovascular System
            "hypertension": {
                "disease_name": "Hypertension (High Blood Pressure)",
                "medical_definition": "Chronic medical condition where blood pressure in the arteries is persistently elevated",
                "layman_explanation": "High blood pressure is when your heart has to work too hard to pump blood through your body. It's like water trying to flow through a hose that's being squeezed too tightly.",
                "causes": [
                    "Genetic factors",
                    "High salt intake",
                    "Obesity",
                    "Lack of physical activity",
                    "Stress",
                    "Excessive alcohol consumption",
                    "Smoking"
                ],
                "risk_factors": [
                    "Age (over 65)",
                    "Family history",
                    "African American ethnicity",
                    "Diabetes",
                    "Chronic kidney disease",
                    "Sleep apnea"
                ],
                "body_system": "Cardiovascular",
                "severity_level": "Moderate to Severe",
                "duration": "Chronic condition",
                "common_symptoms": [
                    "Often asymptomatic",
                    "Headaches",
                    "Shortness of breath",
                    "Nosebleeds",
                    "Dizziness",
                    "Chest pain"
                ],
                "when_to_see_doctor": [
                    "Blood pressure reading above 140/90",
                    "Severe headaches",
                    "Chest pain",
                    "Difficulty breathing",
                    "Vision problems"
                ]
            },
            
            # Gastrointestinal System
            "gastroenteritis": {
                "disease_name": "Gastroenteritis (Stomach Flu)",
                "medical_definition": "Inflammation of the stomach and intestines, usually caused by viral or bacterial infection",
                "layman_explanation": "Stomach flu is when your stomach and intestines get irritated and inflamed, usually from a tiny invader. It makes you feel sick to your stomach and causes problems with your digestive system.",
                "causes": [
                    "Norovirus (most common)",
                    "Rotavirus",
                    "Bacterial infections (E. coli, Salmonella)",
                    "Food poisoning",
                    "Contaminated water"
                ],
                "risk_factors": [
                    "Weakened immune system",
                    "Travel to developing countries",
                    "Consumption of contaminated food or water",
                    "Close contact with infected person",
                    "Poor hygiene"
                ],
                "body_system": "Gastrointestinal",
                "severity_level": "Mild to Moderate",
                "duration": "1-3 days typically",
                "common_symptoms": [
                    "Nausea",
                    "Vomiting",
                    "Diarrhea",
                    "Abdominal pain",
                    "Fever",
                    "Loss of appetite",
                    "Dehydration"
                ],
                "when_to_see_doctor": [
                    "Severe dehydration",
                    "Blood in vomit or stool",
                    "High fever",
                    "Symptoms lasting more than 3 days",
                    "Signs of severe dehydration"
                ]
            },
            
            # Musculoskeletal System
            "arthritis": {
                "disease_name": "Arthritis",
                "medical_definition": "Inflammation of one or more joints, causing pain and stiffness",
                "layman_explanation": "Arthritis is when the joints in your body (where bones meet) get swollen and painful. It's like the hinges on a door getting rusty and hard to move.",
                "causes": [
                    "Wear and tear (osteoarthritis)",
                    "Autoimmune response (rheumatoid arthritis)",
                    "Injury",
                    "Infection",
                    "Genetic factors",
                    "Obesity"
                ],
                "risk_factors": [
                    "Age (over 65)",
                    "Family history",
                    "Previous joint injury",
                    "Obesity",
                    "Repetitive joint use",
                    "Gender (women more affected)"
                ],
                "body_system": "Musculoskeletal",
                "severity_level": "Mild to Severe",
                "duration": "Chronic condition",
                "common_symptoms": [
                    "Joint pain",
                    "Stiffness",
                    "Swelling",
                    "Reduced range of motion",
                    "Warmth around joints",
                    "Fatigue"
                ],
                "when_to_see_doctor": [
                    "Severe joint pain",
                    "Joint deformity",
                    "Loss of function",
                    "Fever with joint symptoms",
                    "Sudden onset of severe symptoms"
                ]
            },
            
            # Endocrine System
            "diabetes_type2": {
                "disease_name": "Type 2 Diabetes Mellitus",
                "medical_definition": "Chronic metabolic disorder characterized by high blood sugar levels due to insulin resistance or insufficient insulin production",
                "layman_explanation": "Type 2 diabetes is when your body can't use sugar properly. It's like having a key that doesn't fit the lock anymore - your body has trouble getting sugar from your blood into your cells where it's needed for energy.",
                "causes": [
                    "Insulin resistance",
                    "Insufficient insulin production",
                    "Genetic factors",
                    "Obesity",
                    "Physical inactivity",
                    "Poor diet"
                ],
                "risk_factors": [
                    "Family history",
                    "Obesity",
                    "Age (over 45)",
                    "Physical inactivity",
                    "High blood pressure",
                    "High cholesterol",
                    "Gestational diabetes history"
                ],
                "body_system": "Endocrine",
                "severity_level": "Moderate to Severe",
                "duration": "Chronic condition",
                "common_symptoms": [
                    "Increased thirst",
                    "Frequent urination",
                    "Increased hunger",
                    "Unexplained weight loss",
                    "Fatigue",
                    "Blurred vision",
                    "Slow-healing sores"
                ],
                "when_to_see_doctor": [
                    "Blood sugar levels above 126 mg/dL",
                    "Symptoms of high blood sugar",
                    "Frequent infections",
                    "Vision problems",
                    "Numbness or tingling in hands/feet"
                ]
            },
            
            # Nervous System
            "migraine": {
                "disease_name": "Migraine",
                "medical_definition": "Neurological disorder characterized by recurrent, severe headaches often accompanied by nausea, vomiting, and sensitivity to light and sound",
                "layman_explanation": "A migraine is like having a very bad headache that feels like someone is hitting your head with a hammer. It often comes with feeling sick to your stomach and being bothered by bright lights or loud sounds.",
                "causes": [
                    "Genetic factors",
                    "Hormonal changes",
                    "Stress",
                    "Certain foods",
                    "Sleep disturbances",
                    "Environmental factors",
                    "Medication overuse"
                ],
                "risk_factors": [
                    "Family history",
                    "Gender (women more affected)",
                    "Age (peak in 30s-40s)",
                    "Hormonal changes",
                    "Stress",
                    "Certain medical conditions"
                ],
                "body_system": "Nervous",
                "severity_level": "Moderate to Severe",
                "duration": "4-72 hours per episode",
                "common_symptoms": [
                    "Severe headache",
                    "Nausea",
                    "Vomiting",
                    "Sensitivity to light",
                    "Sensitivity to sound",
                    "Aura (visual disturbances)",
                    "Dizziness"
                ],
                "when_to_see_doctor": [
                    "Sudden, severe headache",
                    "Headache with fever, stiff neck, or rash",
                    "Headache after head injury",
                    "New headache pattern",
                    "Headache that worsens with coughing or movement"
                ]
            },
            
            # Urinary System
            "urinary_tract_infection": {
                "disease_name": "Urinary Tract Infection (UTI)",
                "medical_definition": "Infection of any part of the urinary system, most commonly caused by bacteria",
                "layman_explanation": "A UTI is when bacteria get into your urinary system (the parts of your body that make and get rid of urine) and cause an infection. It's like having an unwelcome guest in your body's plumbing system.",
                "causes": [
                    "E. coli bacteria (most common)",
                    "Other bacteria",
                    "Sexual activity",
                    "Poor hygiene",
                    "Urinary catheter use",
                    "Blocked urine flow"
                ],
                "risk_factors": [
                    "Female gender",
                    "Sexual activity",
                    "Menopause",
                    "Diabetes",
                    "Urinary catheter use",
                    "Kidney stones",
                    "Weakened immune system"
                ],
                "body_system": "Urinary",
                "severity_level": "Mild to Moderate",
                "duration": "3-7 days with treatment",
                "common_symptoms": [
                    "Burning sensation during urination",
                    "Frequent urination",
                    "Urgent need to urinate",
                    "Cloudy or bloody urine",
                    "Lower abdominal pain",
                    "Fever",
                    "Back pain"
                ],
                "when_to_see_doctor": [
                    "Symptoms of UTI",
                    "Fever with UTI symptoms",
                    "Back pain with UTI symptoms",
                    "Blood in urine",
                    "Symptoms not improving with treatment"
                ]
            },
            
            # Skin System
            "eczema": {
                "disease_name": "Eczema (Atopic Dermatitis)",
                "medical_definition": "Chronic inflammatory skin condition characterized by dry, itchy, and inflamed skin",
                "layman_explanation": "Eczema is when your skin gets very dry, itchy, and sometimes red and swollen. It's like your skin is having an allergic reaction and gets irritated easily.",
                "causes": [
                    "Genetic factors",
                    "Immune system dysfunction",
                    "Environmental triggers",
                    "Skin barrier dysfunction",
                    "Allergens",
                    "Stress"
                ],
                "risk_factors": [
                    "Family history of eczema",
                    "Personal or family history of allergies",
                    "Asthma",
                    "Hay fever",
                    "Dry skin",
                    "Stress"
                ],
                "body_system": "Integumentary (Skin)",
                "severity_level": "Mild to Severe",
                "duration": "Chronic condition with flare-ups",
                "common_symptoms": [
                    "Dry, itchy skin",
                    "Red, inflamed patches",
                    "Rough, scaly skin",
                    "Cracking or bleeding",
                    "Thickened skin",
                    "Sensitivity to irritants"
                ],
                "when_to_see_doctor": [
                    "Severe itching",
                    "Signs of skin infection",
                    "Eczema not responding to treatment",
                    "Significant impact on daily life",
                    "New or worsening symptoms"
                ]
            }
        }
    
    def _initialize_medical_translations(self):
        """
        Initialize medical terminology translations for layman understanding
        """
        self.medical_translations = {
            # Respiratory terms
            "rhinovirus": "a type of virus that causes colds",
            "coronavirus": "a family of viruses that can cause respiratory infections",
            "bronchial tubes": "the tubes that carry air to and from your lungs",
            "inflammation": "swelling and irritation in your body",
            "airflow obstruction": "when air can't flow easily through your breathing tubes",
            "wheezing": "a whistling sound when you breathe",
            
            # Cardiovascular terms
            "blood pressure": "the force of blood pushing against the walls of your blood vessels",
            "arteries": "blood vessels that carry blood away from your heart",
            "hypertension": "high blood pressure",
            "cardiovascular": "related to your heart and blood vessels",
            
            # Gastrointestinal terms
            "gastroenteritis": "inflammation of your stomach and intestines",
            "norovirus": "a virus that causes stomach flu",
            "dehydration": "when your body doesn't have enough water",
            "nausea": "feeling like you want to throw up",
            "vomiting": "throwing up or being sick",
            "diarrhea": "loose, watery bowel movements",
            
            # Musculoskeletal terms
            "joints": "places where two bones meet and move",
            "osteoarthritis": "arthritis caused by wear and tear on joints",
            "rheumatoid arthritis": "arthritis caused by your immune system attacking your joints",
            "stiffness": "when your joints feel hard to move",
            "range of motion": "how far you can move a joint",
            
            # Endocrine terms
            "insulin": "a hormone that helps your body use sugar for energy",
            "insulin resistance": "when your body doesn't respond well to insulin",
            "blood sugar": "the amount of sugar in your blood",
            "metabolic": "related to how your body processes food and energy",
            
            # Nervous system terms
            "neurological": "related to your brain and nervous system",
            "aura": "warning signs that come before a migraine",
            "sensitivity": "being more affected by something than usual",
            "recurrent": "happening over and over again",
            
            # Urinary terms
            "urinary system": "the parts of your body that make and get rid of urine",
            "bacteria": "tiny living things that can cause infections",
            "urination": "the act of passing urine",
            "catheter": "a tube used to drain urine from the bladder",
            
            # Skin terms
            "dermatitis": "inflammation of the skin",
            "atopic": "tending to develop allergic reactions",
            "barrier dysfunction": "when your skin doesn't protect you as well as it should",
            "flare-up": "when symptoms get worse for a period of time",
            "irritants": "things that can make your skin irritated",
            
            # General medical terms
            "chronic": "lasting a long time or recurring",
            "acute": "happening suddenly and lasting a short time",
            "asymptomatic": "having no symptoms",
            "severe": "very serious or intense",
            "moderate": "not too mild, not too severe",
            "mild": "not very serious or intense",
            "genetic": "related to your genes and family history",
            "autoimmune": "when your immune system attacks your own body",
            "inflammatory": "causing swelling and irritation",
            "dysfunction": "not working properly",
            "predisposition": "a tendency to develop something",
            "contaminated": "made impure or unsafe",
            "pathogen": "a microorganism that can cause disease",
            "symptom": "a sign that something is wrong with your body",
            "diagnosis": "identifying what disease or condition you have",
            "treatment": "medical care to help you get better",
            "prevention": "actions to stop something from happening",
            "prognosis": "the likely outcome of a disease",
            "complication": "an additional problem that develops",
            "side effect": "an unwanted effect of a treatment",
            "dosage": "how much medicine to take",
            "contraindication": "a reason not to use a particular treatment",
            "allergy": "an overreaction of your immune system to something",
            "immunity": "your body's ability to fight off diseases",
            "vaccination": "getting a shot to prevent a disease",
            "antibiotic": "medicine that kills bacteria",
            "antiviral": "medicine that fights viruses",
            "anti-inflammatory": "medicine that reduces swelling",
            "analgesic": "pain-relieving medicine",
            "antihistamine": "medicine that helps with allergies",
            "steroid": "a type of medicine that reduces inflammation",
            "therapy": "treatment to help with a condition",
            "rehabilitation": "treatment to help you recover function",
            "prognosis": "the expected outcome of a disease"
        }
    
    def _initialize_care_plans(self):
        """
        Initialize comprehensive care plans for each disease
        """
        self.care_plans = {
            "common_cold": {
                "immediate_care": [
                    "Rest and get plenty of sleep",
                    "Stay hydrated by drinking water, tea, or clear broths",
                    "Use saline nasal drops or sprays to relieve congestion",
                    "Gargle with warm salt water for sore throat",
                    "Use a humidifier to add moisture to the air"
                ],
                "medications": [
                    "Over-the-counter pain relievers (acetaminophen, ibuprofen)",
                    "Decongestants for nasal congestion",
                    "Cough suppressants for dry cough",
                    "Expectorants for productive cough",
                    "Throat lozenges for sore throat"
                ],
                "lifestyle_modifications": [
                    "Avoid close contact with others to prevent spread",
                    "Wash hands frequently",
                    "Cover mouth and nose when coughing or sneezing",
                    "Avoid smoking and secondhand smoke",
                    "Eat a balanced diet with fruits and vegetables"
                ],
                "follow_up": [
                    "Monitor symptoms for 7-10 days",
                    "Seek medical attention if symptoms worsen",
                    "Return to normal activities when feeling better"
                ]
            },
            
            "influenza": {
                "immediate_care": [
                    "Rest in bed until fever subsides",
                    "Stay hydrated with water, electrolyte drinks, or clear broths",
                    "Use fever-reducing medications as directed",
                    "Apply cool compresses for fever",
                    "Isolate from others to prevent spread"
                ],
                "medications": [
                    "Antiviral medications (if prescribed within 48 hours)",
                    "Fever reducers (acetaminophen, ibuprofen)",
                    "Cough suppressants if needed",
                    "Pain relievers for body aches",
                    "Decongestants for nasal congestion"
                ],
                "lifestyle_modifications": [
                    "Stay home from work or school until fever-free for 24 hours",
                    "Avoid close contact with others",
                    "Wash hands frequently",
                    "Cover mouth and nose when coughing or sneezing",
                    "Get annual flu vaccination"
                ],
                "follow_up": [
                    "Monitor for complications (pneumonia, dehydration)",
                    "Seek emergency care for severe symptoms",
                    "Follow up with healthcare provider if symptoms persist"
                ]
            },
            
            "asthma": {
                "immediate_care": [
                    "Use rescue inhaler as prescribed",
                    "Sit upright and try to stay calm",
                    "Remove triggers if possible",
                    "Use breathing techniques",
                    "Seek emergency care if symptoms don't improve"
                ],
                "medications": [
                    "Rescue inhalers (short-acting bronchodilators)",
                    "Controller medications (inhaled corticosteroids)",
                    "Long-acting bronchodilators",
                    "Oral corticosteroids for severe attacks",
                    "Allergy medications if needed"
                ],
                "lifestyle_modifications": [
                    "Identify and avoid triggers",
                    "Keep rescue inhaler accessible at all times",
                    "Use air purifiers and maintain clean environment",
                    "Exercise regularly but avoid triggers",
                    "Manage stress and anxiety"
                ],
                "follow_up": [
                    "Regular check-ups with healthcare provider",
                    "Monitor peak flow readings",
                    "Update asthma action plan as needed",
                    "Review medication effectiveness"
                ]
            },
            
            "hypertension": {
                "immediate_care": [
                    "Take prescribed medications as directed",
                    "Monitor blood pressure regularly",
                    "Reduce sodium intake immediately",
                    "Limit alcohol consumption",
                    "Manage stress through relaxation techniques"
                ],
                "medications": [
                    "ACE inhibitors",
                    "Angiotensin receptor blockers",
                    "Diuretics",
                    "Beta-blockers",
                    "Calcium channel blockers"
                ],
                "lifestyle_modifications": [
                    "Follow DASH diet (low sodium, high potassium)",
                    "Exercise regularly (150 minutes per week)",
                    "Maintain healthy weight",
                    "Limit alcohol to 1-2 drinks per day",
                    "Quit smoking",
                    "Manage stress"
                ],
                "follow_up": [
                    "Regular blood pressure monitoring",
                    "Annual check-ups with healthcare provider",
                    "Monitor for complications",
                    "Adjust medications as needed"
                ]
            },
            
            "gastroenteritis": {
                "immediate_care": [
                    "Rest and avoid solid foods initially",
                    "Stay hydrated with clear liquids",
                    "Use oral rehydration solutions",
                    "Avoid dairy products and fatty foods",
                    "Wash hands frequently"
                ],
                "medications": [
                    "Oral rehydration solutions",
                    "Anti-nausea medications if prescribed",
                    "Antidiarrheal medications (use cautiously)",
                    "Probiotics to restore gut bacteria",
                    "Antibiotics only if bacterial cause confirmed"
                ],
                "lifestyle_modifications": [
                    "Gradually reintroduce bland foods",
                    "Avoid contaminated food and water",
                    "Practice good hygiene",
                    "Stay home until symptoms resolve",
                    "Avoid preparing food for others"
                ],
                "follow_up": [
                    "Monitor for signs of dehydration",
                    "Seek medical attention if symptoms worsen",
                    "Return to normal diet gradually"
                ]
            },
            
            "arthritis": {
                "immediate_care": [
                    "Apply ice packs to reduce inflammation",
                    "Use heat therapy for stiffness",
                    "Rest affected joints",
                    "Use assistive devices if needed",
                    "Take prescribed medications"
                ],
                "medications": [
                    "Nonsteroidal anti-inflammatory drugs (NSAIDs)",
                    "Acetaminophen for pain",
                    "Disease-modifying antirheumatic drugs (DMARDs)",
                    "Corticosteroids",
                    "Biologic medications"
                ],
                "lifestyle_modifications": [
                    "Maintain healthy weight",
                    "Exercise regularly (low-impact activities)",
                    "Use joint protection techniques",
                    "Apply heat and cold therapy",
                    "Consider physical therapy"
                ],
                "follow_up": [
                    "Regular monitoring of joint function",
                    "Adjust treatment plan as needed",
                    "Monitor for medication side effects",
                    "Consider surgical options if necessary"
                ]
            },
            
            "diabetes_type2": {
                "immediate_care": [
                    "Monitor blood glucose levels regularly",
                    "Take medications as prescribed",
                    "Follow meal plan consistently",
                    "Stay hydrated",
                    "Recognize signs of high/low blood sugar"
                ],
                "medications": [
                    "Metformin (first-line treatment)",
                    "Sulfonylureas",
                    "DPP-4 inhibitors",
                    "GLP-1 receptor agonists",
                    "Insulin (if needed)"
                ],
                "lifestyle_modifications": [
                    "Follow diabetes meal plan",
                    "Exercise regularly (150 minutes per week)",
                    "Maintain healthy weight",
                    "Monitor blood glucose levels",
                    "Quit smoking",
                    "Manage stress"
                ],
                "follow_up": [
                    "Regular HbA1c testing",
                    "Annual eye exams",
                    "Regular foot exams",
                    "Monitor blood pressure and cholesterol",
                    "Adjust treatment as needed"
                ]
            },
            
            "migraine": {
                "immediate_care": [
                    "Rest in a dark, quiet room",
                    "Apply cold compress to head or neck",
                    "Take prescribed medications early",
                    "Stay hydrated",
                    "Avoid triggers if possible"
                ],
                "medications": [
                    "Triptans for acute treatment",
                    "NSAIDs for mild migraines",
                    "Anti-nausea medications",
                    "Preventive medications if frequent",
                    "Caffeine (in moderation)"
                ],
                "lifestyle_modifications": [
                    "Identify and avoid triggers",
                    "Maintain regular sleep schedule",
                    "Eat regular meals",
                    "Manage stress",
                    "Exercise regularly"
                ],
                "follow_up": [
                    "Keep migraine diary",
                    "Review treatment effectiveness",
                    "Adjust preventive strategies",
                    "Monitor for medication overuse"
                ]
            },
            
            "urinary_tract_infection": {
                "immediate_care": [
                    "Drink plenty of water",
                    "Urinate frequently",
                    "Avoid irritating substances",
                    "Use heating pad for pain",
                    "Take prescribed antibiotics"
                ],
                "medications": [
                    "Antibiotics (as prescribed)",
                    "Pain relievers (phenazopyridine)",
                    "Cranberry supplements (may help prevent)",
                    "Probiotics to restore balance",
                    "Urinary analgesics"
                ],
                "lifestyle_modifications": [
                    "Drink plenty of water",
                    "Urinate after sexual activity",
                    "Wipe from front to back",
                    "Avoid irritating feminine products",
                    "Wear cotton underwear"
                ],
                "follow_up": [
                    "Complete full course of antibiotics",
                    "Monitor for recurring infections",
                    "Follow up if symptoms persist",
                    "Consider preventive measures"
                ]
            },
            
            "eczema": {
                "immediate_care": [
                    "Apply moisturizer frequently",
                    "Use gentle, fragrance-free products",
                    "Avoid scratching",
                    "Apply cool compresses for itching",
                    "Keep nails short"
                ],
                "medications": [
                    "Topical corticosteroids",
                    "Topical calcineurin inhibitors",
                    "Antihistamines for itching",
                    "Oral corticosteroids for severe cases",
                    "Antibiotics if infected"
                ],
                "lifestyle_modifications": [
                    "Use gentle, fragrance-free skincare products",
                    "Moisturize skin regularly",
                    "Avoid known triggers",
                    "Wear soft, breathable fabrics",
                    "Manage stress"
                ],
                "follow_up": [
                    "Monitor skin condition regularly",
                    "Adjust treatment as needed",
                    "Prevent skin infections",
                    "Review trigger identification"
                ]
            }
        }
    
    def get_disease_info(self, disease_name: str) -> Optional[Dict]:
        """
        Get comprehensive disease information
        
        Args:
            disease_name: Name of the disease
            
        Returns:
            Disease information dictionary
        """
        # Normalize disease name
        normalized_name = disease_name.lower().replace(" ", "_").replace("-", "_")
        
        if normalized_name in self.disease_database:
            return self.disease_database[normalized_name]
        
        # Try to find by partial match
        for key, value in self.disease_database.items():
            if disease_name.lower() in value.get("disease_name", "").lower():
                return value
        
        return None
    
    def get_care_plan(self, disease_name: str) -> Optional[Dict]:
        """
        Get care plan for a disease
        
        Args:
            disease_name: Name of the disease
            
        Returns:
            Care plan dictionary
        """
        # Normalize disease name
        normalized_name = disease_name.lower().replace(" ", "_").replace("-", "_")
        
        if normalized_name in self.care_plans:
            return self.care_plans[normalized_name]
        
        # Try to find by partial match
        for key, value in self.care_plans.items():
            if disease_name.lower() in key:
                return value
        
        return None
    
    def get_all_diseases(self) -> List[str]:
        """
        Get list of all available diseases
        
        Returns:
            List of disease names
        """
        return [info["disease_name"] for info in self.disease_database.values()]
    
    def search_diseases(self, query: str) -> List[Dict]:
        """
        Search diseases by query
        
        Args:
            query: Search query
            
        Returns:
            List of matching diseases
        """
        query = query.lower()
        results = []
        
        for key, value in self.disease_database.items():
            disease_name = value.get("disease_name", "").lower()
            symptoms = " ".join(value.get("common_symptoms", [])).lower()
            body_system = value.get("body_system", "").lower()
            
            if (query in disease_name or 
                query in symptoms or 
                query in body_system or
                query in key):
                results.append(value)
        
        return results
    
    def get_diseases_by_body_system(self, body_system: str) -> List[Dict]:
        """
        Get diseases by body system
        
        Args:
            body_system: Body system name
            
        Returns:
            List of diseases in the specified body system
        """
        return [
            disease_info for disease_info in self.disease_database.values()
            if disease_info.get('body_system', '').lower() == body_system.lower()
        ]
    
    def save_to_file(self, filename: str = "expanded_medical_dictionary.json"):
        """
        Save the medical dictionary to a JSON file
        
        Args:
            filename: Output filename
        """
        data = {
            "disease_database": self.disease_database,
            "medical_translations": self.medical_translations,
            "care_plans": self.care_plans
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Expanded medical dictionary saved to {filename}")
    
    def load_from_file(self, filename: str = "expanded_medical_dictionary.json"):
        """
        Load the medical dictionary from a JSON file
        
        Args:
            filename: Input filename
        """
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.disease_database = data.get("disease_database", {})
            self.medical_translations = data.get("medical_translations", {})
            self.care_plans = data.get("care_plans", {})
            
            print(f"✅ Expanded medical dictionary loaded from {filename}")
        else:
            print(f"❌ File {filename} not found")

def main():
    """
    Demo the expanded medical dictionary
    """
    print("🚀 EXPANDED MEDICAL DICTIONARY - 10 COMMON DISEASES")
    print("="*60)
    
    # Initialize the expanded medical dictionary
    medical_dict = ExpandedMedicalDictionary()
    
    print(f"📚 Loaded {len(medical_dict.disease_database)} diseases")
    print(f"📝 Loaded {len(medical_dict.medical_translations)} medical translations")
    print(f"🏥 Loaded {len(medical_dict.care_plans)} care plans")
    
    print(f"\n📋 Available Diseases:")
    for i, disease in enumerate(medical_dict.get_all_diseases(), 1):
        print(f"  {i}. {disease}")
    
    print(f"\n🔍 Body Systems Covered:")
    body_systems = set()
    for disease_info in medical_dict.disease_database.values():
        body_systems.add(disease_info.get('body_system', 'Unknown'))
    
    for system in sorted(body_systems):
        diseases = medical_dict.get_diseases_by_body_system(system)
        print(f"  - {system}: {len(diseases)} diseases")
    
    # Save to file
    medical_dict.save_to_file()
    
    print(f"\n✅ Expanded Medical Dictionary Ready!")
    print("Features:")
    print("  ✅ 10 Common Diseases")
    print("  ✅ Multiple Body Systems")
    print("  ✅ Comprehensive Care Plans")
    print("  ✅ Medical Terminology Translations")
    print("  ✅ JSON Export/Import")
    print("="*60)

if __name__ == "__main__":
    main()
