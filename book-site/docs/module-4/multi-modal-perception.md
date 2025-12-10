---
id: multi-modal-perception
title: "Multi-Modal Perception"
sidebar_label: "Multi-Modal Perception"
sidebar_position: 3
---

# Multi-Modal Perception

## Introduction

In this chapter, we'll explore how to combine vision and language to create a comprehensive understanding system. Multi-modal perception is crucial for robots to interpret complex scenes and respond to natural language queries about what they perceive.

## Learning Objectives

By the end of this chapter, you will be able to:
- Combine visual and linguistic information for scene understanding
- Implement vision-language fusion techniques
- Create systems that can answer questions about visual scenes
- Integrate perception with language understanding

## Overview

Multi-modal perception combines information from different sensory inputs (vision, language) to create richer representations than single-modal approaches. The system will:
1. Process visual input to identify objects and spatial relationships
2. Understand language queries about the visual scene
3. Fuse visual and linguistic information
4. Generate appropriate responses to queries

## Vision Processing Fundamentals

### Object Detection and Recognition

For vision processing, we'll use established computer vision techniques:

```python
import cv2
import numpy as np
from typing import List, Dict, Tuple
import torch
import torchvision.transforms as T

class VisionProcessor:
    def __init__(self):
        # Load pre-trained object detection model (e.g., YOLO, SSD, or similar)
        # For educational purposes, we'll simulate the detection process
        self.object_classes = [
            'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train',
            'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign',
            'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep',
            'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella',
            'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard',
            'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard',
            'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork',
            'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange',
            'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair',
            'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv',
            'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave',
            'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase',
            'scissors', 'teddy bear', 'hair drier', 'toothbrush'
        ]

    def detect_objects(self, image_path: str) -> List[Dict]:
        """
        Simulate object detection in an image
        Returns list of detected objects with bounding boxes and confidence
        """
        # In practice, this would use a real object detection model
        # For simulation, we'll return some sample objects
        image = cv2.imread(image_path)
        height, width, _ = image.shape

        # Simulated detections
        detections = [
            {
                'class': 'red cube',
                'confidence': 0.92,
                'bbox': [width * 0.3, height * 0.4, width * 0.1, height * 0.1],
                'center': (width * 0.35, height * 0.45)
            },
            {
                'class': 'blue cylinder',
                'confidence': 0.88,
                'bbox': [width * 0.6, height * 0.5, width * 0.1, height * 0.15],
                'center': (width * 0.65, height * 0.575)
            },
            {
                'class': 'green ball',
                'confidence': 0.95,
                'bbox': [width * 0.2, height * 0.7, width * 0.08, height * 0.08],
                'center': (width * 0.24, height * 0.74)
            }
        ]

        return detections

    def get_spatial_relationships(self, detections: List[Dict]) -> List[str]:
        """
        Determine spatial relationships between objects
        """
        relationships = []
        for i, obj1 in enumerate(detections):
            for j, obj2 in enumerate(detections):
                if i != j:
                    x1, y1 = obj1['center']
                    x2, y2 = obj2['center']

                    # Calculate relative position
                    dx = x2 - x1
                    dy = y2 - y1

                    if abs(dx) > abs(dy):  # Horizontal relationship is stronger
                        if dx > 0:
                            relationship = f"{obj1['class']} is to the left of {obj2['class']}"
                        else:
                            relationship = f"{obj1['class']} is to the right of {obj2['class']}"
                    else:  # Vertical relationship is stronger
                        if dy > 0:
                            relationship = f"{obj1['class']} is above {obj2['class']}"
                        else:
                            relationship = f"{obj1['class']} is below {obj2['class']}"

                    relationships.append(relationship)

        return relationships
```

### Scene Understanding

```python
class SceneInterpreter:
    def __init__(self):
        self.vision_processor = VisionProcessor()

    def interpret_scene(self, image_path: str) -> Dict:
        """
        Interpret the visual scene and extract meaningful information
        """
        # Detect objects in the scene
        objects = self.vision_processor.detect_objects(image_path)

        # Determine spatial relationships
        relationships = self.vision_processor.get_spatial_relationships(objects)

        # Create a scene description
        scene_description = {
            'objects': objects,
            'relationships': relationships,
            'object_count': len(objects),
            'scene_summary': self.generate_scene_summary(objects)
        }

        return scene_description

    def generate_scene_summary(self, objects: List[Dict]) -> str:
        """
        Generate a textual summary of the scene
        """
        if not objects:
            return "The scene appears to be empty."

        # Count objects by type
        object_counts = {}
        for obj in objects:
            obj_type = obj['class']
            object_counts[obj_type] = object_counts.get(obj_type, 0) + 1

        # Generate summary
        items = []
        for obj_type, count in object_counts.items():
            if count == 1:
                items.append(f"a {obj_type}")
            else:
                items.append(f"{count} {obj_type}s")

        if len(items) == 1:
            summary = f"The scene contains {items[0]}."
        elif len(items) == 2:
            summary = f"The scene contains {items[0]} and {items[1]}."
        else:
            summary = f"The scene contains {', '.join(items[:-1])}, and {items[-1]}."

        return summary
```

