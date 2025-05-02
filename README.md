# Simple Wiki

A lightweight wiki system built with Flask.

## Features

- Create and edit wiki pages using Markdown
- Search functionality
- User registration and authentication
- Clean, responsive design
- Simple file-based storage (no database required)

## Installation

1. Clone this repository:

   ```
   git clone <repository-url>
   cd Wiki
   ```

2. Create a virtual environment and activate it:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Wiki

1. Start the Flask development server:

   ```
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

## Usage

### Creating Pages

- Navigate to any non-existent page URL, and you'll be prompted to create it
- Use the search function to look for content, and create new pages from search results
- Use Markdown syntax to format your content

### Markdown Syntax

- `# Heading 1` - Creates a top-level heading
- `## Heading 2` - Creates a second-level heading
- `**bold text**` - Makes text bold
- `*italic text*` - Makes text italic
- `[link text](URL)` - Creates a hyperlink
- `![alt text](image-url)` - Inserts an image
- `- item 1` - Creates a bulleted list
- `1. item 2` - Creates a numbered list
- ```- Creates a code block

  ```

## Customization

- Edit the CSS in `static/css/style.css` to change the appearance
- Modify the templates in the `templates` directory to change the layout

## Production Deployment

For production use, consider:

1. Using a proper database instead of file storage
2. Setting up proper user authentication with password reset
3. Adding CSRF protection
4. Configuring a production WSGI server like Gunicorn
5. Setting up a reverse proxy like Nginx

## License

This project is open source and available under the MIT License.
