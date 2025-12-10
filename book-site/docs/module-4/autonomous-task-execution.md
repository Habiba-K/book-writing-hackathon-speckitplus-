---
id: autonomous-task-execution
title: "Autonomous Task Execution"
sidebar_label: "Autonomous Task Execution"
sidebar_position: 4
---

# Autonomous Task Execution

## Introduction

In this chapter, we'll explore how to create autonomous task execution systems that can plan, act, monitor, and recover from failures. Building on the perception and language understanding from previous chapters, we'll create systems that can execute complex multi-step tasks autonomously.

## Learning Objectives

By the end of this chapter, you will be able to:
- Plan and execute multi-step robotic tasks
- Monitor task execution and detect failures
- Implement error recovery strategies
- Create robust autonomous systems

## Overview

Autonomous task execution involves:
1. Breaking down complex tasks into executable steps
2. Planning the sequence of actions needed
3. Executing actions while monitoring progress
4. Detecting and recovering from failures
5. Providing feedback to users

## Task Planning and Sequencing

### Task Representation

First, let's define how we represent tasks and their dependencies:

```python
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskType(Enum):
    NAVIGATION = "navigation"
    MANIPULATION = "manipulation"
    PERCEPTION = "perception"
    COMMUNICATION = "communication"

@dataclass
class TaskStep:
    """Represents a single step in a task"""
    id: str
    name: str
    task_type: TaskType
    parameters: Dict[str, Any]
    dependencies: List[str]  # IDs of tasks that must complete first
    timeout: float = 30.0  # seconds

@dataclass
class Task:
    """Represents a complete task with multiple steps"""
    id: str
    name: str
    description: str
    steps: List[TaskStep]
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = None
    started_at: datetime = None
    completed_at: datetime = None
    current_step: int = 0
    error_message: Optional[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
```

### Task Planner

```python
class TaskPlanner:
    def __init__(self):
        self.tasks = {}  # task_id -> Task
        self.task_queue = []  # Queue of pending tasks

    def create_task_from_intent(self, intent: Dict[str, Any]) -> Task:
        """
        Create a task from a natural language intent
        """
        intent_type = intent.get('intent_type', 'unknown')
        parameters = intent.get('parameters', {})

        if intent_type == 'pick_up':
            return self._create_pickup_task(parameters)
        elif intent_type == 'move_to':
            return self._create_navigation_task(parameters)
        elif intent_type == 'find_object':
            return self._create_find_task(parameters)
        else:
            raise ValueError(f"Unknown intent type: {intent_type}")

    def _create_pickup_task(self, parameters: Dict[str, Any]) -> Task:
        """Create a pickup task with multiple steps"""
        object_name = parameters.get('target', 'unknown')

        steps = [
            TaskStep(
                id=str(uuid.uuid4()),
                name=f"Locate {object_name}",
                task_type=TaskType.PERCEPTION,
                parameters={'object_name': object_name},
                dependencies=[]
            ),
            TaskStep(
                id=str(uuid.uuid4()),
                name=f"Navigate to {object_name}",
                task_type=TaskType.NAVIGATION,
                parameters={'target_object': object_name},
                dependencies=[steps[0].id if 'steps' in locals() else '']  # Will be fixed
            ),
            TaskStep(
                id=str(uuid.uuid4()),
                name=f"Pick up {object_name}",
                task_type=TaskType.MANIPULATION,
                parameters={'object_name': object_name},
                dependencies=[steps[1].id if len(steps) > 1 else '']  # Will be fixed
            )
        ]

        # Fix dependencies after creating all steps
        for i, step in enumerate(steps):
            if i > 0:
                step.dependencies = [steps[i-1].id]

        task_id = str(uuid.uuid4())
        task = Task(
            id=task_id,
            name=f"Pick up {object_name}",
            description=f"Task to locate, navigate to, and pick up {object_name}",
            steps=steps
        )

        return task

    def _create_navigation_task(self, parameters: Dict[str, Any]) -> Task:
        """Create a navigation task"""
        location = parameters.get('target', 'unknown')

        steps = [
            TaskStep(
                id=str(uuid.uuid4()),
                name=f"Plan path to {location}",
                task_type=TaskType.PERCEPTION,
                parameters={'target_location': location},
                dependencies=[]
            ),
            TaskStep(
                id=str(uuid.uuid4()),
                name=f"Navigate to {location}",
                task_type=TaskType.NAVIGATION,
                parameters={'target_location': location},
                dependencies=[steps[0].id]
            )
        ]

        task_id = str(uuid.uuid4())
        task = Task(
            id=task_id,
            name=f"Navigate to {location}",
            description=f"Task to navigate to {location}",
            steps=steps
        )

        return task

    def _create_find_task(self, parameters: Dict[str, Any]) -> Task:
        """Create a find object task"""
        query = parameters.get('query', 'objects')

        steps = [
            TaskStep(
                id=str(uuid.uuid4()),
                name=f"Scan environment for {query}",
                task_type=TaskType.PERCEPTION,
                parameters={'query': query},
                dependencies=[]
            ),
            TaskStep(
                id=str(uuid.uuid4()),
                name=f"Report findings about {query}",
                task_type=TaskType.COMMUNICATION,
                parameters={'query': query},
                dependencies=[steps[0].id]
            )
        ]

        task_id = str(uuid.uuid4())
        task = Task(
            id=task_id,
            name=f"Find {query}",
            description=f"Task to find and report about {query}",
            steps=steps
        )

        return task
```