## Vision-Language Fusion

### Cross-Modal Attention

The key to multi-modal perception is effectively combining visual and linguistic information:

```python
import numpy as np
from typing import List, Dict

class VisionLanguageFusion:
    def __init__(self):
        # For educational purposes, we'll simulate embeddings
        # In practice, you'd use pre-trained models like CLIP
        self.vision_processor = VisionProcessor()
        self.scene_interpreter = SceneInterpreter()

    def encode_visual_features(self, image_path: str) -> np.ndarray:
        """
        Simulate encoding visual features from an image
        In practice, this would use a CNN or transformer model
        """
        # Simulate visual features as a random vector
        # In reality, this would come from a pre-trained vision model
        return np.random.rand(512)  # 512-dimensional feature vector

    def encode_textual_features(self, text: str) -> np.ndarray:
        """
        Simulate encoding textual features from text
        In practice, this would use a pre-trained language model
        """
        # Simulate text features as a random vector
        # In reality, this would come from a pre-trained language model
        return np.random.rand(512)  # 512-dimensional feature vector

    def compute_visual_text_alignment(self, image_path: str, query: str) -> Dict:
        """
        Compute alignment between visual elements and text query
        """
        # Get scene information
        scene_info = self.scene_interpreter.interpret_scene(image_path)

        # For each object, compute relevance to the query
        query_lower = query.lower()
        relevant_objects = []

        for obj in scene_info['objects']:
            obj_class = obj['class'].lower()
            confidence = obj['confidence']

            # Simple keyword matching for relevance
            relevance_score = 0.0
            if obj_class in query_lower:
                relevance_score = confidence
            elif any(keyword in query_lower for keyword in obj_class.split()):
                relevance_score = confidence * 0.7
            else:
                # Check if object is spatially relevant to query
                if 'near' in query_lower or 'by' in query_lower or 'next to' in query_lower:
                    relevance_score = confidence * 0.5

            if relevance_score > 0.3:  # Threshold for relevance
                relevant_objects.append({
                    'object': obj,
                    'relevance_score': relevance_score
                })

        return {
            'relevant_objects': relevant_objects,
            'scene_summary': scene_info['scene_summary'],
            'spatial_relationships': scene_info['relationships']
        }
```

## Question Answering System

### Visual Question Answering

```python
class VisualQuestionAnswering:
    def __init__(self):
        self.fusion_module = VisionLanguageFusion()
        self.scene_interpreter = SceneInterpreter()

    def answer_question(self, image_path: str, question: str) -> str:
        """
        Answer a natural language question about the visual scene
        """
        question_lower = question.lower()

        # Interpret the scene
        scene_info = self.scene_interpreter.interpret_scene(image_path)
        objects = scene_info['objects']

        # Process different types of questions
        if 'what' in question_lower and 'see' in question_lower:
            return self._answer_what_see_question(scene_info)

        elif 'where' in question_lower or 'location' in question_lower:
            return self._answer_where_question(question, scene_info)

        elif 'how many' in question_lower or 'count' in question_lower:
            return self._answer_count_question(scene_info)

        elif 'color' in question_lower:
            return self._answer_color_question(question, objects)

        elif 'shape' in question_lower:
            return self._answer_shape_question(question, objects)

        else:
            # Use fusion module for general questions
            fusion_result = self.fusion_module.compute_visual_text_alignment(
                image_path, question
            )

            if fusion_result['relevant_objects']:
                relevant_obj = fusion_result['relevant_objects'][0]['object']
                return f"I found {relevant_obj['class']} in the scene."
            else:
                return f"I couldn't find anything related to '{question}' in the scene."

    def _answer_what_see_question(self, scene_info: Dict) -> str:
        """Answer 'what do you see' type questions"""
        return scene_info['scene_summary']

    def _answer_where_question(self, question: str, scene_info: Dict) -> str:
        """Answer 'where is' type questions"""
        # Extract object from question
        import re
        # Look for object name in question
        for obj in scene_info['objects']:
            obj_name = obj['class'].lower()
            if obj_name in question.lower():
                # Find spatial relationships involving this object
                for relationship in scene_info['relationships']:
                    if obj_name in relationship:
                        return relationship

        # If no specific relationship found, just say where it is
        for obj in scene_info['objects']:
            if obj['class'].lower() in question.lower():
                x, y = obj['center']
                return f"The {obj['class']} is at position ({x:.0f}, {y:.0f}) in the image."

        return "I couldn't locate that object in the scene."

    def _answer_count_question(self, scene_info: Dict) -> str:
        """Answer 'how many' type questions"""
        count = scene_info['object_count']
        if count == 0:
            return "I don't see any objects in the scene."
        elif count == 1:
            return "I see one object in the scene."
        else:
            return f"I see {count} objects in the scene."

    def _answer_color_question(self, question: str, objects: List[Dict]) -> str:
        """Answer color-related questions"""
        for obj in objects:
            if obj['class'].lower() in question.lower():
                # Extract color from object name (assuming it's in the name)
                name_parts = obj['class'].split()
                colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple',
                         'pink', 'brown', 'black', 'white', 'gray', 'grey']

                for part in name_parts:
                    if part in colors:
                        return f"The {obj['class']} is {part}."

        return "I couldn't determine the color of that object."

    def _answer_shape_question(self, question: str, objects: List[Dict]) -> str:
        """Answer shape-related questions"""
        shapes = {
            'cube': 'cube-shaped',
            'cylinder': 'cylinder-shaped',
            'ball': 'spherical',
            'sphere': 'spherical',
            'box': 'box-shaped',
            'rectangular': 'rectangular'
        }

        for obj in objects:
            obj_name = obj['class'].lower()
            for shape, description in shapes.items():
                if shape in obj_name:
                    return f"The {obj['class']} is {description}."

        return "I couldn't determine the shape of that object."
```

