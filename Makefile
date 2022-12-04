
.PHONY: install-sys-packages install-python-packages

install-sys-packages:
	sudo apt update && sudo apt install espeak ffmpeg libespeak1

install-python-packages:
	pip install gTTS boto3 scikit-optimize