## Task Execution Engine

### Basic Task Executor

```python
import asyncio
import time
from typing import Callable, Awaitable

class TaskExecutor:
    def __init__(self):
        self.active_tasks = {}  # task_id -> Task
        self.step_executors = {
            TaskType.NAVIGATION: self._execute_navigation_step,
            TaskType.MANIPULATION: self._execute_manipulation_step,
            TaskType.PERCEPTION: self._execute_perception_step,
            TaskType.COMMUNICATION: self._execute_communication_step
        }

    async def execute_task(self, task: Task) -> Task:
        """
        Execute a complete task with monitoring and error handling
        """
        self.active_tasks[task.id] = task
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.now()

        try:
            for i, step in enumerate(task.steps):
                if task.status != TaskStatus.RUNNING:
                    break

                # Check dependencies
                if not self._check_dependencies_satisfied(task, step):
                    task.status = TaskStatus.FAILED
                    task.error_message = f"Dependencies not satisfied for step {step.name}"
                    break

                # Execute the step
                success = await self._execute_step(task, step, i)
                if not success:
                    task.status = TaskStatus.FAILED
                    break

                task.current_step = i + 1

            if task.status == TaskStatus.RUNNING:
                task.status = TaskStatus.COMPLETED
                task.completed_at = datetime.now()

        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error_message = str(e)

        finally:
            if task.id in self.active_tasks:
                del self.active_tasks[task.id]

        return task

    def _check_dependencies_satisfied(self, task: Task, step: TaskStep) -> bool:
        """
        Check if all dependencies for a step are satisfied
        """
        for dep_id in step.dependencies:
            # Find the dependency step in the task
            dep_step = next((s for s in task.steps if s.id == dep_id), None)
            if dep_step:
                # In a real system, you'd track the actual status of each step
                # For this example, we assume dependencies are satisfied
                pass

        return True

    async def _execute_step(self, task: Task, step: TaskStep, step_index: int) -> bool:
        """
        Execute a single task step
        """
        print(f"Executing step {step_index + 1}: {step.name}")

        # Get the appropriate executor
        executor = self.step_executors.get(step.task_type)
        if not executor:
            print(f"No executor found for task type {step.task_type}")
            return False

        try:
            # Execute the step with timeout
            result = await asyncio.wait_for(
                executor(step.parameters),
                timeout=step.timeout
            )
            return result
        except asyncio.TimeoutError:
            print(f"Step {step.name} timed out")
            return False
        except Exception as e:
            print(f"Error executing step {step.name}: {str(e)}")
            return False

    async def _execute_navigation_step(self, parameters: Dict[str, Any]) -> bool:
        """
        Execute a navigation step
        """
        target_location = parameters.get('target_location', 'unknown')
        target_object = parameters.get('target_object', 'unknown')

        print(f"Navigating to {target_location or target_object}")

        # Simulate navigation
        await asyncio.sleep(2)  # Simulate time for navigation

        # In a real system, this would call ROS 2 navigation services
        success = True  # Simulate success

        print(f"Navigation to {target_location or target_object} completed")
        return success

    async def _execute_manipulation_step(self, parameters: Dict[str, Any]) -> bool:
        """
        Execute a manipulation step
        """
        object_name = parameters.get('object_name', 'unknown')

        print(f"Attempting to manipulate {object_name}")

        # Simulate manipulation
        await asyncio.sleep(3)  # Simulate time for manipulation

        # In a real system, this would call ROS 2 manipulation services
        success = True  # Simulate success

        print(f"Manipulation of {object_name} completed")
        return success

    async def _execute_perception_step(self, parameters: Dict[str, Any]) -> bool:
        """
        Execute a perception step
        """
        object_name = parameters.get('object_name', 'unknown')
        target_location = parameters.get('target_location', 'unknown')
        query = parameters.get('query', 'objects')

        if object_name:
            print(f"Looking for {object_name}")
        elif target_location:
            print(f"Planning path to {target_location}")
        else:
            print(f"Scanning for {query}")

        # Simulate perception
        await asyncio.sleep(1)  # Simulate time for perception

        # In a real system, this would call ROS 2 perception services
        success = True  # Simulate success

        print("Perception step completed")
        return success

    async def _execute_communication_step(self, parameters: Dict[str, Any]) -> bool:
        """
        Execute a communication step
        """
        query = parameters.get('query', 'unknown')

        print(f"Communicating about {query}")

        # Simulate communication
        await asyncio.sleep(0.5)  # Simulate time for communication

        # In a real system, this would publish messages or call services
        success = True  # Simulate success

        print("Communication step completed")
        return success
```

