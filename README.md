---

# Python Flask Blog

This project is a simple blog application built using **Python** and the **Flask** web framework. The blog allows users to view posts and provides the ability for an admin to add, edit, and delete blog posts.

## Features

- View all blog posts.
- Add/Edit/Delete posts (Admin access).
- Clean and responsive UI using Bootstrap.
- Session-based admin authentication.

## Project Structure

```bash
├── static
│   └── (CSS, JavaScript, images)
├── templates
│   ├── layout.html
│   ├── index.html
│   ├── edit.html
│   ├── post.html
│   └── (other HTML templates)
├── instance
│   └── config.json  # Secret settings (like admin credentials)
├── main.py  # Main Flask application
├── tc.py  # Additional utilities or configurations
└── config.json  # General application configuration
```

## Installation

### Prerequisites

- Python 3.x
- Flask

### 1. Clone the repository

```bash
git clone https://github.com/SonuSharma828/Python-flask-blog.git
cd Python-flask-blog
```

### 2. Create a Virtual Environment (Optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Required Packages

```bash
pip install -r requirements.txt
```

### 4. Configure the Application

- Open the `instance/config.json` file and set up the necessary details like:
  - `admin-user`: Username for admin access.
  - `admin-password`: Password for admin access.
  - Other general settings (like database settings).

### 5. Run the Application

```bash
python main.py
```

The app will be running on [http://localhost:5000](http://localhost:5000).

## Usage

### Admin Panel

To add, edit, or delete posts, log in with the admin credentials provided in the `config.json`. Once logged in, you will be able to:
- Add a new post.
- Edit an existing post.
- Delete posts.

### Main Blog

Users can visit the main blog page to view all the blog posts.

## Screenshots

### Blog Homepage
![Blog Homepage](static/assets/img/homepage-screenshot.jpg)

### Admin Edit Post Page
![Admin Edit Post](static/assets/img/editpost-screenshot.jpg)

## Contributing

If you'd like to contribute, feel free to fork the repository and submit a pull request. For major changes, please open an issue first to discuss what you'd like to change.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to adjust this template to match any additional features or information you want to include!
