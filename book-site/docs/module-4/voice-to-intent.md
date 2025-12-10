---
id: voice-to-intent
title: "Voice to Intent"
sidebar_label: "Voice to Intent"
sidebar_position: 1
---

# Voice to Intent

## Introduction

In this chapter, we'll explore how to convert voice commands to text and extract meaningful intent from natural language. This forms the foundation of our Vision-Language-Action (VLA) pipeline, enabling robots to understand human speech and respond appropriately.

## Learning Objectives

By the end of this chapter, you will be able to:
- Implement speech-to-text conversion using Whisper
- Extract intent from transcribed speech
- Map natural language to actionable commands
- Handle voice input in a robotic system

## Overview

Voice-to-intent processing is a critical component of human-robot interaction. The process involves:
1. Capturing audio input from the user
2. Converting speech to text using automatic speech recognition (ASR)
3. Analyzing the text to extract the user's intent
4. Mapping the intent to specific robot actions

## OpenAI Whisper Integration

OpenAI's Whisper is a state-of-the-art speech recognition model that can convert speech to text with high accuracy. It supports multiple languages and can run offline, making it ideal for robotic applications.

### Installation

First, install the required dependencies:

```bash
pip install openai-whisper
pip install torch
```

### Basic Whisper Usage

```python
import whisper

# Load the model (tiny, base, small, medium, large)
model = whisper.load_model("tiny")

# Transcribe audio file
result = model.transcribe("audio_file.wav")
print(result["text"])
```

## Speech-to-Text Pipeline

### Audio Preprocessing

Before feeding audio to Whisper, we may need to preprocess it:

```python
import librosa
import numpy as np

def preprocess_audio(audio_path, target_sr=16000):
    # Load audio file
    audio, sr = librosa.load(audio_path, sr=target_sr)

    # Normalize audio
    audio = audio / np.max(np.abs(audio))

    return audio
```

### Real-time Audio Processing

For real-time applications, we can use PyAudio to capture microphone input:

```python
import pyaudio
import wave
import whisper

def record_audio(duration=5, sample_rate=16000, chunk_size=1024):
    p = pyaudio.PyAudio()

    stream = p.open(
        format=pyaudio.paFloat32,
        channels=1,
        rate=sample_rate,
        input=True,
        frames_per_buffer=chunk_size
    )

    print("Recording...")
    frames = []

    for _ in range(0, int(sample_rate / chunk_size * duration)):
        data = stream.read(chunk_size)
        frames.append(data)

    print("Recording finished.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save to temporary file
    wf = wave.open("temp_audio.wav", 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paFloat32))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()

    return "temp_audio.wav"
```

## Intent Classification

After converting speech to text, we need to extract the user's intent. For educational purposes, we'll implement a simple keyword-based approach.

### Basic Intent Classifier

```python
import re
from enum import Enum
from dataclasses import dataclass
from typing import Optional

class IntentType(Enum):
    PICK_UP = "pick_up"
    MOVE_TO = "move_to"
    IDENTIFY = "identify"
    GREET = "greet"
    FOLLOW = "follow"
    STOP = "stop"

@dataclass
class Intent:
    intent_type: IntentType
    confidence: float
    parameters: dict
    entities: list

class IntentClassifier:
    def __init__(self):
        self.intent_patterns = {
            IntentType.PICK_UP: [
                r"pick.*up.*([a-zA-Z\s]+)",
                r"grab.*([a-zA-Z\s]+)",
                r"take.*([a-zA-Z\s]+)",
                r"get.*([a-zA-Z\s]+)"
            ],
            IntentType.MOVE_TO: [
                r"go.*to.*([a-zA-Z\s]+)",
                r"move.*to.*([a-zA-Z\s]+)",
                r"walk.*to.*([a-zA-Z\s]+)",
                r"navigate.*to.*([a-zA-Z\s]+)"
            ],
            IntentType.IDENTIFY: [
                r"what.*([a-zA-Z\s]+).*see",
                r"where.*([a-zA-Z\s]+)",
                r"find.*([a-zA-Z\s]+)",
                r"locate.*([a-zA-Z\s]+)"
            ]
        }

    def classify(self, text: str) -> Optional[Intent]:
        text_lower = text.lower()

        for intent_type, patterns in self.intent_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, text_lower)
                if match:
                    entities = list(match.groups())
                    parameters = {"target": entities[0].strip() if entities else ""}

                    return Intent(
                        intent_type=intent_type,
                        confidence=0.9,  # High confidence for keyword match
                        parameters=parameters,
                        entities=entities
                    )

        # If no pattern matches, return None or a default intent
        return Intent(
            intent_type=IntentType.IDENTIFY,
            confidence=0.5,
            parameters={"query": text},
            entities=[]
        )
```

## Voice Command Processing Pipeline

Now let's combine everything into a complete pipeline:

