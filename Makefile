
.PHONY: install-sys-packages install-python-packages install-python-packages-colab download-data-from-google-drive

install-sys-packages:
	sudo apt update && sudo apt install espeak ffmpeg libespeak1

install-python-packages:
	pip install gTTS boto3 scikit-optimize botocore matplotlib numpy opencv_python pandas plotly scikit_learn tabulate easyocr

install-python-packages-colab:
	pip install gTTS boto3 scikit-optimize easyocr

download-data-from-google-drive:
	cp -r /content/drive/MyDrive/iam_dataset /
	rm -rf /words
	mkdir -p /words
	tar xvzf /iam_dataset/words.tgz -C /words
	rm -rf /forms
	mkdir -p /forms
	tar xvzf /iam_dataset/formsA-D.tgz -C /forms
	tar xvzf /iam_dataset/formsE-H.tgz -C /forms
	tar xvzf /iam_dataset/formsI-Z.tgz -C /forms
	rm -rf /words_label
	mkdir -p /words_label
	tar xvzf /iam_dataset/ascii.tgz -C /words_label