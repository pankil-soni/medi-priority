general_information = """
    general_information = "Patient Name: Sneh Age: 20 Symptoms: - Low fever (99 degrees Fahrenheit) - Cold - Cough Pain Assessment:  None provided Medication: Paracetamol, effective for a few hours Symptom Duration: 2 days Additional Information: None"
    """
visual_information = """
Skin Color and Condition:
Pale Skin: The patient's skin appears slightly pale, which could indicate anemia, shock, or lack of oxygen.
Yellowish Skin (Jaundice): No signs of yellowing are observed in the skin.
Blue Skin or Lips (Cyanosis): No blue discoloration is visible on the skin or lips.
Redness: There is significant redness on the cheeks and nose, which may suggest a condition like rosacea.
Rashes or Hives: No rashes or hives are visible on the face.
Pimples, Pustules, or Pox: No pimples, pustules, or pox are observed.

Eyes:
Dark Circles: There are dark circles under the eyes, suggesting sleep deprivation, stress, or chronic fatigue.
Yellowing (Scleral Icterus): No yellowing is observed in the sclera.
Red or Bloodshot Eyes: The eyes appear slightly red or bloodshot, which could indicate an infection, allergy, or irritation.
Drooping Eyelids (Ptosis): The eyelids appear slightly droopy, which may be due to fatigue or neurological issues.

Mouth and Lips:
Blue Lips (Cyanosis): The lips appear slightly blue, indicating poor oxygenation.
Swollen Lips: There is no swelling observed on the lips.
Cracked or Dry Lips: The lips appear dry, which may indicate dehydration or vitamin deficiencies.

Neck region:
Swollen Glands: No swollen glands are visible in the neck region.
Visible Thyroid Enlargement (Goiter): The thyroid gland is not visibly enlarged.
"""
    
import requests

# Define the URL for the API endpoint
url = 'http://127.0.0.1:5000/generate-video'

# Define the payload with general_information and video_information
payload = {
    "general_information": general_information,
    "vision_information": visual_information
}

# Send a POST request to the API
response = requests.post(url, json=payload)

# Check the response status code
if response.status_code == 200:
    # Save the received video file
    with open('received_video.mp4', 'wb') as video_file:
        video_file.write(response.content)
    print("Video received and saved as 'received_video.mp4'")
else:
    print(f"Failed to receive video. Status code: {response.status_code}")
    print(f"Response: {response.json()}")
