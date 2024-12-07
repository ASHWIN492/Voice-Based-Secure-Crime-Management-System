'''from cryptography.fernet import Fernet

# Generate a Fernet key
key = Fernet.generate_key()
print("Generated key:", key.decode())  # Print and save this key securely'''
import subprocess

def convert_to_mp4(input_path, output_path):
    ffmpeg_command = [
        'ffmpeg', '-i', input_path,
        '-vcodec', 'h264', '-acodec', 'aac',
        '-strict', 'experimental', output_path
    ]
    subprocess.run(ffmpeg_command)
    


convert_to_mp4("../static/uploads/crimevideos/weapon detection coding.mp4","../static/uploads/weapon detection coding.mp4")
print("done")