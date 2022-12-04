
.PHONY: install-sys-packages install-python-packages download-data-from-google-drive

install-sys-packages:
	sudo apt update && sudo apt install espeak ffmpeg libespeak1

install-python-packages:
	pip install gTTS boto3 scikit-optimize

download-data-from-google-drive:
	cp -r /content/drive/MyDrive/521\ ML\ \ final\ project/dataset/iam/compressed /
	rm -rf /words
	mkdir -p /words
	tar xvzf /compressed/words.tgz -C /words
	rm -rf /lines
	mkdir -p /lines
	tar xvzf /compressed/lines.tgz -C /lines
	rm -rf /forms
	mkdir -p /forms
	tar xvzf /compressed/formsA-D.tgz -C /forms
	tar xvzf /compressed/formsE-H.tgz -C /forms
	tar xvzf /compressed/formsI-Z.tgz -C /forms
	rm -rf /words_label
	mkdir -p /words_label
	tar xvzf /compressed/ascii.tgz -C /words_label
	rm -rf /xml
	mkdir -p /xml
	tar xvzf /compressed/xml.tgz -C /xml
	rm -rf /samples
	mkdir -p /samples
	cp -r /content/drive/MyDrive/521\ ML\ \ final\ project/dataset/iam/samples/* /samples/
