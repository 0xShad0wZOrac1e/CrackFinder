# CrackFinder: Find Cracks Around Recognized Sites

CrackFinder is a Python script designed to search for cracked games across various recognized sites. It leverages web scraping techniques to gather results from multiple sources, providing a consolidated list of available game cracks.

## Features

- Supports multiple sites for comprehensive search results.
- Customizable search queries and site selection.
- Adjustable timeout between requests to avoid being flagged as a bot.
- Option to save results to a file.

## Requirements

- Python 3.x
- Required libraries: `requests`, `beautifulsoup4`

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/CrackFinder.git
    cd CrackFinder
    ```

2. Install the required libraries:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

Run the script from the command line with the following options:

```sh
python crackfinder.py --name <crack_name> [--sites <site1,site2,...>] [--timeout <seconds>] [--save <True/False>]
```

### Arguments

- `--name`: **(Required)** The name of the crack to search for.
- `--sites`: Comma-separated list of sites to search. Default is "all".
- `--timeout`: Time (in seconds) to wait between each request. Default is 2 seconds.
- `--save`: Boolean flag to save the results to a file. Default is False.

### Example

```sh
python crackfinder.py --name "example_game" --sites "gog-games,ovagames" --timeout 3 --save True
```

## Supported Sites

- GOG Games
- Gload
- Online Fix
- OvaGames
- G4U
- RLSBB
- Downloadha
- DigitalZone
- GameDrive

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss your ideas.

## Contact

For any questions or issues, please open an issue on the GitHub repository.

---

*Note: This script is for educational purposes only. Downloading and using cracked software is illegal and unethical. Always support the developers by purchasing legitimate copies of the software.*
