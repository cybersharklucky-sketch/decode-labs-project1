"""
Project 1: To-Do List Application
DecodeLabs Industrial Training Kit 2026
"""

import json
from pathlib import Path
from datetime import datetime


TASKS_FILE = Path("tasks.json")


class TaskManager:
    """Handle all task data and storage."""

    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def _next_id(self):
        return max((task["id"] for task in self.tasks), default=0) + 1

    def add_task(self, description):
        description = description.strip()

        if not description:
            return False, "Task cannot be empty."

        task = {
            "id": self._next_id(),
            "description": description,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "completed": False,
        }

        self.tasks.append(task)
        self.save_tasks()
        return True, f"Task added successfully. ID: {task['id']}"

    def view_tasks(self, show_completed=True):
        if not self.tasks:
            return "No tasks available."

        data = self.tasks if show_completed else [
            task for task in self.tasks if not task["completed"]
        ]

        if not data:
            return "No active tasks."

        output = []
        output.append("-" * 70)
        output.append(f"{'ID':<5}{'Task':<40}{'Status':<12}{'Created'}")
        output.append("-" * 70)

        for task in data:
            status = "Completed" if task["completed"] else "Pending"
            output.append(
                f"{task['id']:<5}{task['description']:<40}"
                f"{status:<12}{task['created_at']}"
            )

        output.append("-" * 70)
        return "\n".join(output)

    def complete_task(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = True
                self.save_tasks()
                return True, "Task marked as completed."

        return False, "Task ID not found."

    def delete_task(self, task_id):
        for index, task in enumerate(self.tasks):
            if task["id"] == task_id:
                self.tasks.pop(index)
                self.save_tasks()
                return True, "Task deleted successfully."

        return False, "Task ID not found."

    def save_tasks(self):
        TASKS_FILE.write_text(json.dumps(self.tasks, indent=4))

    def load_tasks(self):
        if TASKS_FILE.exists():
            try:
                self.tasks = json.loads(TASKS_FILE.read_text())
            except Exception:
                self.tasks = []


class ToDoApp:
    """Console user interface."""

    def __init__(self):
        self.manager = TaskManager()

    def menu(self):
        print("\n" + "=" * 50)
        print("DecodeLabs To-Do List")
        print("=" * 50)
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Complete Task")
        print("4. Delete Task")
        print("5. Exit")
        print("=" * 50)

    def run(self):
        while True:
            self.menu()

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                task = input("Enter task: ")
                print(self.manager.add_task(task)[1])

            elif choice == "2":
                print(self.manager.view_tasks())

            elif choice == "3":
                try:
                    task_id = int(input("Enter Task ID: "))
                    print(self.manager.complete_task(task_id)[1])
                except ValueError:
                    print("Please enter a valid number.")

            elif choice == "4":
                try:
                    task_id = int(input("Enter Task ID: "))
                    print(self.manager.delete_task(task_id)[1])
                except ValueError:
                    print("Please enter a valid number.")

            elif choice == "5":
                print("Thank you.")
                break

            else:
                print("Invalid choice.")

            input("\nPress Enter to continue...")


def main():
    app = ToDoApp()
    app.run()


if __name__ == "__main__":
    main()
