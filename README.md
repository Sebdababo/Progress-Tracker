# Progress Tracker Application

## Overview
The Project Manager application is a simple desktop tool built using Python's Tkinter library. It allows users to manage multiple projects, track tasks within each project, and visualize progress.

## Features
- **Project Management**: Create, select, and remove projects.
- **Task Management**: Add, complete, and remove tasks within projects.
- **Progress Tracking**: Visual representation of task completion status.
- **Data Persistence**: Save and load project data to/from a JSON file.

## Requirements
- Python 3.x
- Tkinter library (included with standard Python distribution)

## Installation
1. **Clone the Repository**:
    ```bash
    git clone https://github.com/Sebdababo/Progress-Tracker.git
    cd project-Tracker
    ```
2. **Run the Application**:
    ```bash
    python progress tracker.py
    ```

## Usage
1. **Starting the Application**: 
   - Run `progress tracker.py` to start the application.
   
2. **Creating a New Project**:
   - Click on the "New Project" button.
   - Enter the project name in the dialog that appears.
   
3. **Selecting a Project**:
   - Click on the "Select Project" button.
   - Double-click on a project from the list or select it and click "OK".
   
4. **Removing a Project**:
   - Click on the "Remove Project" button.
   - Select a project from the list and confirm the removal.
   
5. **Adding a Task**:
   - Ensure a project is selected.
   - Click on the "Add Task" button.
   - Enter the task name in the dialog that appears.
   
6. **Completing a Task**:
   - Ensure a project is selected.
   - Click on the "Complete Task" button.
   - Enter the task name in the dialog that appears.
   
7. **Removing a Task**:
   - Ensure a project is selected.
   - Click on the "Remove Task" button.
   - Enter the task name in the dialog that appears.
   
8. **Progress Tracking**:
   - The progress bar at the bottom displays the completion percentage of tasks in the selected project.

## Data Persistence
- Project data is saved to `project_data.json` in the application directory when the window is closed.
- Data is loaded from `project_data.json` when the application starts.

## Closing the Application
- Data is automatically saved when the application window is closed.
