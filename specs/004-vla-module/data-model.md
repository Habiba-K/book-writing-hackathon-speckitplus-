# Data Model: VLA Module (Theoretical Framework)

## Core Theoretical Entities

### VoiceCommand
- **transcription**: string - Text representation of speech input
- **confidence**: float - Confidence score of speech recognition (0.0-1.0)
- **timestamp**: datetime - Time of command receipt
- **status**: enum - Processing state (RECEIVED, TRANSCRIBING, PROCESSED, FAILED)

### Intent
- **command_text**: string - Original transcribed text
- **action_type**: string - Categorical action classification (PICK_UP, MOVE_TO, IDENTIFY, etc.)
- **parameters**: object - Action-specific parameters (object_name, location, etc.)
- **confidence**: float - Confidence score of intent classification (0.0-1.0)

### VisionData
- **timestamp**: datetime - Time of image capture
- **detected_objects**: array - List of identified objects with properties
- **scene_description**: string - Textual description of the visual scene
- **spatial_relationships**: object - Relationships between objects in the scene

### ActionCommand
- **action_type**: string - Type of robot action to execute
- **parameters**: object - Action-specific parameters
- **target_robot**: string - Identifier of target robot
- **timeout**: int - Maximum execution time (seconds)

## Theoretical Data Flow

```
VoiceCommand → Intent → ActionCommand
VisionData → PerceptionResult → ActionCommand
Intent + VisionData → Fused Command → ActionCommand
```

## Theoretical Validation Rules

1. **VoiceCommand**: Must have non-empty transcription and valid confidence score
2. **Intent**: Must have valid action_type and required parameters
3. **VisionData**: Must have valid timestamp and non-empty detected_objects array
4. **ActionCommand**: Must have valid action_type and appropriate parameters

## Theoretical Serialization Format

All data objects follow JSON format for theoretical compatibility with message passing systems, with binary data (audio, images) conceptually base64 encoded when included in messages.