## Monitoring and Feedback

### Task Monitor

```python
class TaskMonitor:
    def __init__(self):
        self.observers = []  # List of callback functions
        self.task_status_history = {}  # task_id -> list of status changes

    def add_observer(self, callback: Callable[[Dict], None]):
        """
        Add an observer to be notified of task status changes
        """
        self.observers.append(callback)

    def notify_observers(self, task_id: str, status: TaskStatus, progress: float = 0.0):
        """
        Notify all observers of a task status change
        """
        notification = {
            'task_id': task_id,
            'status': status.value,
            'progress': progress,
            'timestamp': datetime.now()
        }

        for observer in self.observers:
            try:
                observer(notification)
            except Exception as e:
                print(f"Error notifying observer: {str(e)}")

    def track_task_progress(self, task_id: str, status: TaskStatus, progress: float = 0.0):
        """
        Track task progress and notify observers
        """
        if task_id not in self.task_status_history:
            self.task_status_history[task_id] = []

        self.task_status_history[task_id].append({
            'status': status.value,
            'progress': progress,
            'timestamp': datetime.now()
        })

        self.notify_observers(task_id, status, progress)

    def get_task_history(self, task_id: str) -> List[Dict]:
        """
        Get the status history for a task
        """
        return self.task_status_history.get(task_id, [])
```

## Error Recovery System

### Recovery Strategies

