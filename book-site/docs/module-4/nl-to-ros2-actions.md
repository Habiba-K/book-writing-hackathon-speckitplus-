---
id: nl-to-ros2-actions
title: "NL to ROS 2 Actions"
sidebar_label: "NL to ROS 2 Actions"
sidebar_position: 2
---

# NL to ROS 2 Actions

## Introduction

In this chapter, we'll explore how to map natural language commands to ROS 2 actions. Building on the voice-to-intent processing from the previous chapter, we'll create a system that translates human language into robot behaviors using the ROS 2 framework.

## Learning Objectives

By the end of this chapter, you will be able to:
- Map natural language intents to ROS 2 action clients
- Create action servers for robotic tasks
- Implement parameter extraction for action commands
- Handle action execution and feedback

## Overview

The Natural Language to ROS 2 Actions pipeline involves:
1. Receiving intent and parameters from the voice processing module
2. Mapping the intent to appropriate ROS 2 action types
3. Creating action goals with extracted parameters
4. Executing actions through ROS 2 action clients
5. Handling action feedback and results

## ROS 2 Action Fundamentals

ROS 2 actions are a way to communicate between nodes for long-running tasks. They provide feedback during execution and can be preempted if needed.

### Action Structure

An action definition has three parts:
- **Goal**: The desired outcome
- **Feedback**: Status updates during execution
- **Result**: Final outcome of the action

### Example Action Definition

```
# Goal: Object to pick up
string object_name
---
# Result: Success or failure
bool success
string message
---
# Feedback: Current progress
string status
float64 progress
```

## Setting Up Action Clients

First, let's create an action client to interact with robot actions:

```python
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node

# Import action definitions (these would be in your custom package)
from your_robot_interfaces.action import PickObject, NavigateToPose, FindObject

class NLToROS2ActionsNode(Node):
    def __init__(self):
        super().__init__('nl_to_ros2_actions_node')

        # Action clients for different robot capabilities
        self.pick_client = ActionClient(self, PickObject, 'pick_object')
        self.navigate_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        self.find_client = ActionClient(self, FindObject, 'find_object')

        # Subscriber for voice commands
        self.subscription = self.create_subscription(
            String,
            'voice_commands',
            self.voice_command_callback,
            10
        )

        # Wait for action servers to be available
        self.pick_client.wait_for_server()
        self.navigate_client.wait_for_server()
        self.find_client.wait_for_server()

    def voice_command_callback(self, msg):
        # Parse the command from the message
        command_data = self.parse_command(msg.data)
        intent = command_data['intent']
        parameters = command_data['parameters']

        # Execute the appropriate action based on intent
        if intent == 'pick_up':
            self.execute_pick_action(parameters)
        elif intent == 'move_to':
            self.execute_navigate_action(parameters)
        elif intent == 'identify':
            self.execute_find_action(parameters)

    def parse_command(self, command_str):
        # Parse the command string to extract intent and parameters
        parts = command_str.split(':')
        intent = parts[0].strip()
        parameters = eval(parts[1].strip()) if len(parts) > 1 else {}
        return {'intent': intent, 'parameters': parameters}
```

## Action Mapping Implementation

### Pick Action Implementation

```python
from your_robot_interfaces.action import PickObject
from rclpy.action import GoalResponse, CancelResponse
from rclpy.action.server import ActionServer, ServerGoalHandle

class PickActionServer(Node):
    def __init__(self):
        super().__init__('pick_action_server')
        self._action_server = ActionServer(
            self,
            PickObject,
            'pick_object',
            self.execute_callback
        )

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing pick object action...')

        feedback_msg = PickObject.Feedback()
        result = PickObject.Result()

        object_name = goal_handle.request.object_name
        self.get_logger().info(f'Trying to pick up {object_name}')

        # Update feedback
        feedback_msg.status = f'Locating {object_name}'
        feedback_msg.progress = 0.1
        goal_handle.publish_feedback(feedback_msg)

        # Simulate object localization
        if self.localize_object(object_name):
            feedback_msg.status = f'Approaching {object_name}'
            feedback_msg.progress = 0.4
            goal_handle.publish_feedback(feedback_msg)

            # Simulate approach
            if self.approach_object(object_name):
                feedback_msg.status = f'Grasping {object_name}'
                feedback_msg.progress = 0.7
                goal_handle.publish_feedback(feedback_msg)

                # Simulate grasp
                if self.grasp_object(object_name):
                    result.success = True
                    result.message = f'Successfully picked up {object_name}'
                    goal_handle.succeed()
                else:
                    result.success = False
                    result.message = f'Failed to grasp {object_name}'
                    goal_handle.abort()
            else:
                result.success = False
                result.message = f'Failed to approach {object_name}'
                goal_handle.abort()
        else:
            result.success = False
            result.message = f'Could not locate {object_name}'
            goal_handle.abort()

        return result

    def localize_object(self, object_name):
        # Simulate object localization
        # In practice, this would use perception systems
        self.get_logger().info(f'Localizing {object_name}')
        return True  # Simulate success

    def approach_object(self, object_name):
        # Simulate robot approaching the object
        self.get_logger().info(f'Approaching {object_name}')
        return True  # Simulate success

    def grasp_object(self, object_name):
        # Simulate robot grasping the object
        self.get_logger().info(f'Grasping {object_name}')
        return True  # Simulate success
```