## Integration with ROS 2

### Vision-Language Node

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from your_interfaces.srv import AnswerQuestion  # Custom service

class VisionLanguageNode(Node):
    def __init__(self):
        super().__init__('vision_language_node')

        # Initialize vision-language components
        self.vqa_system = VisualQuestionAnswering()

        # Subscriber for camera images
        self.image_subscriber = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        # Service to answer questions about the scene
        self.question_service = self.create_service(
            AnswerQuestion,
            'answer_vision_question',
            self.answer_question_callback
        )

        # Publisher for scene descriptions
        self.scene_publisher = self.create_publisher(
            String,
            'scene_description',
            10
        )

        # Store the latest image
        self.latest_image_path = None
        self.get_logger().info('Vision-Language node initialized')

    def image_callback(self, msg):
        """
        Handle incoming camera images
        In practice, you'd convert the ROS Image message to a format
        that can be processed by your vision system
        """
        # For this example, we'll assume the image is saved and we have a path
        # In reality, you'd convert msg.data to an image file or numpy array
        pass

    def answer_question_callback(self, request, response):
        """
        Answer a question about the current scene
        """
        try:
            if self.latest_image_path is None:
                response.success = False
                response.answer = "No image available to answer the question."
                return response

            # Answer the question using the VQA system
            answer = self.vqa_system.answer_question(
                self.latest_image_path,
                request.question
            )

            response.success = True
            response.answer = answer

            # Log the interaction
            self.get_logger().info(f"Question: {request.question}")
            self.get_logger().info(f"Answer: {answer}")

        except Exception as e:
            response.success = False
            response.answer = f"Error processing question: {str(e)}"

        return response

def main(args=None):
    rclpy.init(args=args)
    node = VisionLanguageNode()

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

## Practical Example: Scene Query System

Here's a complete example that demonstrates the multi-modal perception system:

```python
class MultiModalPerceptionSystem:
    def __init__(self):
        self.vision_processor = VisionProcessor()
        self.scene_interpreter = SceneInterpreter()
        self.fusion_module = VisionLanguageFusion()
        self.vqa_system = VisualQuestionAnswering()

    def process_scene_query(self, image_path: str, query: str) -> Dict:
        """
        Process a scene query combining vision and language
        """
        # Step 1: Interpret the scene
        scene_info = self.scene_interpreter.interpret_scene(image_path)

        # Step 2: Answer the query
        answer = self.vqa_system.answer_question(image_path, query)

        # Step 3: Compute visual-text alignment
        alignment = self.fusion_module.compute_visual_text_alignment(
            image_path, query
        )

        # Step 4: Package results
        result = {
            'query': query,
            'answer': answer,
            'scene_info': scene_info,
            'alignment': alignment,
            'confidence': self._compute_confidence(alignment, answer)
        }

        return result

    def _compute_confidence(self, alignment: Dict, answer: str) -> float:
        """
        Compute confidence in the answer based on alignment quality
        """
        if not alignment['relevant_objects'] and 'couldn\'t find' in answer.lower():
            return 0.3  # Low confidence when nothing found
        elif alignment['relevant_objects']:
            avg_relevance = np.mean([
                obj['relevance_score'] for obj in alignment['relevant_objects']
            ])
            return min(1.0, avg_relevance + 0.2)  # Boost slightly
        else:
            return 0.8  # Default confidence for general answers

# Example usage
def example_usage():
    system = MultiModalPerceptionSystem()

    # Simulate an image path (in practice, this would be a real image)
    image_path = "simulated_scene.jpg"

    # Example queries
    queries = [
        "What objects do you see?",
        "Where is the red cube?",
        "How many objects are there?",
        "What color is the cylinder?"
    ]

    for query in queries:
        result = system.process_scene_query(image_path, query)
        print(f"Query: {query}")
        print(f"Answer: {result['answer']}")
        print(f"Confidence: {result['confidence']:.2f}")
        print("-" * 50)

if __name__ == "__main__":
    example_usage()
```

