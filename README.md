# CloudflareDNSUpdater

**CloudflareDNSUpdater** is a Python-based utility for automatically updating DNS records with Cloudflare. It ensures your domain's DNS settings are always in sync with your current public IP address by periodically checking and updating Cloudflare's DNS records.

## Features

- **Automatic DNS Updates**: Periodically updates DNS records to match your current public IP address.
- **Configurable Interval**: Set the frequency of DNS updates in minutes.
- **GUI Interface**: User-friendly graphical interface for easy configuration and management.
- **API Token Support**: Utilizes Cloudflare's API tokens for secure access.
- **Startup Integration**: Optionally start the updater automatically with Windows.
- **Dynamic Record Fetching**: Retrieves and displays DNS records from Cloudflare in a dropdown list for easy selection.

## Installation

You can install CloudflareDNSUpdater by following the instructions below.

### Download

- **Windows Executable:** You can download the Windows executable file from the [releases page](releases/windows_executable/).

### Using the Executable

1. **Download the Executable:** Visit the [releases page](releases/windows_executable/) and download CloudflareDNSUpdater.exe`.
2. **Run the Executable:** Double-click the downloaded file to start the application. If you are prompted for administrator privileges, grant them to allow the application to function correctly.

## Getting Started

### Prerequisites

- **Python 3.6+**: Ensure Python 3.6 or higher is installed on your system.
- **Python Packages**: Install the required packages using pip.



### Usage

1. **Configure the Updater**:
    - Open the GUI application.
    - Enter your Cloudflare API token, zone ID, and DNS record details.

2. **Start Updating**:
    - Click the **"Start Updating"** button to begin automatic DNS updates.

3. **Update DNS Records List**:
    - Click the **"Update Record List"** button to fetch and display DNS records in the dropdown.

### GUI Configuration

- **API Token**: Enter your Cloudflare API token to authenticate.
- **Zone ID**: Provide the Zone ID of the domain you want to update.
- **DNS Record**: Select the DNS record you want to update from the dropdown list.
- **(Sub)Domain**: Enter the domain or subdomain for which the DNS record should be updated.
- **Record Type**: Specify the type of DNS record (e.g., `A` for address).
- **Update Interval**: Set how often (in minutes) the DNS record should be updated.
- **Start with Windows**: Check this option to start the updater automatically when Windows boots.

## License

This project is licensed under the [MIT License](LICENSE). See the [LICENSE](LICENSE) file for more details.

## Contributing

Contributions are welcome! If you have suggestions or improvements, please submit a pull request or open an issue.

## Contact

For questions or support, please contact geral.lemondrops@gmail.com or open an issue in this repository.

---

Happy updating!