### Navigation Action Implementation

```python
from your_robot_interfaces.action import NavigateToPose
import math

class NavigateActionServer(Node):
    def __init__(self):
        super().__init__('navigate_action_server')
        self._action_server = ActionServer(
            self,
            NavigateToPose,
            'navigate_to_pose',
            self.execute_callback
        )

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing navigation action...')

        feedback_msg = NavigateToPose.Feedback()
        result = NavigateToPose.Result()

        target_location = goal_handle.request.target_location
        self.get_logger().info(f'Navigating to {target_location}')

        # Update feedback
        feedback_msg.status = f'Planning path to {target_location}'
        feedback_msg.progress = 0.1
        goal_handle.publish_feedback(feedback_msg)

        # Plan path
        path = self.plan_path(target_location)
        if path:
            feedback_msg.status = f'Executing navigation to {target_location}'
            feedback_msg.progress = 0.3
            goal_handle.publish_feedback(feedback_msg)

            # Execute navigation
            if self.execute_navigation(path):
                result.success = True
                result.message = f'Successfully reached {target_location}'
                goal_handle.succeed()
            else:
                result.success = False
                result.message = f'Failed to navigate to {target_location}'
                goal_handle.abort()
        else:
            result.success = False
            result.message = f'Could not plan path to {target_location}'
            goal_handle.abort()

        return result

    def plan_path(self, target_location):
        # Simulate path planning
        # In practice, this would use navigation2 stack
        self.get_logger().info(f'Planning path to {target_location}')
        return True  # Simulate success

    def execute_navigation(self, path):
        # Simulate navigation execution
        self.get_logger().info('Executing navigation')
        return True  # Simulate success
```

## Parameter Extraction and Validation

When mapping natural language to actions, we need to extract and validate parameters:

```python
class ParameterExtractor:
    def __init__(self):
        self.object_synonyms = {
            'red cube': ['red cube', 'red block', 'red box'],
            'blue cylinder': ['blue cylinder', 'blue tube', 'blue can'],
            'green ball': ['green ball', 'green sphere', 'green orb']
        }

        self.location_synonyms = {
            'kitchen': ['kitchen', 'cooking area', 'stove area'],
            'living room': ['living room', 'sitting room', 'lounge'],
            'bedroom': ['bedroom', 'sleeping room', 'bed room']
        }

    def extract_object_parameter(self, text, intent):
        text_lower = text.lower()

        # Look for known objects
        for canonical_name, synonyms in self.object_synonyms.items():
            for synonym in synonyms:
                if synonym in text_lower:
                    return canonical_name

        # If no known object found, return the noun phrase
        # This would require more sophisticated NLP in practice
        return self.extract_noun_phrase(text)

    def extract_location_parameter(self, text, intent):
        text_lower = text.lower()

        # Look for known locations
        for canonical_name, synonyms in self.location_synonyms.items():
            for synonym in synonyms:
                if synonym in text_lower:
                    return canonical_name

        return self.extract_location_from_text(text)

    def extract_noun_phrase(self, text):
        # Simplified noun phrase extraction
        # In practice, use NLTK or spaCy for better results
        words = text.split()
        for i, word in enumerate(words):
            if word.lower() in ['the', 'a', 'an']:
                continue
            # Look for potential objects after determiners
            if i + 1 < len(words):
                return f"{word} {words[i+1]}"
        return text  # Return full text if no pattern found

    def extract_location_from_text(self, text):
        # Simplified location extraction
        words = text.split()
        for word in words:
            if word.lower() in ['kitchen', 'bedroom', 'living', 'office', 'bathroom', 'dining']:
                return word
        return "unknown_location"
```

## Action Execution Manager

To handle the execution of actions based on voice commands:

```python
class ActionExecutionManager:
    def __init__(self, node):
        self.node = node
        self.parameter_extractor = ParameterExtractor()

    def execute_pick_action(self, parameters):
        # Extract object name from parameters
        object_name = parameters.get('target', 'unknown')

        # Create goal for pick action
        goal_msg = PickObject.Goal()
        goal_msg.object_name = object_name

        # Send goal to action server
        self.node.get_logger().info(f'Sending pick goal for {object_name}')

        # Use async send goal to not block the node
        future = self.node.pick_client.send_goal_async(
            goal_msg,
            feedback_callback=self.pick_feedback_callback
        )

        # Add done callback to handle result
        future.add_done_callback(self.pick_goal_response_callback)

    def execute_navigate_action(self, parameters):
        # Extract location from parameters
        location = parameters.get('target', 'unknown')

        # Create goal for navigation action
        goal_msg = NavigateToPose.Goal()
        goal_msg.target_location = location

        # Send goal to action server
        self.node.get_logger().info(f'Sending navigation goal to {location}')

        future = self.node.navigate_client.send_goal_async(
            goal_msg,
            feedback_callback=self.navigate_feedback_callback
        )

        future.add_done_callback(self.navigate_goal_response_callback)

    def execute_find_action(self, parameters):
        # Extract object to find from parameters
        query = parameters.get('query', 'objects')

        # Create goal for find action
        goal_msg = FindObject.Goal()
        goal_msg.query = query

        # Send goal to action server
        self.node.get_logger().info(f'Sending find goal for {query}')

        future = self.node.find_client.send_goal_async(
            goal_msg,
            feedback_callback=self.find_feedback_callback
        )

        future.add_done_callback(self.find_goal_response_callback)

    def pick_feedback_callback(self, feedback_msg):
        self.node.get_logger().info(
            f'Pick action feedback: {feedback_msg.status} '
            f'({feedback_msg.progress:.1%})'
        )

    def pick_goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.node.get_logger().info('Pick goal was rejected')
            return

        get_result_future = goal_handle.get_result_async()
        get_result_future.add_done_callback(self.pick_result_callback)

    def pick_result_callback(self, future):
        result = future.result().result
        self.node.get_logger().info(f'Pick result: {result.success} - {result.message}')

    # Similar callback methods for navigate and find actions...
```

## Natural Language Understanding Integration

Let's create a more sophisticated NLU system that can handle various command formats:

```python
import re
from typing import Dict, Any

class NaturalLanguageUnderstanding:
    def __init__(self):
        # Define patterns for different command types
        self.patterns = {
            'pick_up': [
                r"pick\s+(?:up\s+|)(?:the\s+|)(\w+(?:\s+\w+)*)",
                r"grab\s+(?:the\s+|)(\w+(?:\s+\w+)*)",
                r"take\s+(?:the\s+|)(\w+(?:\s+\w+)*)",
                r"get\s+(?:the\s+|)(\w+(?:\s+\w+)*)"
            ],
            'move_to': [
                r"go\s+(?:to\s+|)(?:the\s+|)(\w+(?:\s+\w+)*)",
                r"move\s+(?:to\s+|)(?:the\s+|)(\w+(?:\s+\w+)*)",
                r"walk\s+(?:to\s+|)(?:the\s+|)(\w+(?:\s+\w+)*)",
                r"navigate\s+(?:to\s+|)(?:the\s+|)(\w+(?:\s+\w+)*)"
            ],
            'identify': [
                r"what\s+(?:objects\s+|)(?:do\s+|)(?:you\s+|)see",
                r"find\s+(?:the\s+|)(\w+(?:\s+\w+)*)",
                r"where\s+(?:is\s+|)(?:the\s+|)(\w+(?:\s+\w+)*)"
            ]
        }

    def parse_command(self, text: str) -> Dict[str, Any]:
        text_lower = text.lower().strip()

        for intent_type, patterns in self.patterns.items():
            for pattern in patterns:
                match = re.search(pattern, text_lower)
                if match:
                    # Extract parameters from the match
                    parameters = list(match.groups())
                    target = parameters[0] if parameters and parameters[0] else ""

                    return {
                        'intent': intent_type,
                        'parameters': {'target': target.strip()},
                        'confidence': 0.9
                    }

        # If no pattern matches, return unknown intent
        return {
            'intent': 'unknown',
            'parameters': {'raw_command': text},
            'confidence': 0.1
        }

    def validate_command(self, parsed_command: Dict[str, Any]) -> bool:
        intent = parsed_command['intent']
        params = parsed_command['parameters']

        if intent == 'pick_up':
            target = params.get('target', '')
            if not target:
                return False
            # Additional validation could go here
            return True
        elif intent == 'move_to':
            target = params.get('target', '')
            if not target:
                return False
            # Additional validation could go here
            return True
        elif intent == 'identify':
            return True  # Identification commands are generally valid

        return False
```

