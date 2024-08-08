import requests
import json
import time

def make_video_call_request(usename: str, passwd: str, source_url:str, input_text:str):
    auth = (usename, passwd)

    url = "https://api.d-id.com/talks"

    payload = {
        "source_url": source_url,
        "script": {
            "type": "text",
            "subtitles": "false",
            "provider": {
                "type": "microsoft",
                "voice_id": "en-US-JennyNeural"
            },
            "input": input_text
        },
        "config": {
            "fluent": "false",
            "pad_audio": "0.0"
        }
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    response = requests.post(url, auth=auth, json=payload, headers=headers)

    print(response.text)
    job_id = json.loads(response.text)["id"]
    return job_id

def extract_video_link(usename: str, passwd: str, job_id: str):
    auth = (usename, passwd)
    url = f"https://api.d-id.com/talks/{job_id}"
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    response = requests.get(url, auth=auth, headers=headers)

    print(response.text)
    data = json.loads(response.text)["result_url"]
    return data

def download_video(url, filename):
  """
  Downloads a video from the given URL and saves it to the specified filename.

  Args:
      url (str): The URL of the video.
      filename (str): The filename to save the video as.
  """
  try:
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Raise an exception for unsuccessful requests
  except requests.exceptions.RequestException as e:
    print(f"Error downloading video: {e}")
    return

  # Check for video content type
  if not response.headers.get('Content-Type', '').startswith('video/'):
    print(f"URL '{url}' does not appear to contain a video.")
    return

  # Open the file for writing in binary mode
  with open(filename, 'wb') as f:
    for chunk in response.iter_content(1024):
      if chunk:  # filter out keep-alive new chunks
        f.write(chunk)
  print(f"Video downloaded successfully to '{filename}'.")

if __name__ == "__main__":

    job_id = make_video_call_request(usename="bmVlbEBhdmlhdG8uY29uc3VsdGluZw", passwd="pass", source_url="https://create-images-results.d-id.com/api_docs/assets/alice_getting_started_v3.png", input_text="""Hey Neel happy weekend,
I hope you're feeling okay today. It's important to take care of yourself, so make sure to get plenty of rest and stay hydrated by drinking lots of fluids like water, clear broth, or herbal tea. You might find over-the-counter pain relievers like Tylenol or Advil helpful for reducing fever and aches. A humidifier or a hot shower can also relieve congestion. Lastly, try to avoid contact with others to prevent spreading your illness. Take care and get well soon!""")
    print(job_id)
    print('-------------')
    time.sleep(20)
    video_url =extract_video_link(usename="bmVlbEBhdmlhdG8uY29uc3VsdGluZw", passwd="pass", job_id=job_id)
    # video_url = extract_video_link(usename="bmVlbEBhdmlhdG8uY29uc3VsdGluZw", passwd="pass", job_id="tlk_haaNlxDsVAUBWN3lTT9fu")
    print("---------")
    download_video(url=video_url, filename="intro2.mp4")