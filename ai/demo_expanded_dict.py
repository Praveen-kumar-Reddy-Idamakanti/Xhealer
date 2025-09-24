"""
Demo script for the expanded medical dictionary
"""

from expanded_medical_dictionary import ExpandedMedicalDictionary
import json

def main():
    print("🚀 EXPANDED MEDICAL DICTIONARY DEMO")
    print("="*50)
    
    # Initialize the expanded medical dictionary
    medical_dict = ExpandedMedicalDictionary()
    
    # Test with a specific disease
    disease_name = "Influenza"
    disease_info = medical_dict.get_disease_info(disease_name)
    care_plan = medical_dict.get_care_plan(disease_name)
    
    print(f"📋 Testing Disease: {disease_name}")
    print(f"✅ Disease Found: {disease_info is not None}")
    print(f"✅ Care Plan Found: {care_plan is not None}")
    
    if disease_info:
        print(f"\n🏥 Disease Information:")
        print(f"  - Name: {disease_info.get('disease_name', 'N/A')}")
        print(f"  - Body System: {disease_info.get('body_system', 'N/A')}")
        print(f"  - Severity: {disease_info.get('severity_level', 'N/A')}")
        print(f"  - Duration: {disease_info.get('duration', 'N/A')}")
        symptoms = disease_info.get('common_symptoms', [])
        print(f"  - Symptoms: {', '.join(symptoms[:3])}")
    
    if care_plan:
        print(f"\n🏥 Care Plan:")
        immediate_care = care_plan.get('immediate_care', ['N/A'])
        print(f"  - Immediate Care: {immediate_care[0]}")
        medications = care_plan.get('medications', ['N/A'])
        print(f"  - Medications: {medications[0]}")
        lifestyle = care_plan.get('lifestyle_modifications', ['N/A'])
        print(f"  - Lifestyle: {lifestyle[0]}")
    
    # Test search functionality
    print(f"\n🔍 Search Test:")
    search_results = medical_dict.search_diseases('respiratory')
    print(f"  - Found {len(search_results)} respiratory diseases")
    
    # Test body system filtering
    print(f"\n🔍 Body System Test:")
    respiratory_diseases = medical_dict.get_diseases_by_body_system('Respiratory')
    print(f"  - Respiratory diseases: {len(respiratory_diseases)}")
    
    # Show all available diseases
    print(f"\n📚 All Available Diseases:")
    all_diseases = medical_dict.get_all_diseases()
    for i, disease in enumerate(all_diseases, 1):
        print(f"  {i}. {disease}")
    
    # Save sample output
    sample_output = {
        'disease_info': disease_info,
        'care_plan': care_plan,
        'search_results_count': len(search_results),
        'respiratory_diseases_count': len(respiratory_diseases),
        'all_diseases': all_diseases
    }
    
    with open('expanded_dict_demo.json', 'w', encoding='utf-8') as f:
        json.dump(sample_output, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Demo results saved to: expanded_dict_demo.json")
    print("="*50)
    print("🎉 EXPANDED MEDICAL DICTIONARY READY!")
    print("Features:")
    print("  ✅ 10 Common Diseases")
    print("  ✅ 8 Body Systems")
    print("  ✅ Comprehensive Care Plans")
    print("  ✅ Medical Terminology")
    print("  ✅ Search & Filter Functions")
    print("="*50)

if __name__ == "__main__":
    main()