## Complete Integration Example

Here's how all the components work together:

```python
class NLToROS2Node(Node):
    def __init__(self):
        super().__init__('nl_to_ros2_node')

        # Initialize components
        self.nlu = NaturalLanguageUnderstanding()
        self.action_manager = ActionExecutionManager(self)

        # Action clients
        self.pick_client = ActionClient(self, PickObject, 'pick_object')
        self.navigate_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        self.find_client = ActionClient(self, FindObject, 'find_object')

        # Wait for servers
        self.pick_client.wait_for_server()
        self.navigate_client.wait_for_server()
        self.find_client.wait_for_server()

        # Subscriber for voice commands
        self.subscription = self.create_subscription(
            String,
            'voice_commands',
            self.voice_command_callback,
            10
        )

        self.get_logger().info('NL to ROS2 Actions node initialized')

    def voice_command_callback(self, msg):
        try:
            # Parse the natural language command
            parsed_command = self.nlu.parse_command(msg.data)

            # Validate the command
            if not self.nlu.validate_command(parsed_command):
                self.get_logger().warn(f'Invalid command: {msg.data}')
                return

            # Execute the appropriate action
            intent = parsed_command['intent']
            parameters = parsed_command['parameters']

            if intent == 'pick_up':
                self.action_manager.execute_pick_action(parameters)
            elif intent == 'move_to':
                self.action_manager.execute_navigate_action(parameters)
            elif intent == 'identify':
                self.action_manager.execute_find_action(parameters)
            else:
                self.get_logger().warn(f'Unknown intent: {intent}')

        except Exception as e:
            self.get_logger().error(f'Error processing command: {str(e)}')

def main(args=None):
    rclpy.init(args=args)
    node = NLToROS2Node()

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

## Exercise: Extend the Action Mapping System

Create an additional action type for "open_door" and integrate it into the system:

1. Define a new action interface for opening doors
2. Create an action server for the open_door action
3. Add a pattern to the NLU system to recognize door-related commands
4. Implement the action execution in the ActionExecutionManager

Example solution:

```python
# 1. Action interface (in your_interfaces/action/OpenDoor.idl)
# string door_name
# ---
# bool success
# string message
# ---
# string status
# float64 progress

# 2. Action server
from your_interfaces.action import OpenDoor

class OpenDoorActionServer(Node):
    def __init__(self):
        super().__init__('open_door_action_server')
        self._action_server = ActionServer(
            self,
            OpenDoor,
            'open_door',
            self.execute_callback
        )

    def execute_callback(self, goal_handle):
        feedback_msg = OpenDoor.Feedback()
        result = OpenDoor.Result()

        door_name = goal_handle.request.door_name
        self.get_logger().info(f'Opening door: {door_name}')

        feedback_msg.status = f'Approaching {door_name}'
        feedback_msg.progress = 0.3
        goal_handle.publish_feedback(feedback_msg)

        # Simulate door opening
        if self.approach_and_open_door(door_name):
            result.success = True
            result.message = f'Successfully opened {door_name}'
            goal_handle.succeed()
        else:
            result.success = False
            result.message = f'Failed to open {door_name}'
            goal_handle.abort()

        return result

# 3. Add pattern to NLU system
# In the patterns dictionary, add:
# 'open_door': [
#     r"open\s+(?:the\s+|)(\w+(?:\s+\w+)*)\s+door",
#     r"open\s+door\s+(?:to\s+|)(\w+(?:\s+\w+)*)"
# ]

# 4. Add execution method to ActionExecutionManager
def execute_open_door_action(self, parameters):
    door_name = parameters.get('target', 'unknown')
    goal_msg = OpenDoor.Goal()
    goal_msg.door_name = door_name

    self.node.get_logger().info(f'Sending open door goal for {door_name}')
    # Implementation similar to other action methods...
```

## Summary

In this chapter, we've covered:
- Mapping natural language intents to ROS 2 actions
- Creating action clients and servers for robot behaviors
- Parameter extraction and validation
- Handling action feedback and results
- Integrating NLU with ROS 2 action systems

## Key Takeaways

- ROS 2 actions provide a robust way to handle long-running robot tasks
- Proper parameter extraction is crucial for accurate command execution
- Feedback mechanisms allow for responsive human-robot interaction
- Validation prevents invalid commands from being executed

## Next Steps

In the next chapter, we'll explore multi-modal perception, combining vision and language to create a more comprehensive understanding system.