## Exercise: Implement a Custom Scene Understanding Component

Create a component that can understand and describe spatial arrangements:

1. Create a function that describes the layout of a room
2. Implement spatial reasoning for relative positions
3. Add support for containment relationships (objects inside other objects)

Example solution:

```python
class SpatialReasoning:
    def __init__(self):
        self.relative_positions = {
            'left': lambda p1, p2: p1[0] < p2[0],
            'right': lambda p1, p2: p1[0] > p2[0],
            'above': lambda p1, p2: p1[1] < p2[1],  # In image coordinates, y increases downward
            'below': lambda p1, p2: p1[1] > p2[1],
            'near': lambda p1, p2: np.linalg.norm(np.array(p1) - np.array(p2)) < 100,  # pixels
        }

    def describe_room_layout(self, objects: List[Dict]) -> str:
        """
        Describe the general layout of objects in the room
        """
        if len(objects) < 2:
            return "The room has very few objects."

        # Group objects by area
        left_objects = [obj for obj in objects if obj['center'][0] < 0.5]  # Left half
        right_objects = [obj for obj in objects if obj['center'][0] >= 0.5]  # Right half
        top_objects = [obj for obj in objects if obj['center'][1] < 0.5]  # Top half
        bottom_objects = [obj for obj in objects if obj['center'][1] >= 0.5]  # Bottom half

        description = "The room is organized as follows:\n"

        if left_objects:
            left_names = [obj['class'] for obj in left_objects]
            description += f"- Left side: {', '.join(left_names)}\n"

        if right_objects:
            right_names = [obj['class'] for obj in right_objects]
            description += f"- Right side: {', '.join(right_names)}\n"

        if top_objects:
            top_names = [obj['class'] for obj in top_objects]
            description += f"- Upper area: {', '.join(top_names)}\n"

        if bottom_objects:
            bottom_names = [obj['class'] for obj in bottom_objects]
            description += f"- Lower area: {', '.join(bottom_names)}\n"

        return description

    def find_containment(self, objects: List[Dict]) -> List[str]:
        """
        Find potential containment relationships
        """
        containments = []

        # In a real system, you'd use 3D information or semantic understanding
        # For simulation, we'll use simple heuristics
        for obj1 in objects:
            for obj2 in objects:
                if obj1 != obj2:
                    # Check if obj1 could be inside obj2 based on size and position
                    # This is a simplified heuristic
                    if ('box' in obj2['class'] or 'container' in obj2['class']) and \
                       ('cube' in obj1['class'] or 'ball' in obj1['class']):
                        if self._is_within_bounds(obj1, obj2):
                            containments.append(f"{obj1['class']} is inside {obj2['class']}")

        return containments

    def _is_within_bounds(self, inner_obj: Dict, outer_obj: Dict) -> bool:
        """
        Check if inner object is within bounds of outer object
        """
        inner_center = inner_obj['center']
        outer_bbox = outer_obj['bbox']

        x, y = inner_center
        x_min, y_min, width, height = outer_bbox
        x_max, y_max = x_min + width, y_min + height

        return x_min <= x <= x_max and y_min <= y <= y_max
```

## Summary

In this chapter, we've covered:
- Vision processing fundamentals for object detection
- Scene interpretation and description
- Vision-language fusion techniques
- Visual question answering systems
- Integration with ROS 2 for real-time applications
- Spatial reasoning and scene understanding

## Key Takeaways

- Multi-modal perception combines visual and linguistic information for richer understanding
- Cross-modal attention mechanisms help align vision and language
- Visual question answering enables natural interaction with robotic systems
- Spatial reasoning is crucial for understanding object relationships
- ROS 2 integration enables real-time multi-modal perception in robotics

## Next Steps

In the next chapter, we'll explore autonomous task execution, combining the perception and language understanding we've developed with action planning and execution.