```python
import whisper
import os
from pathlib import Path

class VoiceProcessor:
    def __init__(self, whisper_model="tiny"):
        self.model = whisper.load_model(whisper_model)
        self.intent_classifier = IntentClassifier()

    def process_voice_command(self, audio_path: str) -> Intent:
        # Step 1: Transcribe audio
        result = self.model.transcribe(audio_path)
        transcription = result["text"]

        # Step 2: Classify intent
        intent = self.intent_classifier.classify(transcription)

        return intent

    def process_real_time(self, duration=5) -> Intent:
        # Record audio
        audio_path = record_audio(duration)

        # Process the recorded audio
        intent = self.process_voice_command(audio_path)

        # Clean up temporary file
        if os.path.exists(audio_path):
            os.remove(audio_path)

        return intent
```

## Command Validation

It's important to validate commands before executing them:

```python
class CommandValidator:
    def __init__(self):
        self.valid_objects = [
            "cube", "ball", "cylinder", "box", "cup",
            "bottle", "book", "phone", "table", "chair"
        ]
        self.valid_locations = [
            "kitchen", "living room", "bedroom", "office",
            "dining room", "bathroom", "hallway"
        ]

    def validate_intent(self, intent: Intent) -> bool:
        if intent.intent_type == IntentType.PICK_UP:
            target = intent.parameters.get("target", "").lower()
            # Simple validation - check if target contains any known object
            for obj in self.valid_objects:
                if obj in target:
                    return True
            return False

        elif intent.intent_type == IntentType.MOVE_TO:
            target = intent.parameters.get("target", "").lower()
            for loc in self.valid_locations:
                if loc in target:
                    return True
            return False

        return True  # Other intents are considered valid by default
```

## Integration with ROS 2

To connect with ROS 2, we can create a service that processes voice commands:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from vla_interfaces.srv import ProcessVoiceCommand  # Custom service

class VoiceToIntentNode(Node):
    def __init__(self):
        super().__init__('voice_to_intent_node')
        self.voice_processor = VoiceProcessor()
        self.validator = CommandValidator()

        # Service to process voice commands
        self.srv = self.create_service(
            ProcessVoiceCommand,
            'process_voice_command',
            self.process_voice_callback
        )

        # Publisher for recognized commands
        self.command_publisher = self.create_publisher(String, 'voice_commands', 10)

    def process_voice_callback(self, request, response):
        try:
            # Process the voice command
            intent = self.voice_processor.process_voice_command(request.audio_path)

            # Validate the command
            is_valid = self.validator.validate_intent(intent)

            if is_valid:
                # Publish the recognized command
                cmd_msg = String()
                cmd_msg.data = f"{intent.intent_type.value}: {intent.parameters}"
                self.command_publisher.publish(cmd_msg)

                response.success = True
                response.intent_type = intent.intent_type.value
                response.parameters = str(intent.parameters)
                response.confidence = intent.confidence
            else:
                response.success = False
                response.error_message = "Invalid command"

        except Exception as e:
            response.success = False
            response.error_message = str(e)

        return response

def main(args=None):
    rclpy.init(args=args)
    node = VoiceToIntentNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Exercise: Implement Your Own Voice Command Handler

Create a simple voice command handler that:
1. Takes a text input (simulating transcribed speech)
2. Implements at least 3 different intent types
3. Extracts relevant parameters from the command
4. Validates the command against a predefined list of objects

Example solution:

```python
def simple_voice_handler(text: str):
    # Convert to lowercase for easier processing
    text_lower = text.lower()

    # Simple intent detection
    if "pick up" in text_lower or "grab" in text_lower:
        # Extract object to pick up
        import re
        match = re.search(r"(?:pick up|grab)\s+(.+)", text_lower)
        if match:
            obj = match.group(1).strip()
            return {"intent": "pick_up", "object": obj, "confidence": 0.9}

    elif "go to" in text_lower or "move to" in text_lower:
        # Extract location
        import re
        match = re.search(r"(?:go to|move to)\s+(.+)", text_lower)
        if match:
            location = match.group(1).strip()
            return {"intent": "move_to", "location": location, "confidence": 0.9}

    elif "what" in text_lower and ("see" in text_lower or "is" in text_lower):
        return {"intent": "identify", "query": text_lower, "confidence": 0.8}

    return {"intent": "unknown", "confidence": 0.1}

# Test the handler
print(simple_voice_handler("Please pick up the red cube"))
print(simple_voice_handler("Go to the kitchen"))
print(simple_voice_handler("What objects do you see?"))
```

## Summary

In this chapter, we've covered the fundamentals of voice-to-intent processing:
- Speech-to-text conversion using Whisper
- Basic intent classification using pattern matching
- Command validation techniques
- Integration concepts with ROS 2

## Key Takeaways

- Whisper provides accurate offline speech recognition
- Intent classification can be implemented with pattern matching for educational purposes
- Command validation is crucial for safe robot operation
- Real-time audio processing requires careful resource management

## Next Steps

In the next chapter, we'll explore how to map these natural language intents to ROS 2 actions, creating a complete voice-to-action pipeline.