```python
from enum import Enum

class RecoveryStrategy(Enum):
    RETRY = "retry"
    SKIP = "skip"
    ABORT = "abort"
    FALLBACK = "fallback"

class ErrorRecovery:
    def __init__(self):
        self.recovery_strategies = {
            'navigation_timeout': RecoveryStrategy.RETRY,
            'object_not_found': RecoveryStrategy.SKIP,
            'grasp_failure': RecoveryStrategy.RETRY,
            'path_blocked': RecoveryStrategy.FALLBACK,
            'communication_error': RecoveryStrategy.RETRY
        }

    def determine_recovery_strategy(self, error_type: str) -> RecoveryStrategy:
        """
        Determine the appropriate recovery strategy for an error
        """
        return self.recovery_strategies.get(error_type, RecoveryStrategy.ABORT)

    def execute_recovery(self, task: Task, step: TaskStep, error_type: str) -> bool:
        """
        Execute recovery based on the error type
        """
        strategy = self.determine_recovery_strategy(error_type)
        print(f"Recovery strategy for {error_type}: {strategy.value}")

        if strategy == RecoveryStrategy.RETRY:
            return self._retry_step(task, step)
        elif strategy == RecoveryStrategy.SKIP:
            return self._skip_step(task, step)
        elif strategy == RecoveryStrategy.FALLBACK:
            return self._fallback_step(task, step)
        else:  # ABORT
            return False

    def _retry_step(self, task: Task, step: TaskStep) -> bool:
        """
        Retry the failed step
        """
        print(f"Retrying step: {step.name}")
        # In a real system, you might add delay, change parameters, etc.
        return True  # Simulate successful retry

    def _skip_step(self, task: Task, step: TaskStep) -> bool:
        """
        Skip the failed step and continue with the task
        """
        print(f"Skipping step: {step.name}")
        # Update task to mark this step as skipped
        # In a real system, you'd need to handle dependencies
        return True

    def _fallback_step(self, task: Task, step: TaskStep) -> bool:
        """
        Execute a fallback action
        """
        print(f"Executing fallback for step: {step.name}")
        # Implement fallback logic
        return True
```

## Complete Task Execution System

### Main Task Manager

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

