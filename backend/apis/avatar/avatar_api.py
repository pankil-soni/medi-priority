from flask import Flask, request, send_file, jsonify
import os
from make_video import make_video

app = Flask(__name__)



@app.route('/generate-video', methods=['POST'])
def generate_video_endpoint():
    try:
        data = request.json
        general_info = data.get('general_information')
        vision_info = data.get('vision_information')
        
        if not general_info or not vision_info:
            return jsonify({"error": "Both 'general_information' and 'video_information' are required"}), 400
        
        
        make_video(general_info, vision_info)
        
        output_path = "intro2.mp4"
        # Send the generated video as a response
        return send_file(output_path, as_attachment=True)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
