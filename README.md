# Influencer Management System

This project is an Influencer Management System designed to handle influencer profiles, campaign management, ad requests, and associated API endpoints.

## Table of Contents

-   [Project Overview](#project-overview)
-   [Features](#features)
-   [Directory Structure](#directory-structure)
-   [Installation](#installation)
-   [Usage](#usage)
-   [API Documentation](#api-documentation)
-   [Testing](#testing)
-   [Contributing](#contributing)
-   [License](#license)

## Project Overview

The Influencer Management System provides functionalities for managing influencers, sponsors, campaigns, and ad requests. It allows administrators to oversee all aspects of the campaigns and track ad performance effectively.

## Features

-   Admin management
-   Influencer management
-   Sponsor management
-   Campaign management
-   Ad request handling
-   Ad performance tracking
-   API endpoints for all major functionalities

## Directory Structure

```./
├── .gitignore
├── dir.txt
├── local_run.bat
├── local_setup.bat
├── README.md
├── requirements.txt
├── run.py
├── app/
│ ├── config.py
│ ├── data.py
│ ├── models.py
│ ├── init.py
│ ├── api/
│ │ ├── admin.py
│ │ ├── adperformance.py
│ │ ├── adrequest.py
│ │ ├── campaign.py
│ │ ├── influencer.py
│ │ ├── sponsor.py
│ │ └── init.py
│ ├── static/
│ │ ├── css/
│ │ │ ├── index.css
│ │ │ ├── style.css
│ │ │ ├── admin/
│ │ │ │ ├── admins.css
│ │ │ │ ├── campaigns.css
│ │ │ │ ├── dashboard.css
│ │ │ │ ├── influencers.css
│ │ │ │ └── sponsors.css
│ │ │ ├── auth/
│ │ │ │ ├── login.css
│ │ │ │ ├── register_influencer.css
│ │ │ │ └── register_sponsor.css
│ │ │ ├── influencer/
│ │ │ │ ├── dashboard.css
│ │ │ │ ├── find_campaign.css
│ │ │ │ ├── profile.css
│ │ │ │ ├── sponsors.css
│ │ │ │ └── stats.css
│ │ │ ├── sponsor/
│ │ │ │ ├── dashboard.css
│ │ │ │ ├── influencers.css
│ │ │ │ └── profile.css
│ │ ├── img/
│ │ │ ├── path_to_profile_picture.webp
│ │ │ ├── icons/
│ │ │ └── logos/
│ │ ├── js/
│ │ │ ├── admin/
│ │ │ │ ├── admins.js
│ │ │ │ ├── campaigns.js
│ │ │ │ ├── dashboard.js
│ │ │ │ ├── influencers.js
│ │ │ │ └── sponsors.js
│ │ │ ├── auth/
│ │ │ │ ├── login.js
│ │ │ │ ├── register_influencer.js
│ │ │ │ └── register_sponsor.js
│ │ │ ├── influencer/
│ │ │ │ ├── dashboard.js
│ │ │ │ ├── find_campaign.js
│ │ │ │ ├── profile.js
│ │ │ │ ├── sponsors.js
│ │ │ │ └── stats.js
│ │ │ ├── sponsor/
│ │ │ ├── campaigns.js
│ │ │ ├── dashboard.js
│ │ │ ├── influencers.js
│ │ │ ├── profile.js
│ │ │ └── stats.js
│ ├── templates/
│ │ ├── index.html
│ │ ├── admin/
│ │ │ ├── admins.html
│ │ │ ├── campaigns.html
│ │ │ ├── dashboard.html
│ │ │ ├── influencers.html
│ │ │ └── sponsors.html
│ │ ├── auth/
│ │ │ ├── login.html
│ │ │ ├── register_influencer.html
│ │ │ └── register_sponsor.html
│ │ ├── influencer/
│ │ │ ├── dashboard.html
│ │ │ ├── find_campaign.html
│ │ │ ├── profile.html
│ │ │ ├── sponsors.html
│ │ │ └── stats.html
│ │ ├── sponsor/
│ │ ├── campaigns.html
│ │ ├── dashboard.html
│ │ ├── influencers.html
│ │ ├── profile.html
│ │ └── stats.html
│ ├── views/
│ │ ├── admin.py
│ │ ├── auth.py
│ │ ├── influencer.py
│ │ ├── sponsor.py
│ │ └── init.py
├── docs/
│ └── api.yaml
└── instance/
└── database.db
```

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/influencer-management-system.git
    cd influencer-management-system
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Configure your environment variables in `config.py`.

## Usage

1. Start the application:

    ```sh
    python run.py
    ```

2. Access the application at `http://localhost:5000`.

## API Documentation

The API documentation is available in the `docs/api.yaml` file. You can view it using any YAML viewer or import it into tools like Swagger UI or Postman.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

Fork the repository.
Create a new branch for your feature or bug fix.
Commit your changes.
Push the branch and create a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
