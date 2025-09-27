[README.md](https://github.com/user-attachments/files/22574474/README.md)
# OOPS — Projects Organized by Folder
This repository contains several small Python projects (data structures and small demos) organized into top-level folders. This README shows what lives where and how to run each component.

## Repository layout
- `smarthome/` — Smart Home model and GUI
	- `smarthome.py` — device models and CLI
	- `ui.smarthome.py` — Tkinter desktop GUI
- `stack/` — Stack implementations and exercises
	- `stack_linked_list.py` — linked-list-based Stack + parentheses checker
	- `stackproblem.py` — original stack/assignment file
- `messagingqueue/` — Message queue implementation
	- `messagingqueue.py`
- `bankaccount/` — `bankaccount.py` (bank account example)
- `tvmodel/` — `tvmodel.py` (TV model example)
- `pacman/` — `pacman.1.py` (game example)
- `README.md`, `LICENSE` — repo docs and license

## Quick start
1. Clone the repository:
```powershell
git clone https://github.com/rahul200618/OOPS.git
cd OOPS
```

2. (Optional) Create and activate a virtual environment:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## How to run the examples

Smarthome GUI (desktop)
```powershell
python smarthome/ui.smarthome.py
```

Smarthome CLI
```powershell
python smarthome/smarthome.py
```

Stack (linked-list implementation)
```powershell
python stack/stack_linked_list.py
```

Messaging Queue (console)
```powershell
python messagingqueue/messagingqueue.py
```

Other example scripts can be run in a similar way from their folders.

## Notes
- I added a `.gitignore` to exclude archives and `__pycache__`. If you need files ignored differently, update `.gitignore`.
- The repository contains small demo programs; feel free to reorganize per-project or extract into separate repos if you prefer.

## Contributing
- Create a branch for a feature (e.g., `feature/smarthome-improvements`), then open a pull request.

## License
This project is licensed under the MIT License — see the `LICENSE` file.

## Author
[rahul200618](https://github.com/rahul200618)
