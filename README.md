# text_to_emotion
i have made gui based text to emotion project using python and few more libraries it is related to NLP


Text to Emotion Detector 🎭
============================

This project is an AI-based GUI application that detects the emotion from the input text using a Hugging Face Transformer model and displays a corresponding emoji. It also features a fun word-scramble game mode, history saving, and text-to-speech.

Repository: https://github.com/MuhammadTalhaCharan/text_to_emotion

------------------------
📌 Features
------------------------
- Detect emotions from text using Hugging Face transformer model.
- Shows appropriate emoji for the detected emotion.
- Fun Game Mode to unscramble emotion-related words.
- Save and view emotion detection history.
- Text-to-speech support (if pyttsx3 is installed).
- Clean and user-friendly GUI built with Tkinter.

------------------------
🧠 How it Works
------------------------
1. User enters text in the GUI.
2. The Hugging Face model (`j-hartmann/emotion-english-distilroberta-base`) predicts the dominant emotion.
3. The app displays a matching emoji and saves the text/emotion to a local JSON file.
4. Game Mode lets users unscramble emotion words for engagement.

------------------------
🛠️ Requirements
------------------------
- Python 3.7+
- Install the required libraries:

```
pip install transformers torch tkinter pyttsx3
```

*Note:* On some systems you may also need:
```
pip install sentencepiece
```

------------------------
🚀 How to Run
------------------------
1. download this repository:
```
git clone https://github.com/MuhammadTalhaCharan/text_to_emotion

```

2. Install the requirements:
```
3. Run the app:
```
python text_to_emotion.py
```

------------------------
💾 Creating Executable (Windows)
------------------------
To create an `.exe` file for Windows:

1. Make sure `pyinstaller` is installed:
```
pip install pyinstaller
```

2. Generate the executable:
```
pyinstaller --onefile --windowed text_to_emotion.py
```

3. Your `.exe` will be found in the `dist` folder.

YOU CAN GENERATE BUT FOR NOW IAM FACING WINDOWS ISSUE SO THE EXE IS NOT BUILDING PROPERLY.

------------------------
📁 Files in this Repo
------------------------
- `text_to_emotion.py`: Main Python script.
- `emotion_history.json`: Stores recent emotion detection results.
- `README.txt`: This file.

------------------------
🙌 THANKS