class TaskManager:
    def __init__(self):
        self.task_planner = TaskPlanner()
        self.task_executor = TaskExecutor()
        self.task_monitor = TaskMonitor()
        self.error_recovery = ErrorRecovery()
        self.executor = ThreadPoolExecutor(max_workers=4)

    async def execute_intent(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a natural language intent as a task
        """
        try:
            # Create task from intent
            task = self.task_planner.create_task_from_intent(intent)
            print(f"Created task: {task.name}")

            # Monitor the task
            self.task_monitor.add_observer(
                lambda notification: print(f"Task {notification['task_id']}: {notification['status']} ({notification['progress']:.1%})")
            )

            # Execute the task
            result_task = await self.task_executor.execute_task(task)

            # Return result
            return {
                'task_id': result_task.id,
                'success': result_task.status == TaskStatus.COMPLETED,
                'status': result_task.status.value,
                'error_message': result_task.error_message,
                'steps_completed': result_task.current_step,
                'total_steps': len(result_task.steps)
            }

        except Exception as e:
            return {
                'success': False,
                'error_message': str(e),
                'status': 'failed'
            }

    async def execute_multi_step_task(self, intent_sequence: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Execute a sequence of intents as a multi-step task
        """
        results = []
        for intent in intent_sequence:
            result = await self.execute_intent(intent)
            results.append(result)

            # If a step fails and is critical, we might want to stop
            if not result['success']:
                print(f"Task failed: {result.get('error_message', 'Unknown error')}")
                break

        return results
```

## Integration with ROS 2

### Task Execution Node

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from your_interfaces.srv import ExecuteTask  # Custom service
from your_interfaces.msg import TaskStatus as TaskStatusMsg

class TaskExecutionNode(Node):
    def __init__(self):
        super().__init__('task_execution_node')

        # Initialize task management components
        self.task_manager = TaskManager()

        # Service to execute tasks
        self.task_service = self.create_service(
            ExecuteTask,
            'execute_task',
            self.execute_task_callback
        )

        # Publisher for task status updates
        self.status_publisher = self.create_publisher(
            TaskStatusMsg,
            'task_status',
            10
        )

        # Subscriber for task cancellation
        self.cancel_subscriber = self.create_subscription(
            String,
            'cancel_task',
            self.cancel_task_callback,
            10
        )

        # Add monitor observer to publish status updates
        self.task_manager.task_monitor.add_observer(
            self._publish_task_status
        )

        self.get_logger().info('Task Execution node initialized')

    def execute_task_callback(self, request, response):
        """
        Execute a task from a service request
        """
        try:
            # Parse the intent from the request
            intent = {
                'intent_type': request.intent_type,
                'parameters': dict(request.parameters)
            }

            # Execute the task (this would need to be async in practice)
            # For this example, we'll use a simplified approach
            result = asyncio.run(
                self.task_manager.execute_intent(intent)
            )

            # Set response
            response.success = result['success']
            response.task_id = result.get('task_id', '')
            response.message = result.get('error_message', 'Task completed successfully')

        except Exception as e:
            response.success = False
            response.message = f"Error executing task: {str(e)}"

        return response

    def cancel_task_callback(self, msg):
        """
        Handle task cancellation requests
        """
        task_id = msg.data
        self.get_logger().info(f'Request to cancel task: {task_id}')
        # In a real implementation, you'd have a way to cancel active tasks

    def _publish_task_status(self, notification):
        """
        Publish task status updates
        """
        status_msg = TaskStatusMsg()
        status_msg.task_id = notification['task_id']
        status_msg.status = notification['status']
        status_msg.progress = notification['progress']
        status_msg.timestamp = self.get_clock().now().to_msg()

        self.status_publisher.publish(status_msg)

def main(args=None):
    rclpy.init(args=args)
    node = TaskExecutionNode()

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

## Practical Example: Multi-Step Task Execution

Here's a complete example that demonstrates the autonomous task execution system:

```python
async def example_multi_step_task():
    """
    Example: Execute a complex task like "Go to the kitchen, find a cup, and bring it to me"
    """
    task_manager = TaskManager()

    # Break down the complex intent into individual intents
    intent_sequence = [
        {
            'intent_type': 'move_to',
            'parameters': {'target': 'kitchen'}
        },
        {
            'intent_type': 'find_object',
            'parameters': {'query': 'cup'}
        },
        {
            'intent_type': 'pick_up',
            'parameters': {'target': 'cup'}
        },
        {
            'intent_type': 'move_to',
            'parameters': {'target': 'user location'}
        }
    ]

    print("Executing multi-step task: 'Go to the kitchen, find a cup, and bring it to me'")
    results = await task_manager.execute_multi_step_task(intent_sequence)

    print("\nTask execution results:")
    for i, result in enumerate(results):
        status = "✓" if result['success'] else "✗"
        print(f"Step {i+1}: {status} {result.get('error_message', 'Success')}")

# Example of error recovery
async def example_error_recovery():
    """
    Example: Demonstrate error recovery in task execution
    """
    task_manager = TaskManager()

    # Simulate a task that might fail
    intent = {
        'intent_type': 'pick_up',
        'parameters': {'target': 'red cube'}
    }

    print("\nExecuting task with potential error recovery...")
    result = await task_manager.execute_intent(intent)
    print(f"Task result: {result}")

if __name__ == "__main__":
    # Run the examples
    asyncio.run(example_multi_step_task())
    asyncio.run(example_error_recovery())
```

## Exercise: Implement a Custom Task Scheduler

Create a task scheduler that can:
1. Schedule tasks to run at specific times
2. Handle task priorities
3. Manage resource conflicts between tasks
4. Provide progress tracking

Example solution:

```python
import heapq
from datetime import datetime, timedelta
from enum import Enum

class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class ScheduledTask:
    def __init__(self, task, scheduled_time, priority=TaskPriority.MEDIUM):
        self.task = task
        self.scheduled_time = scheduled_time
        self.priority = priority
        self.id = str(uuid.uuid4())

    def __lt__(self, other):
        # For priority queue: higher priority first, then earlier time
        if self.priority.value != other.priority.value:
            return self.priority.value > other.priority.value
        return self.scheduled_time < other.scheduled_time

class TaskScheduler:
    def __init__(self):
        self.task_queue = []  # Priority queue of scheduled tasks
        self.active_tasks = set()  # Currently executing tasks
        self.completed_tasks = []  # History of completed tasks

    def schedule_task(self, task, delay_seconds=0, priority=TaskPriority.MEDIUM):
        """
        Schedule a task to run after a delay
        """
        scheduled_time = datetime.now() + timedelta(seconds=delay_seconds)
        scheduled_task = ScheduledTask(task, scheduled_time, priority)

        heapq.heappush(self.task_queue, scheduled_task)
        print(f"Scheduled task '{task.name}' for {scheduled_time} with priority {priority.value}")

    def run_scheduled_tasks(self):
        """
        Execute tasks that are ready to run
        """
        current_time = datetime.now()
        ready_tasks = []

        # Find all tasks that are ready to execute
        while self.task_queue and self.task_queue[0].scheduled_time <= current_time:
            ready_tasks.append(heapq.heappop(self.task_queue))

        # Execute ready tasks
        for scheduled_task in ready_tasks:
            print(f"Executing scheduled task: {scheduled_task.task.name}")
            # In a real system, you'd execute the task asynchronously
            # For this example, we'll just mark it as completed
            self.completed_tasks.append(scheduled_task)
            print(f"Completed scheduled task: {scheduled_task.task.name}")

    def get_schedule_status(self):
        """
        Get the status of scheduled tasks
        """
        return {
            'pending_tasks': len(self.task_queue),
            'active_tasks': len(self.active_tasks),
            'completed_tasks': len(self.completed_tasks),
            'next_task_time': self.task_queue[0].scheduled_time if self.task_queue else None
        }

# Example usage of the scheduler
def example_scheduler():
    scheduler = TaskScheduler()

    # Create some sample tasks
    task1 = Task(
        id="task1",
        name="Check room temperature",
        description="Monitor room temperature and adjust HVAC",
        steps=[]
    )

    task2 = Task(
        id="task2",
        name="Greet user",
        description="Welcome user and provide status update",
        steps=[]
    )

    # Schedule tasks
    scheduler.schedule_task(task1, delay_seconds=5, priority=TaskPriority.HIGH)
    scheduler.schedule_task(task2, delay_seconds=10, priority=TaskPriority.MEDIUM)

    print("Initial schedule status:", scheduler.get_schedule_status())

    # Run scheduled tasks
    import time
    time.sleep(6)  # Wait for first task to be ready
    scheduler.run_scheduled_tasks()

    print("After running tasks:", scheduler.get_schedule_status())

if __name__ == "__main__":
    example_scheduler()
```

## Summary

In this chapter, we've covered:
- Task planning and representation for autonomous execution
- Task execution engines with monitoring capabilities
- Error detection and recovery strategies
- Integration with ROS 2 for real-time task execution
- Scheduling and prioritization of tasks

## Key Takeaways

- Autonomous task execution requires breaking complex tasks into manageable steps
- Monitoring is crucial for detecting failures and tracking progress
- Error recovery strategies should be planned for different failure modes
- Task scheduling and prioritization help manage complex workflows
- ROS 2 integration enables real-time autonomous behavior in robotics

## Next Steps

In the next chapter, we'll explore the capstone integration, bringing together all the components we've developed into a complete Vision-Language-Action system.